#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AWS S3文件夹下载器 (Generic S3 Downloader)
支持匿名访问公开存储桶 - 修复版
"""

import os
import re
import boto3
import argparse
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from botocore import UNSIGNED
from botocore.config import Config


class S3FolderDownloader:
    def __init__(self, s3_url=None, profile_name=None, access_key=None, secret_key=None,
                 region=None, output_dir=None, max_workers=10, anonymous=False):
        """
        初始化S3文件夹下载器

        参数:
            s3_url (str): S3链接，格式为 's3://bucket-name/folder/path/' 或 'https://bucket-name.s3.region.amazonaws.com/folder/path/'
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
        self.keep_structure = False  # 默认不保留完整结构
        self.bucket_name = None
        self.prefix = None
        self.s3_client = None
        self.lock = threading.Lock()
        self.total_files = 0
        self.downloaded_files = 0
        self.progress_bar = None

    def parse_s3_url(self, s3_url):
        """解析S3 URL以获取bucket名称和前缀"""
        if s3_url.startswith('s3://'):
            # 处理s3://bucket-name/key格式
            parts = s3_url.replace('s3://', '').split('/', 1)
            self.bucket_name = parts[0]
            self.prefix = parts[1] if len(parts) > 1 else ''
        elif 's3.amazonaws.com' in s3_url:
            # 处理https://bucket-name.s3.region.amazonaws.com/key格式
            parsed_url = urllib.parse.urlparse(s3_url)
            self.bucket_name = parsed_url.netloc.split('.')[0]
            self.prefix = parsed_url.path.lstrip('/')
        elif 's3-' in s3_url and '.amazonaws.com' in s3_url:
            # 处理https://s3-region.amazonaws.com/bucket-name/key格式
            parsed_url = urllib.parse.urlparse(s3_url)
            path_parts = parsed_url.path.lstrip('/').split('/', 1)
            self.bucket_name = path_parts[0]
            self.prefix = path_parts[1] if len(path_parts) > 1 else ''
        else:
            raise ValueError("无法识别的S3 URL格式。请使用以下格式之一：\n"
                           "- s3://bucket-name/folder/path/\n"
                           "- https://bucket-name.s3.region.amazonaws.com/folder/path/\n"
                           "- https://s3-region.amazonaws.com/bucket-name/folder/path/")

        # 确保前缀以斜杠结尾（如果有前缀）
        if self.prefix and not self.prefix.endswith('/'):
            self.prefix += '/'

        return self.bucket_name, self.prefix

    def initialize_s3_client(self):
        """初始化S3客户端"""
        client_kwargs = {}

        if self.region:
            client_kwargs['region_name'] = self.region

        # 如果指定了匿名访问，使用UNSIGNED配置
        if self.anonymous:
            print("使用匿名访问模式...")
            # 使用UNSIGNED签名，这是正确的匿名访问方式
            client_kwargs['config'] = Config(signature_version=UNSIGNED)
            self.s3_client = boto3.client('s3', **client_kwargs)
            return self.s3_client

        # 否则按正常流程尝试认证
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
            # 尝试使用默认凭证，如果失败则自动尝试匿名访问
            try:
                self.s3_client = boto3.client('s3', **client_kwargs)
                # 测试连接
                self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.prefix, MaxKeys=1)
            except Exception as e:
                print(f"无法使用默认凭证: {str(e)}")
                print("自动切换到匿名访问模式...")

                # 使用UNSIGNED配置进行匿名访问
                client_kwargs['config'] = Config(signature_version=UNSIGNED)
                self.s3_client = boto3.client('s3', **client_kwargs)

        return self.s3_client

    def count_files(self, bucket, prefix):
        """计算需要下载的文件总数"""
        count = 0
        paginator = self.s3_client.get_paginator('list_objects_v2')

        # 遍历所有页面
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if 'Contents' in page:
                # 排除目录本身和空目录
                files = [obj for obj in page['Contents'] if not obj['Key'].endswith('/')]
                count += len(files)

        return count

    def download_file(self, bucket, key, local_path):
        """下载单个文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # 下载文件
            self.s3_client.download_file(bucket, key, local_path)

            # 更新进度条
            with self.lock:
                self.downloaded_files += 1
                if self.progress_bar:
                    self.progress_bar.update(1)

            return True
        except Exception as e:
            print(f"下载文件 {key} 时出错: {str(e)}")
            return False

    def download_folder(self):
        """下载整个文件夹"""
        try:
            # 解析S3链接
            if not self.bucket_name or not self.prefix:
                self.parse_s3_url(self.s3_url)

            # 初始化S3客户端
            if not self.s3_client:
                self.initialize_s3_client()

            print(f"开始从 s3://{self.bucket_name}/{self.prefix} 下载文件到 {self.output_dir}")
            if self.keep_structure:
                print("将保留完整的目录结构")
            else:
                print("将只下载指定前缀下的文件")

            # 计算文件总数用于进度显示
            print("正在计算文件总数...")
            self.total_files = self.count_files(self.bucket_name, self.prefix)
            print(f"找到 {self.total_files} 个文件需要下载")

            if self.total_files == 0:
                print("指定的S3路径中没有找到文件")
                return

            # 创建进度条
            self.progress_bar = tqdm(total=self.total_files, unit='files')

            # 获取所有对象
            paginator = self.s3_client.get_paginator('list_objects_v2')
            download_tasks = []

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 遍历所有页面
                for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix):
                    if 'Contents' in page:
                        for obj in page['Contents']:
                            key = obj['Key']

                            # 跳过目录本身
                            if key.endswith('/'):
                                continue

                            # 根据keep_structure标志决定路径处理方式
                            if self.keep_structure:
                                # 保留完整的路径结构
                                local_path = os.path.join(self.output_dir, key)
                            else:
                                # 只保留相对于指定前缀的路径
                                relative_path = key[len(self.prefix):] if self.prefix else key
                                local_path = os.path.join(self.output_dir, relative_path)

                            # 提交下载任务
                            download_tasks.append(
                                executor.submit(
                                    self.download_file,
                                    self.bucket_name,
                                    key,
                                    local_path
                                )
                            )

            # 关闭进度条
            if self.progress_bar:
                self.progress_bar.close()

            print(f"下载完成! 成功下载了 {self.downloaded_files}/{self.total_files} 个文件到 {self.output_dir}")

        except Exception as e:
            print(f"下载过程中出错: {str(e)}")
            if self.progress_bar:
                self.progress_bar.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='下载AWS S3文件夹中的所有文件')
    parser.add_argument('s3_url', help='S3链接，例如 s3://bucket-name/folder/ 或 https://bucket-name.s3.region.amazonaws.com/folder/')
    parser.add_argument('--profile', '-p', help='AWS配置文件名称')
    parser.add_argument('--access-key', '-ak', help='AWS访问密钥ID')
    parser.add_argument('--secret-key', '-sk', help='AWS秘密访问密钥')
    parser.add_argument('--region', '-r', help='AWS区域')
    parser.add_argument('--output-dir', '-o', help='本地输出目录，默认为当前目录')
    parser.add_argument('--max-workers', '-w', type=int, default=5, help='最大并发下载线程数，默认5')
    parser.add_argument('--anonymous', '-a', action='store_true', help='使用匿名访问（用于公开存储桶）')
    parser.add_argument('--keep-structure', '-k', action='store_true', help='保留完整的目录结构（包含存储桶路径）')

    args = parser.parse_args()

    # 如果同时提供了profile和access/secret key，使用access/secret key
    if args.profile and (args.access_key or args.secret_key):
        print("警告: 同时提供了配置文件和访问密钥，将优先使用访问密钥")

    # 初始化下载器
    downloader = S3FolderDownloader(
        s3_url=args.s3_url,
        profile_name=args.profile,
        access_key=args.access_key,
        secret_key=args.secret_key,
        region=args.region,
        output_dir=args.output_dir,
        max_workers=args.max_workers,
        anonymous=args.anonymous
    )

    # 如果指定了保留目录结构，设置标志位
    if args.keep_structure:
        downloader.keep_structure = True
    else:
        downloader.keep_structure = False

    # 开始下载
    downloader.download_folder()


if __name__ == "__main__":
    main()