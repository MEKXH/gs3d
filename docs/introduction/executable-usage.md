# 使用可执行文件

GS3D 提供预编译的可执行文件，让您无需安装 Python 环境即可使用。

## 下载与安装

### 1. 下载可执行文件

访问 [Releases 页面](https://github.com/MEKXH/gs3d/releases/latest) 下载适合您系统的版本：

| 平台 | 架构 | 文件名 |
|------|------|--------|
| Windows | x64 | `gs3d-windows-x86_64.exe` |
| Linux | x64 | `gs3d-linux-x86_64` |
| macOS | - | 开发中，即将推出 |

### 2. 设置权限

#### Windows
无需额外设置，直接双击运行即可。

#### Linux
```bash
# 添加执行权限
chmod +x gs3d-linux-x86_64
```

### 3. 添加到 PATH（可选）

为了能在任何位置使用 `gs3d` 命令，您可以将可执行文件添加到系统 PATH：

#### Windows
1. 将 `gs3d-windows-x86_64.exe` 重命名为 `gs3d.exe`
2. 将文件移动到 `C:\tools\` 或任何您喜欢的目录
3. 将该目录添加到系统 PATH 环境变量

#### Linux
```bash
# 重命名并移动到 /usr/local/bin
sudo mv gs3d-linux-x86_64 /usr/local/bin/gs3d
sudo chmod +x /usr/local/bin/gs3d
```

## 使用示例

### 基本用法

```bash
# Windows
gs3d-windows-x86_64.exe https://bucket.s3.amazonaws.com/file.txt

# Linux
./gs3d-linux-x86_64 https://bucket.s3.amazonaws.com/file.txt
```

### 匿名访问公开存储桶

```bash
# 下载单个文件
gs3d https://geoschem.s3.amazonaws.com/PM25/AS.tar.gz -a

# 下载整个文件夹
gs3d s3://public-bucket/folder/ -a
```

### 指定输出目录

```bash
# 保存到指定目录
gs3d s3://bucket/file.txt -o /path/to/output/
```

### 保留目录结构

```bash
# 下载时保留完整的S3目录结构
gs3d s3://bucket/folder/ -k
```

### 调整并发下载数

```bash
# 使用10个并发线程下载
gs3d s3://bucket/folder/ -w 10
```

## 故障排除

### Windows 安全警告

首次运行时，Windows 可能显示安全警告。点击"更多信息"，然后选择"仍要运行"。

### Linux 权限问题

如果遇到权限问题：

```bash
# 确保有执行权限
chmod +x gs3d-linux-x86_64

# 或者以管理员身份运行
sudo ./gs3d-linux-x86_64 ...
```

## 验证下载

每个版本都提供 SHA256 校验和，您可以验证下载的完整性：

```bash
# 下载校验和文件
wget https://github.com/MEKXH/gs3d/releases/download/v1.0.0/checksums.txt

# Windows (PowerShell)
Get-FileHash gs3d-windows-x86_64.exe -Algorithm SHA256

# Linux
sha256sum gs3d-linux-x86_64
```

## 常见问题

### Q: 为什么文件很大？
A: 可执行文件包含了 Python 运行时和所有依赖库，因此体积较大（约 20-30MB）。

### Q: 能否减小文件大小？
A: 已经通过 UPX 压缩，进一步压缩可能影响兼容性。

### Q: 支持其他架构吗？
A: 目前支持 x86_64 架构。如需其他架构，请使用源码安装。

### Q: 如何更新？
A: 下载最新版本的可执行文件并替换旧版本即可。

### Q: macOS 版本什么时候推出？
A: macOS 版本正在开发中，预计很快会在 Releases 页面发布。

## 与源码运行的对比

| 特性 | 可执行文件 | 源码运行 |
|------|------------|----------|
| 安装难度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 文件大小 | 大 (~30MB) | 小 |
| 更新方式 | 手动下载 | git pull |
| 系统要求 | 无 | Python 3.8+ |
| 依赖管理 | 内置 | 需要管理 |

选择建议：
- **新手用户**：推荐使用可执行文件
- **Python 开发者**：推荐使用源码运行
- **服务器环境**：根据具体情况选择

## 反馈

如果您在使用可执行文件时遇到问题，请：

1. 查看[故障排除指南](/guide/troubleshooting)
2. 在 [GitHub Issues](https://github.com/MEKXH/gs3d/issues) 报告问题
3. 附上您的操作系统和版本信息