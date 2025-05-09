# GS3D - 通用S3下载工具

<p align="center">
  <img src="./docs/public/logo.svg" alt="GS3D Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/MEKXH/gs3d/releases"><img src="https://img.shields.io/github/v/release/MEKXH/gs3d" alt="发布版本"></a>
  <a href="https://github.com/MEKXH/gs3d/blob/master/LICENSE"><img src="https://img.shields.io/github/license/MEKXH/gs3d" alt="许可证"></a>
  <a href="https://github.com/MEKXH/gs3d/issues"><img src="https://img.shields.io/github/issues/MEKXH/gs3d" alt="问题"></a>
  <a href="https://mekxh.github.io/gs3d/"><img src="https://img.shields.io/badge/文档-在线-blue" alt="文档"></a>
</p>

[English](README.md)

## 简介

GS3D (Generic S3 Downloader) 是一个通用的Python工具，专为从AWS S3存储桶下载整个文件夹及其内容而设计。它提供了简单而强大的命令行界面，让用户能够轻松地从S3存储桶中检索文件。

### 核心功能

- **多线程并行下载**：利用多线程技术同时下载多个文件，显著提高下载速度
- **匿名访问支持**：无需AWS凭证即可访问公开存储桶
- **目录结构管理**：灵活选择是否保留完整S3目录结构
- **实时进度显示**：通过进度条直观显示下载进度
- **多种认证方式**：支持AWS配置文件、访问密钥和默认凭证

## 安装

### 前置条件

- Python 3.6+
- pip (Python包管理器)

### 安装依赖

```bash
pip install boto3 tqdm
```

### 获取GS3D

克隆此仓库或直接下载脚本文件：

```bash
git clone https://github.com/MEKXH/gs3d.git
cd gs3d
```

## 快速开始

### 基本用法

```bash
python GS3D.py s3://my-bucket/my-folder/ --output-dir ./downloads
```

### 下载公开存储桶内容

```bash
python GS3D.py s3://public-bucket/folder/ --anonymous
```

### 保留完整目录结构

```bash
python GS3D.py s3://my-bucket/folder/ --keep-structure --output-dir ./downloads
```

### 使用AWS配置文件

```bash
python GS3D.py s3://my-bucket/folder/ --profile my-profile-name
```

## 命令行参数

| 参数 | 短格式 | 说明 |
|------|-------|------|
| `s3_url` | - | S3链接 (必需) |
| `--profile` | `-p` | AWS配置文件名称 |
| `--access-key` | `-ak` | AWS访问密钥ID |
| `--secret-key` | `-sk` | AWS秘密访问密钥 |
| `--region` | `-r` | AWS区域 |
| `--output-dir` | `-o` | 本地输出目录，默认为当前目录 |
| `--max-workers` | `-w` | 最大并发下载线程数，默认为10 |
| `--anonymous` | `-a` | 使用匿名访问模式（用于公开存储桶） |
| `--keep-structure` | `-k` | 保留完整的目录结构 |

## 使用案例

### 下载GEOS-Chem气候数据

```bash
python GS3D.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --region us-east-1 --output-dir ./climate-data
```

### 备份项目资源

```bash
python GS3D.py s3://my-company/project-assets/ --profile work --output-dir ./backup --keep-structure
```

### 在AWS EC2实例上使用

在EC2实例上运行且已配置IAM角色时，无需提供凭证：

```bash
python GS3D.py s3://internal-data/reports/ --output-dir /mnt/data
```

## 文档

完整文档可在我们的[官方文档网站](https://mekxh.github.io/gs3d/)查看。

### 本地运行文档

如果你想在本地运行文档网站：

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm docs:dev
```

然后在浏览器中访问 `http://localhost:5173`。

### 文档部署

本项目提供了两个部署脚本，用于将文档部署到GitHub Pages：

#### 使用完整部署脚本 (推荐)

完整版脚本提供详细的日志和错误处理：

```powershell
.\scripts\deploy.ps1
```

#### 使用快速部署脚本

快速版脚本更为简洁，但需要提供仓库URL：

```powershell
.\scripts\quick-deploy.ps1 -RepoUrl "https://github.com/MEKXH/gs3d.git"
```

两个脚本都支持以下参数：
- `-RepoUrl`: GitHub仓库URL
- `-BranchName`: 部署分支名称 (默认: gh-pages)
- `-Force`: 强制推送 (覆盖远程历史)

## 项目结构

```
gs3d/
├── GS3D.py              # 主脚本文件
├── docs/                # 文档源文件
│   ├── .vitepress/      # VitePress配置
│   ├── public/          # 静态资源
│   ├── guide/           # 指南文档
│   ├── introduction/    # 介绍文档
│   ├── api/             # API参考
│   └── index.md         # 首页
├── scripts/             # 实用脚本
│   ├── deploy.ps1       # 完整部署脚本
│   └── quick-deploy.ps1 # 快速部署脚本
├── package.json         # 项目配置
└── README.md            # 项目说明
```

## 贡献指南

欢迎贡献！请随时提交问题或拉取请求。对于重大更改，请先开启一个issue讨论您想要更改的内容。

## 许可证

本项目采用 [MIT许可证](LICENSE) 发布。

## 致谢

- [boto3](https://github.com/boto/boto3) - 用于与AWS服务交互的Python SDK
- [tqdm](https://github.com/tqdm/tqdm) - 用于显示进度条
- [VitePress](https://vitepress.dev/) - 用于构建文档网站

## 联系方式

如有任何问题或建议，请[开启一个issue](https://github.com/MEKXH/gs3d/issues)

---