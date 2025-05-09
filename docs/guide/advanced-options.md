# 高级选项

除了基本用法外，GS3D下载工具还提供了一系列高级选项，让你可以更灵活地控制下载过程。本页面将详细介绍这些高级功能。

## 性能调优

### 并发下载线程数

使用`--max-workers`或`-w`参数可以调整并发下载线程数：

```bash
python GS3D.py s3://my-bucket/folder/ --max-workers 20
```

**最佳实践**：
- 对于大量小文件，增加线程数可以提高吞吐量（如15-30线程）
- 对于少量大文件，减少线程数可以提高稳定性（如5-10线程）
- 对于网络条件不佳的环境，较少的线程可能更可靠
- 根据你的系统资源（CPU、内存、网络带宽）调整此值# 高级选项

除了基本用法外，GS3D下载工具还提供了一系列高级选项，让你可以更灵活地控制下载过程。本页面将详细介绍这些高级功能。

## 性能调优

### 并发下载线程数

使用`--max-workers`或`-w`参数可以调整并发下载线程数：

```bash
python s3_folder_downloader.py s3://my-bucket/folder/ --max-workers 20
```

**最佳实践**：
- 对于大量小文件，增加线程数可以提高吞吐量（如15-30线程）
- 对于少量大文件，减少线程数可以提高稳定性（如5-10线程）
- 对于网络条件不佳的环境，较少的线程可能更可靠
- 根据你的系统资源（CPU、内存、网络带宽）调整此值

## AWS特定选项

### 区域指定

某些S3存储桶严格要求在特定区域访问，可以使用`--region`参数明确指定：

```bash
python GS3D.py s3://my-bucket/folder/ --region us-west-2
```

常见的AWS区域代码：
- `us-east-1`: 美国东部（弗吉尼亚北部）
- `us-west-2`: 美国西部（俄勒冈）
- `eu-west-1`: 欧洲（爱尔兰）
- `ap-northeast-1`: 亚太地区（东京）

### 使用特定的端点URL

在某些特殊情况下，你可能需要连接到自定义的S3兼容端点。这可以通过环境变量来实现：

```bash
# 在Linux/macOS上
export AWS_ENDPOINT_URL=https://custom-endpoint.example.com

# 在Windows上
set AWS_ENDPOINT_URL=https://custom-endpoint.example.com

# 然后运行下载工具
python GS3D.py s3://my-bucket/folder/
```

## 路径和输出控制

### URL编码处理

S3对象键（路径）可能包含特殊字符，工具会自动处理URL编码/解码。如果文件名包含特殊字符，它们会被正确下载和保存。

### 处理同名文件

当本地已存在同名文件时，脚本会覆盖现有文件。未来版本可能会添加跳过或重命名的选项。

## 调试和排错选项

### 添加详细日志

如果你需要更详细的输出来诊断问题，可以设置环境变量启用更详细的日志：

```bash
# 在Linux/macOS上
export AWS_SDK_LOGGING=1

# 在Windows上
set AWS_SDK_LOGGING=1
```

这将启用boto3库的详细日志记录，帮助诊断连接或权限问题。

### 错误处理

GS3D下载工具会在下载过程中遇到错误时继续执行，并在完成时汇总成功/失败的文件数量。这确保了单个文件的失败不会中断整个批量下载过程。

## 组合多个选项

你可以组合多个高级选项来满足特定需求：

```bash
python GS3D.py s3://my-bucket/folder/ \
  --profile production \
  --region eu-west-1 \
  --output-dir ./data-backup \
  --max-workers 15 \
  --keep-structure
```

## 脚本集成

GS3D下载工具可以轻松集成到其他Python脚本中，通过导入`S3FolderDownloader`类：

```python
from GS3D import S3FolderDownloader

downloader = S3FolderDownloader(
    s3_url="s3://my-bucket/folder/",
    output_dir="./downloads",
    max_workers=15,
    anonymous=True
)

downloader.download_folder()
```

这种方式允许你在更大的应用程序中使用S3下载功能，或者根据需要自定义行为。

## 未来计划功能

以下是计划在将来版本中添加的高级功能：

- 支持断点续传
- 下载前显示文件列表和总大小
- 文件过滤器（按文件名、大小、日期等）
- 跳过已存在的文件选项
- 下载限速选项

如果你有其他功能建议，欢迎提交议题或拉取请求到GitHub仓库。