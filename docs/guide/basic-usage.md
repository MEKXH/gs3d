# 基本用法

GS3D下载工具提供了简单直观的命令行界面，让你可以轻松地从AWS S3存储桶下载文件。本页面介绍工具的基本用法和主要命令行参数。

## 命令格式

S3下载工具的基本命令格式如下：

```bash
python G3SD.py S3链接 [选项]
```

S3链接是唯一必需的参数，它指定了你要下载的S3存储桶和前缀（文件夹路径）。

## S3链接格式

工具支持以下几种S3链接格式：

1. `s3://bucket-name/folder/path/`
2. `https://bucket-name.s3.region.amazonaws.com/folder/path/`
3. `https://s3-region.amazonaws.com/bucket-name/folder/path/`

例如：
```bash
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/
```

## 主要参数

以下是最常用的命令行参数：

### 输出目录

使用`--output-dir`或`-o`参数指定文件下载的本地目录：

```bash
python G3SD.py s3://my-bucket/folder/ --output-dir ./downloads
```

如果不指定输出目录，文件将下载到当前工作目录。

### 匿名访问

对于公开的S3存储桶，使用`--anonymous`或`-a`参数进行匿名访问：

```bash
python G3SD.py s3://public-bucket/folder/ --anonymous
```

这样无需提供AWS凭证即可下载公开存储桶中的文件。

### 目录结构保留

使用`--keep-structure`或`-k`参数保留完整的S3目录结构：

```bash
python G3SD.py s3://my-bucket/folder/ --keep-structure
```

默认情况下，工具只会保留相对于指定前缀的路径结构。使用此参数可以保留完整路径。

### 并发下载线程数

使用`--max-workers`或`-w`参数调整并发下载线程数：

```bash
python G3SD.py s3://my-bucket/folder/ --max-workers 20
```

默认值为10。对于大量小文件，增加此值可提高下载速度；对于少量大文件，可能需要减小此值以保持稳定性。

### AWS区域

使用`--region`或`-r`参数指定AWS区域：

```bash
python G3SD.py s3://my-bucket/folder/ --region us-east-1
```

## 认证选项

S3下载工具支持多种认证方式：

### AWS配置文件

使用`--profile`或`-p`参数指定AWS配置文件：

```bash
python G3SD.py s3://my-bucket/folder/ --profile my-profile
```

### 访问密钥

使用`--access-key`和`--secret-key`参数直接提供AWS访问密钥：

```bash
python G3SD.py s3://my-bucket/folder/ --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY
```

## 完整示例

以下是一些完整的使用示例：

### 基本下载

```bash
python G3SD.py s3://my-bucket/my-folder/ --output-dir ./downloads
```

### 匿名访问公开存储桶

```bash
python G3SD.py s3://public-dataset/folder/ --anonymous --region us-east-1 --output-dir ./data
```

### 保留目录结构并使用配置文件

```bash
python G3SD.py s3://my-bucket/deep/nested/folder/ --profile work --output-dir ./backup --keep-structure
```

### 调整并发下载设置

```bash
python G3SD.py s3://large-files-bucket/folder/ --max-workers 5 --output-dir ./large-files
```

## 参数总结

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