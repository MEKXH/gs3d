---
layout: home
hero:
  name: G3SD
  text: 通用AWS S3下载工具
  tagline: 轻松下载AWS S3存储桶内容的Python工具
  image:
    src: /logo.svg
    alt: G3SD Logo
  actions:
    - theme: brand
      text: 快速开始
      link: /introduction/getting-started
    - theme: alt
      text: 查看源码
      link: https://github.com/yourusername/G3SD
features:
  - icon: 🚀
    title: 高效下载
    details: 多线程并行下载，最大限度提升下载速度
  - icon: 🔒
    title: 支持匿名访问
    details: 无需AWS凭证即可访问公开存储桶
  - icon: 🧩
    title: 灵活配置
    details: 丰富的命令行选项，满足各种下载需求
  - icon: 📁
    title: 目录结构管理
    details: 灵活选择保留完整目录结构或仅保留文件
  - icon: 📊
    title: 实时进度显示
    details: 直观的进度条，随时了解下载状态
  - icon: 🔧
    title: 易于安装
    details: 简单的依赖要求，轻松安装和使用
---

# AWS S3文件夹下载工具

G3SD（Generic S3 Downloader）是一个强大而简单的Python工具，专为从AWS S3存储桶下载文件而设计。无论是公开数据集还是私有内容，G3SD都能帮助您轻松获取所需文件。

## 主要功能

- **轻松下载** - 简单的命令行界面，只需提供S3链接即可
- **匿名访问** - 无需AWS凭证即可访问公开存储桶
- **目录结构管理** - 灵活选择是否保留完整的S3目录结构
- **多线程并行下载** - 显著提高下载速度
- **实时进度显示** - 直观了解下载进度
- **自动创建目录** - 自动在本地创建必要的目录结构

## 快速开始

安装依赖：

```bash
pip install boto3 tqdm
```

下载公开存储桶：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous
```

保留目录结构：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous --keep-structure
```

## 为什么选择G3SD？

与AWS CLI的`aws s3 sync`命令相比，G3SD提供了：

- 更简单的命令行界面
- 内置的匿名访问支持
- 灵活的目录结构管理选项
- 直观的进度显示
- 无需完整AWS CLI安装

## 适用场景

G3SD特别适用于：

- 下载科研数据集（如GEOS-Chem气候数据）
- 从公开S3存储桶获取资源
- 备份项目文件
- 在AWS EC2实例上访问S3存储桶内容

## 立即开始使用

点击[快速开始](/introduction/getting-started)了解更多，或查看[基本用法](/guide/basic-usage)获取详细指南。

---

<div class="footer-message">
G3SD是一个开源项目，遵循MIT许可证，欢迎贡献和改进。
</div>