# 快速开始

本指南将帮助你快速上手GS3D下载工具，从安装到运行你的第一个下载命令。

## 安装

### 前置条件

在开始之前，确保你的系统已安装：

- Python 3.6 或更高版本
- pip（Python包管理器）

你可以通过以下命令检查Python版本：

```bash
python --version
```

### 安装依赖

G3SD下载工具依赖于两个主要的Python库：

```bash
pip install boto3 tqdm
```

- **boto3**: AWS Python SDK，用于与S3服务交互
- **tqdm**: 提供进度条功能，直观显示下载进度

### 获取脚本

你可以通过以下方式获取S3下载工具脚本：

1. 从GitHub下载 (推荐)：
   ```bash
   git clone https://github.com/yourusername/G3SD.git
   cd G3SD
   ```

2. 或者直接下载单个脚本文件：
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/G3SD/main/G3SD.py
   ```

## 基本使用

### 下载公开存储桶中的文件

要从公开存储桶下载文件，使用`--anonymous`或`-a`参数：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous
```

### 指定下载目录

使用`--output-dir`或`-o`参数指定下载目录：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous --output-dir ./downloads
```

### 保留目录结构

如果你想保留完整的S3目录结构，添加`--keep-structure`或`-k`参数：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous --output-dir ./downloads --keep-structure
```

## 认证方式

### 使用AWS配置文件

如果你已经配置了AWS凭证，可以使用配置文件：

```bash
python G3SD.py s3://my-bucket/folder/ --profile my-profile-name
```

### 使用访问密钥

或者直接提供AWS访问密钥：

```bash
python G3SD.py s3://my-bucket/folder/ --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY
```

## 常见问题排查

### 无法访问存储桶

如果遇到访问错误，请确认：

1. 对于公开存储桶，使用`--anonymous`参数
2. 尝试指定正确的AWS区域，例如：`--region us-east-1`
3. 对于私有存储桶，确保提供了正确的凭证

### 下载速度慢

如果下载速度不理想，可以调整并发下载线程数：

```bash
python G3SD.py s3://my-bucket/folder/ --max-workers 20
```

## 下一步

现在你已经了解了S3下载工具的基本用法，可以继续探索更多高级功能：

- [基本用法](/guide/basic-usage) - 详细的命令行参数说明
- [匿名访问](/guide/anonymous-access) - 深入了解如何访问公开存储桶
- [目录结构保留](/guide/keep-structure) - 关于目录结构管理的详细说明
- [高级选项](/guide/advanced-options) - 探索更多自定义选项