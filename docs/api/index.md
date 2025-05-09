# API参考

本页面详细介绍GS3D工具的命令行参数和选项。

## 命令行参数

GS3D支持以下命令行参数：

| 参数 | 短格式 | 类型 | 默认值 | 描述 |
|------|-------|------|-------|------|
| `s3_url` | - | 字符串 | (必需) | S3链接，例如s3://bucket-name/folder/ |
| `--profile` | `-p` | 字符串 | None | AWS配置文件名称 |
| `--access-key` | `-ak` | 字符串 | None | AWS访问密钥ID |
| `--secret-key` | `-sk` | 字符串 | None | AWS秘密访问密钥 |
| `--region` | `-r` | 字符串 | None | AWS区域 |
| `--output-dir` | `-o` | 字符串 | 当前目录 | 本地输出目录 |
| `--max-workers` | `-w` | 整数 | 10 | 最大并发下载线程数 |
| `--anonymous` | `-a` | 标志 | False | 使用匿名访问模式（用于公开存储桶） |
| `--keep-structure` | `-k` | 标志 | False | 保留完整的目录结构 |

## 使用语法

基本语法：

```bash
python GS3D.py S3链接 [选项]
```

S3链接是唯一必需的参数，可以是以下格式之一：
- `s3://bucket-name/folder/path/`
- `https://bucket-name.s3.region.amazonaws.com/folder/path/`
- `https://s3-region.amazonaws.com/bucket-name/folder/path/`

## 参数详解

### S3链接

指定要下载的S3存储桶和前缀（文件夹路径）。这是唯一必需的参数。

例如：
```bash
python GS3D.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/
```

### --profile / -p

指定AWS配置文件名称。如果你有多个AWS配置文件，可以使用此参数选择要使用的配置文件。

例如：
```bash
python GS3D.py s3://my-bucket/folder/ --profile work
```

### --access-key / -ak 和 --secret-key / -sk

直接提供AWS访问密钥和秘密访问密钥，而不使用配置文件。

例如：
```bash
python GS3D.py s3://my-bucket/folder/ --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY
```

### --region / -r

指定AWS区域。某些S3存储桶需要在特定区域访问。

例如：
```bash
python GS3D.py s3://my-bucket/folder/ --region us-east-1
```

常见的AWS区域代码：
- `us-east-1`: 美国东部（弗吉尼亚北部）
- `us-west-2`: 美国西部（俄勒冈）
- `eu-west-1`: 欧洲（爱尔兰）
- `ap-northeast-1`: 亚太地区（东京）

### --output-dir / -o

指定文件下载的本地目录。如果不指定，文件将下载到当前工作目录。

例如：
```bash
python GS3D.py s3://my-bucket/folder/ --output-dir ./downloads
```

### --max-workers / -w

调整并发下载线程数。默认值为10。对于大量小文件，增加此值可提高下载速度；对于少量大文件，可能需要减小此值以保持稳定性。

例如：
```bash
python GS3D.py s3://my-bucket/folder/ --max-workers 20
```

### --anonymous / -a

启用匿名访问模式，无需AWS凭证即可访问公开存储桶。

例如：
```bash
python GS3D.py s3://public-bucket/folder/ --anonymous
```

### --keep-structure / -k

保留完整的S3目录结构。默认情况下，工具只会保留相对于指定前缀的路径结构。使用此参数可以保留完整路径。

例如：
```bash
python GS3D.py s3://my-bucket/deep/nested/folder/ --keep-structure
```

## 返回值

GS3D工具在成功执行时返回退出代码0，在遇到错误时返回非零退出代码。

## 示例组合

以下是一些常用的参数组合示例：

### 匿名访问公开数据集并保留目录结构

```bash
python GS3D.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --region us-east-1 --output-dir ./climate-data --keep-structure
```

### 使用AWS配置文件访问私有存储桶并增加并发线程数

```bash
python GS3D.py s3://my-private-bucket/important-data/ --profile production --output-dir ./backup --max-workers 25
```

### 同时使用多个选项

```bash
python GS3D.py s3://my-bucket/folder/ \
  --profile development \
  --region eu-west-1 \
  --output-dir ./downloads \
  --max-workers 15 \
  --keep-structure
```