#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通用 AWS S3 下载器 (Generic S3 Downloader)
支持下载单个文件或整个文件夹，自动检测并适配
"""

import os
import re
import sys
import boto3
import signal
import argparse
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from botocore import UNSIGNED
from botocore.config import Config


class S3Downloader:
    def __init__(self, s3_url=None, profile_name=None, access_key=None, secret_key=None,
                 region=None, output_dir=None, max_workers=10, anonymous=False):
        """
        初始化S3下载器

        参数:
            s3_url (str): S3链接，支持多种格式的S3 URL
            profile_name (str): AWS配置文件名称
            access_key (str): AWS访问密钥ID
            secret_key (str): AWS秘密访问密钥
            region (str): AWS区域
            output_dir (str): 本地输出目录
            max_workers (int): 最大并发下载线程数
            anonymous (bool): 是否使用匿名访问模式
        """
        self.s3_url = s3_url
        self.profile_name = profile_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.output_dir = output_dir or os.getcwd()
        self.max_workers = max_workers
        self.anonymous = anonymous
        self.keep_structure = False

        # S3 相关属性
        self.bucket_name = None
        self.key = None
        self.s3_client = None

        # 下载统计
        self.lock = threading.Lock()
        self.total_files = 0
        self.downloaded_files = 0
        self.progress_bar = None

        # 下载类型标识
        self.download_type = None  # 'file' 或 'folder'

        # 中断标志
        self.interrupted = False
        self.executor = None

        # 设置信号处理器
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置信号处理器，用于处理Ctrl+C等中断信号"""
        def signal_handler(signum, frame):
            print("\n\n检测到中断信号，正在安全退出...")
            self.interrupted = True

            # 关闭进度条
            if self.progress_bar:
                self.progress_bar.close()

            # 如果正在进行文件夹下载，取消所有正在进行的任务
            if self.executor:
                self.executor.shutdown(wait=False)

            # 打印下载统计
            print(f"\n已下载 {self.downloaded_files}/{self.total_files} 个文件")
            print("下载已中断，程序即将退出...")

            sys.exit(1)

        # 注册信号处理器
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # 终止信号

    def _parse_s3_url(self, s3_url):
        """
        解析S3 URL

        支持多种格式:
        - s3://bucket-name/path/to/file
        - https://bucket-name.s3.region.amazonaws.com/path/to/file
        - https://s3-region.amazonaws.com/bucket-name/path/to/file
        """
        if s3_url.startswith('s3://'):
            # 处理s3://bucket-name/key格式
            parts = s3_url.replace('s3://', '').split('/', 1)
            self.bucket_name = parts[0]
            self.key = parts[1] if len(parts) > 1 else ''
        elif 's3.amazonaws.com' in s3_url:
            # 处理https://bucket-name.s3.region.amazonaws.com/key格式
            parsed_url = urllib.parse.urlparse(s3_url)
            self.bucket_name = parsed_url.netloc.split('.')[0]
            self.key = parsed_url.path.lstrip('/')
        elif 's3-' in s3_url and '.amazonaws.com' in s3_url:
            # 处理https://s3-region.amazonaws.com/bucket-name/key格式
            parsed_url = urllib.parse.urlparse(s3_url)
            path_parts = parsed_url.path.lstrip('/').split('/', 1)
            self.bucket_name = path_parts[0]
            self.key = path_parts[1] if len(path_parts) > 1 else ''
        else:
            raise ValueError("无法识别的S3 URL格式。请使用以下格式之一：\n"
                           "- s3://bucket-name/path/to/file\n"
                           "- https://bucket-name.s3.region.amazonaws.com/path/to/file\n"
                           "- https://s3-region.amazonaws.com/bucket-name/path/to/file")

        return self.bucket_name, self.key

    def _initialize_s3_client(self):
        """初始化S3客户端"""
        client_kwargs = {}

        if self.region:
            client_kwargs['region_name'] = self.region

        # 匿名访问模式
        if self.anonymous:
            print("使用匿名访问模式...")
            client_kwargs['config'] = Config(signature_version=UNSIGNED)
            self.s3_client = boto3.client('s3', **client_kwargs)
            return self.s3_client

        # 认证访问模式
        if self.profile_name:
            session = boto3.Session(profile_name=self.profile_name)
            self.s3_client = session.client('s3', **client_kwargs)
        elif self.access_key and self.secret_key:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
            self.s3_client = session.client('s3', **client_kwargs)
        else:
            # 尝试使用默认凭证，失败则自动切换到匿名模式
            try:
                self.s3_client = boto3.client('s3', **client_kwargs)
                # 测试连接
                self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.key, MaxKeys=1)
            except Exception as e:
                print(f"无法使用默认凭证: {str(e)}")
                print("自动切换到匿名访问模式...")
                client_kwargs['config'] = Config(signature_version=UNSIGNED)
                self.s3_client = boto3.client('s3', **client_kwargs)

        return self.s3_client

    def _check_key_type(self):
        """检查指定的key是文件还是文件夹"""
        try:
            # 尝试获取对象元数据
            self.s3_client.head_object(Bucket=self.bucket_name, Key=self.key)
            self.download_type = 'file'
            return 'file'
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                # 如果key不存在作为文件，检查是否可能是文件夹
                self.download_type = 'folder'
                return 'folder'
            else:
                raise

    def _count_folder_files(self, bucket, prefix):
        """计算文件夹中的文件总数"""
        count = 0
        paginator = self.s3_client.get_paginator('list_objects_v2')

        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if self.interrupted:
                return count
            if 'Contents' in page:
                # 排除目录本身
                files = [obj for obj in page['Contents'] if not obj['Key'].endswith('/')]
                count += len(files)

        return count

    def _download_single_item(self, bucket, key, local_path):
        """下载单个文件到指定路径"""
        try:
            # 检查是否被中断
            if self.interrupted:
                return False

            # 确保目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # 下载文件
            self.s3_client.download_file(bucket, key, local_path)

            # 更新进度统计
            with self.lock:
                self.downloaded_files += 1
                if self.progress_bar:
                    self.progress_bar.update(1)

            return True
        except Exception as e:
            if not self.interrupted:
                print(f"下载文件 {key} 时出错: {str(e)}")
            return False

    def _download_file(self):
        """下载单个文件"""
        print(f"开始下载单个文件: s3://{self.bucket_name}/{self.key}")

        # 确定本地保存路径
        if self.keep_structure:
            local_path = os.path.join(self.output_dir, self.key)
        else:
            filename = os.path.basename(self.key)
            local_path = os.path.join(self.output_dir, filename)

        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"保存到: {local_path}")

        try:
            # 获取文件大小用于进度条
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=self.key)
            file_size = response['ContentLength']

            # 创建进度条
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='下载进度') as pbar:
                def callback(chunk):
                    if self.interrupted:
                        raise Exception("下载已被中断")
                    pbar.update(chunk)

                self.s3_client.download_file(
                    self.bucket_name, self.key, local_path,
                    Callback=callback
                )
        except Exception as e:
            if self.interrupted:
                print("\n下载被中断")
                return False
            # 如果无法获取文件大小，使用简单进度提示
            print("下载中...")
            self.s3_client.download_file(self.bucket_name, self.key, local_path)

        if not self.interrupted:
            print(f"下载完成! 文件已保存到 {local_path}")
            return True
        return False

    def _download_folder(self):
        """下载整个文件夹"""
        print(f"开始下载文件夹: s3://{self.bucket_name}/{self.key}")
        print(f"保存到: {self.output_dir}")

        if self.keep_structure:
            print("将保留完整的目录结构")
        else:
            print("将只保留相对路径")

        # 计算文件总数
        print("正在计算文件总数...")
        self.total_files = self._count_folder_files(self.bucket_name, self.key)

        if self.interrupted:
            return False

        print(f"找到 {self.total_files} 个文件需要下载")

        if self.total_files == 0:
            print("指定的路径中没有找到文件")
            return False

        # 创建进度条
        self.progress_bar = tqdm(total=self.total_files, unit='files', desc='下载进度')

        # 并发下载
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        download_tasks = []

        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.key):
                if self.interrupted:
                    break

                if 'Contents' in page:
                    for obj in page['Contents']:
                        if self.interrupted:
                            break

                        file_key = obj['Key']

                        # 跳过目录
                        if file_key.endswith('/'):
                            continue

                        # 计算本地保存路径
                        if self.keep_structure:
                            local_path = os.path.join(self.output_dir, file_key)
                        else:
                            relative_path = file_key[len(self.key):] if self.key else file_key
                            relative_path = relative_path.lstrip('/')
                            local_path = os.path.join(self.output_dir, relative_path)

                        # 提交下载任务
                        future = self.executor.submit(
                            self._download_single_item,
                            self.bucket_name,
                            file_key,
                            local_path
                        )
                        download_tasks.append(future)

            # 等待所有任务完成
            for future in as_completed(download_tasks):
                if self.interrupted:
                    break
                try:
                    future.result()
                except Exception as e:
                    if not self.interrupted:
                        print(f"任务执行出错: {str(e)}")

        except Exception as e:
            if not self.interrupted:
                print(f"下载过程中出错: {str(e)}")
            return False
        finally:
            # 关闭线程池
            self.executor.shutdown(wait=True)

            # 关闭进度条
            if self.progress_bar:
                self.progress_bar.close()

        if not self.interrupted:
            print(f"下载完成! 成功下载了 {self.downloaded_files}/{self.total_files} 个文件到 {self.output_dir}")
            return True
        else:
            print(f"下载被中断! 已下载 {self.downloaded_files}/{self.total_files} 个文件到 {self.output_dir}")
            return False

    def download(self):
        """
        执行下载操作
        自动检测是下载单个文件还是文件夹
        """
        try:
            # 解析S3链接
            if not self.bucket_name or self.key is None:
                self._parse_s3_url(self.s3_url)

            # 初始化S3客户端
            if not self.s3_client:
                self._initialize_s3_client()

            # 检查下载类型
            download_type = self._check_key_type()

            # 根据类型执行相应的下载操作
            if download_type == 'file':
                return self._download_file()
            else:
                return self._download_folder()

        except Exception as e:
            if not self.interrupted:
                print(f"下载过程中出错: {str(e)}")
            if self.progress_bar:
                self.progress_bar.close()
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='下载AWS S3文件夹中的所有文件或单个文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s s3://bucket-name/file.txt
  %(prog)s https://bucket-name.s3.amazonaws.com/folder/ -a
  %(prog)s s3://bucket/folder/ -o /local/path -k

提示:
  - 按 Ctrl+C 可中断下载并安全退出
        """
    )

    parser.add_argument('s3_url', help='S3链接，支持文件或文件夹')
    parser.add_argument('--profile', '-p', help='AWS配置文件名称')
    parser.add_argument('--access-key', '-ak', help='AWS访问密钥ID')
    parser.add_argument('--secret-key', '-sk', help='AWS秘密访问密钥')
    parser.add_argument('--region', '-r', help='AWS区域')
    parser.add_argument('--output-dir', '-o', help='本地输出目录，默认为当前目录')
    parser.add_argument('--max-workers', '-w', type=int, default=5, help='最大并发下载线程数，默认5')
    parser.add_argument('--anonymous', '-a', action='store_true', help='使用匿名访问（用于公开存储桶）')
    parser.add_argument('--keep-structure', '-k', action='store_true', help='保留完整的目录结构（包含存储桶路径）')

    args = parser.parse_args()

    # 警告信息
    if args.profile and (args.access_key or args.secret_key):
        print("警告: 同时提供了配置文件和访问密钥，将优先使用访问密钥")

    # 创建下载器实例
    downloader = S3Downloader(
        s3_url=args.s3_url,
        profile_name=args.profile,
        access_key=args.access_key,
        secret_key=args.secret_key,
        region=args.region,
        output_dir=args.output_dir,
        max_workers=args.max_workers,
        anonymous=args.anonymous
    )

    # 设置保留目录结构标志
    downloader.keep_structure = args.keep_structure

    # 执行下载
    print("按 Ctrl+C 可随时中断下载并退出")
    success = downloader.download()

    # 根据下载结果设置退出代码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()