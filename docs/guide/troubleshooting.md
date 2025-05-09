# 故障排除

本页面提供了使用G3SD工具时可能遇到的常见问题和解决方案。

## 认证相关问题

### Unable to locate credentials

**问题描述**：
```
下载过程中出错: Unable to locate credentials
```

**解决方案**：
1. 对于公开存储桶，使用`--anonymous`或`-a`参数：
   ```bash
   python G3SD.py s3://public-bucket/folder/ --anonymous
   ```

2. 如果确定需要认证，请提供凭证：
   - 使用AWS配置文件：`--profile your-profile`
   - 直接提供密钥：`--access-key YOUR_KEY --secret-key YOUR_SECRET`
   - 设置环境变量：AWS_ACCESS_KEY_ID和AWS_SECRET_ACCESS_KEY

### AuthorizationHeaderMalformed

**问题描述**：
```
下载过程中出错: An error occurred (AuthorizationHeaderMalformed) when calling the ListObjectsV2 operation: The authorization header is malformed; a non-empty Access Key (AKID) must be provided in the credential.
```

**解决方案**：
当使用匿名访问时出现此错误，说明匿名访问配置不正确。确保使用了正确的匿名访问方式：
```bash
python G3SD.py s3://public-bucket/folder/ --anonymous
```

这个问题已在最新版本中修复，通过使用`botocore.UNSIGNED`配置。

## 访问相关问题

### Access Denied

**问题描述**：
```
下载过程中出错: An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```

**解决方案**：
1. 确认存储桶确实是公开的，如果不确定，请尝试使用AWS凭证
2. 检查存储桶名称和路径是否正确
3. 尝试指定正确的AWS区域：
   ```bash
   python G3SD.py s3://my-bucket/folder/ --anonymous --region us-east-1
   ```

### NoSuchBucket

**问题描述**：
```
下载过程中出错: An error occurred (NoSuchBucket) when calling the ListObjectsV2 operation: The specified bucket does not exist
```

**解决方案**：
1. 检查存储桶名称是否拼写正确
2. 确认存储桶仍然存在（公开数据集有时会被移除）
3. 如果是使用HTTPS URL格式，尝试改用s3://格式

### PermanentRedirect

**问题描述**：
```
下载过程中出错: An error occurred (PermanentRedirect) when calling the ListObjectsV2 operation: The bucket you are attempting to access must be addressed using the specified endpoint.
```

**解决方案**：
该存储桶在不同的区域，请使用`--region`参数指定正确的区域：
```bash
python G3SD.py s3://my-bucket/folder/ --region us-west-2
```

尝试常见区域：`us-east-1`, `us-west-2`, `eu-west-1`, `ap-northeast-1`

## 目录结构问题

### 文件下载到错误位置

**问题描述**：
文件未按预期的目录结构下载。

**解决方案**：
1. 默认情况下，工具只会保留相对于指定前缀的路径
2. 如果需要保留完整路径，请使用`--keep-structure`或`-k`参数：
   ```bash
   python G3SD.py s3://my-bucket/deep/nested/folder/ --output-dir ./downloads --keep-structure
   ```

### 指定的S3路径中没有找到文件

**问题描述**：
```
指定的S3路径中没有找到文件
```

**解决方案**：
1. 确保S3路径正确，注意大小写（S3是区分大小写的）
2. 如果路径是一个目录，确保末尾有斜杠
3. 尝试列出上层目录的内容，以确认正确的路径
4. 确认你有权限访问该路径下的内容

## 性能相关问题

### 下载速度慢

**问题描述**：
下载速度比预期慢很多。

**解决方案**：
1. 增加并发下载线程数：
   ```bash
   python G3SD.py s3://my-bucket/folder/ --max-workers 30
   ```
2. 确认网络连接稳定且带宽充足
3. 对于大量小文件，提高线程数可能有帮助
4. 对于少量大文件，请确保网络稳定性

### 内存占用过高

**问题描述**：
工具运行时内存使用过多。

**解决方案**：
1. 减少并发下载线程数：
   ```bash
   python G3SD.py s3://my-bucket/folder/ --max-workers 5
   ```
2. 分批下载大型目录，而不是一次下载所有文件

## 网络相关问题

### 连接断开或超时

**问题描述**：
在长时间下载过程中出现连接断开或超时错误。

**解决方案**：
1. 确保网络连接稳定
2. 减少并发下载线程数以降低网络压力
3. 分批下载，而不是一次下载大量文件
4. 对于不稳定的网络，可能需要多次运行工具来完成下载

### 代理环境问题

**问题描述**：
在使用代理的网络环境中无法连接AWS S3。

**解决方案**：
设置HTTP和HTTPS代理环境变量：

```bash
# 在Linux/macOS上
export HTTP_PROXY=http://proxy.example.com:port
export HTTPS_PROXY=http://proxy.example.com:port

# 在Windows上
set HTTP_PROXY=http://proxy.example.com:port
set HTTPS_PROXY=http://proxy.example.com:port
```

## 脚本相关问题

### 运行时找不到模块

**问题描述**：
```
ModuleNotFoundError: No module named 'boto3'
```

**解决方案**：
安装所需的Python库：
```bash
pip install boto3 tqdm
```

### 权限错误

**问题描述**：
无法创建输出目录或写入文件。

**解决方案**：
1. 确保你有写入指定输出目录的权限
2. 尝试使用不同的输出目录
3. 在Windows上，可能需要以管理员身份运行命令提示符

## 获取更多帮助

如果你遇到的问题未在此页面列出，或者提供的解决方案未能解决你的问题，可以：

1. 检查命令行帮助信息：
   ```bash
   python G3SD.py --help
   ```

2. 启用AWS SDK详细日志进行诊断：
   ```bash
   # 在Windows上
   set AWS_SDK_LOGGING=1
   python G3SD.py ...
   ```

3. 提交问题到GitHub仓库