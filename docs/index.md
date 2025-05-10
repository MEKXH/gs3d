---
layout: home
hero:
  name: GS3D
  text: 通用AWS S3下载工具
  tagline: 轻松下载AWS S3存储桶内容的跨平台工具
  image:
    src: /logo.svg
    alt: GS3D Logo
  actions:
    - theme: brand
      text: 下载可执行文件
      link: https://github.com/MEKXH/gs3d/releases/latest
    - theme: alt
      text: 快速开始
      link: /introduction/getting-started
    - theme: alt
      text: 查看源码
      link: https://github.com/MEKXH/gs3d
features:
  - icon: 🚀
    title: 开箱即用
    details: 下载可执行文件，无需安装Python或依赖
  - icon: 🖥️
    title: 双平台支持
    details: 支持Windows和Linux，macOS版本即将推出
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
    title: 简单易用
    details: 直接下载可执行文件，或使用源码运行
  - icon: ⚡
    title: 高效下载
    details: 多线程并行下载，最大限度提升下载速度

---

# 通用AWS S3下载工具

GS3D（Generic S3 Downloader）是一个强大而简单的工具，专为从AWS S3存储桶下载文件而设计。无论是公开数据集还是私有内容，GS3D都能帮助您轻松获取所需文件。

## 安装方式

### 可执行文件（推荐）

从[Releases页面](https://github.com/MEKXH/gs3d/releases/latest)下载适合您系统的版本：

- **Windows**: `gs3d-windows-x86_64.exe`
- **Linux**: `gs3d-linux-x86_64`
- **macOS**: 即将推出(如需使用，请先自行编译或使用源码)

下载后，您可以直接运行，无需安装Python环境。

### 源码运行

```bash
# 克隆仓库
git clone https://github.com/MEKXH/gs3d.git
cd gs3d

# 安装依赖
pip install boto3 tqdm

# 使用源码
python src/GS3D.py s3://bucket/file.txt
```

## 快速开始

### Windows
```bash
# 下载单个文件
gs3d-windows-x86_64.exe https://bucket.s3.amazonaws.com/file.txt

# 匿名访问公开存储桶
gs3d-windows-x86_64.exe https://public-bucket.s3.amazonaws.com/data/ -a
```

### Linux
```bash
# 添加执行权限
chmod +x gs3d-linux-x86_64

# 下载单个文件
./gs3d-linux-x86_64 https://bucket.s3.amazonaws.com/file.txt

# 下载文件夹并保留结构
./gs3d-linux-x86_64 s3://bucket/folder/ -k
```

## 主要功能

- **自动检测** - 自动识别文件或文件夹下载
- **匿名访问** - 内置对公开存储桶的匿名访问支持
- **灵活配置** - 丰富的命令行选项
- **实时进度** - 直观的进度条显示
- **并行下载** - 多线程提高下载速度
- **校验和验证** - 每个版本提供SHA256校验和

## 使用场景

GS3D特别适用于：

- 下载科研数据集（如GEOS-Chem气候数据）
- 从公开S3存储桶获取开源资源
- 备份和同步数据
- 在AWS EC2实例上访问S3存储桶
- 批量下载大型文件集合

## 命令行选项

```bash
# 基本使用
gs3d <s3-url>

# 常用选项
-a, --anonymous      # 使用匿名访问
-o, --output-dir     # 指定输出目录
-k, --keep-structure # 保留完整目录结构
-w, --max-workers    # 设置并发下载数
-p, --profile        # 使用特定AWS配置文件
--help               # 显示帮助信息
```

## 验证下载

每个版本都提供SHA256校验和，您可以验证下载的文件：

```bash
# Windows (PowerShell)
Get-FileHash gs3d-windows-x86_64.exe -Algorithm SHA256
# 比对 checksums.txt 中的值

# Linux
sha256sum gs3d-linux-x86_64
# 比对 checksums.txt 中的值
```

## 为什么选择GS3D？

与AWS CLI的`aws s3 sync`命令相比，GS3D提供了：

- **零配置使用** - 下载即用，无需安装Python或配置AWS CLI
- **简化语法** - 更直观的命令行接口
- **内置匿名访问** - 无需额外配置即可访问公开存储桶
- **更好的进度显示** - 实时进度条和下载统计

## 立即开始使用

<div style="display: flex; gap: 12px; margin-top: 24px;">
  <a href="https://github.com/MEKXH/gs3d/releases/latest" style="background: linear-gradient(145deg, #3246d3, #4366ea); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">下载可执行文件</a>
  <a href="/introduction/getting-started" style="background: #f4f4f5; color: #3c3c43; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">查看指南</a>
  <a href="/api/command-reference" style="border: 1px solid #e4e4e7; color: #3c3c43; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">API参考</a>
</div>

---

<div class="footer-message">
GS3D是一个开源项目，遵循MIT许可证，欢迎贡献和改进。<br>
💡 <a href="https://github.com/MEKXH/gs3d/issues">反馈问题</a> | 📖 <a href="/guide/troubleshooting">故障排除</a> | 🤝 <a href="/contributing">贡献指南</a>
</div>

<style>
.footer-message {
  text-align: center;
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #e4e4e7;
  color: #6b7280;
}

.footer-message a {
  color: #3246d3;
  text-decoration: none;
}

.footer-message a:hover {
  text-decoration: underline;
}
</style>