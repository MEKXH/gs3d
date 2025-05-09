# GS3D - Generic S3 Downloader

<p align="center">
  <img src="./docs/public/logo.svg" alt="GS3D Logo" width="200"/>
</p>

<p align="center">
  <a href="https://github.com/MEKXH/gs3d/releases"><img src="https://img.shields.io/github/v/release/MEKXH/gs3d" alt="Release"></a>
  <a href="https://github.com/MEKXH/gs3d/blob/main/LICENSE"><img src="https://img.shields.io/github/license/MEKXH/gs3d" alt="License"></a>
  <a href="https://github.com/MEKXH/gs3d/issues"><img src="https://img.shields.io/github/issues/MEKXH/gs3d" alt="Issues"></a>
  <a href="https://mekxh.github.io/gs3d/"><img src="https://img.shields.io/badge/docs-online-blue" alt="Documentation"></a>
</p>

[中文文档](README_zh.md)

## Introduction

GS3D (Generic S3 Downloader) is a versatile Python tool designed specifically for downloading entire folders and their contents from AWS S3 buckets. It provides a simple yet powerful command-line interface that enables users to easily retrieve files from S3 buckets.

### Core Features

- **Multi-threaded parallel downloads**: Utilize multi-threading technology to download multiple files simultaneously, significantly improving download speed
- **Anonymous access support**: Access public buckets without AWS credentials
- **Directory structure management**: Flexibly choose whether to preserve the complete S3 directory structure
- **Real-time progress display**: Visually track download progress through a progress bar
- **Multiple authentication methods**: Support for AWS configuration profiles, access keys, and default credentials

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Installing Dependencies

```bash
pip install boto3 tqdm
```

### Getting GS3D

Clone this repository or download the script directly:

```bash
git clone https://github.com/MEKXH/gs3d.git
cd gs3d
```

## Quick Start

### Basic Usage

```bash
python GS3D.py s3://my-bucket/my-folder/ --output-dir ./downloads
```

### Downloading from Public Buckets

```bash
python GS3D.py s3://public-bucket/folder/ --anonymous
```

### Preserving Directory Structure

```bash
python GS3D.py s3://my-bucket/folder/ --keep-structure --output-dir ./downloads
```

### Using AWS Profile

```bash
python GS3D.py s3://my-bucket/folder/ --profile my-profile-name
```

## Command Line Arguments

| Parameter | Short Form | Description |
|-----------|------------|-------------|
| `s3_url` | - | S3 link (required) |
| `--profile` | `-p` | AWS configuration profile name |
| `--access-key` | `-ak` | AWS access key ID |
| `--secret-key` | `-sk` | AWS secret access key |
| `--region` | `-r` | AWS region |
| `--output-dir` | `-o` | Local output directory, defaults to current directory |
| `--max-workers` | `-w` | Maximum number of concurrent download threads, default is 10 |
| `--anonymous` | `-a` | Use anonymous access mode (for public buckets) |
| `--keep-structure` | `-k` | Preserve complete directory structure |

## Use Cases

### Downloading GEOS-Chem Climate Data

```bash
python GS3D.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --region us-east-1 --output-dir ./climate-data
```

### Backing Up Project Resources

```bash
python GS3D.py s3://my-company/project-assets/ --profile work --output-dir ./backup --keep-structure
```

### Using on AWS EC2 Instances

When running on an EC2 instance with an IAM role configured, no credentials are needed:

```bash
python GS3D.py s3://internal-data/reports/ --output-dir /mnt/data
```

## Documentation

Complete documentation is available on our [official documentation site](https://mekxh.github.io/gs3d/).

### Running Documentation Locally

If you want to run the documentation site locally:

```bash
# Install dependencies
pnpm install

# Start development server
pnpm docs:dev
```

Then visit `http://localhost:5173` in your browser.

### Documentation Deployment

This project provides two deployment scripts for deploying documentation to GitHub Pages:

#### Using the Full Deployment Script (Recommended)

The full version script provides detailed logging and error handling:

```powershell
.\scripts\deploy.ps1
```

#### Using the Quick Deployment Script

The quick version script is more concise but requires the repository URL:

```powershell
.\scripts\quick-deploy.ps1 -RepoUrl "https://github.com/MEKXH/gs3d.git"
```

Both scripts support the following parameters:
- `-RepoUrl`: GitHub repository URL
- `-BranchName`: Deployment branch name (default: gh-pages)
- `-Force`: Force push (overwrite remote history)

## Project Structure

```
gs3d/
├── GS3D.py              # Main script file
├── docs/                # Documentation source files
│   ├── .vitepress/      # VitePress configuration
│   ├── public/          # Static resources
│   ├── guide/           # Guide documentation
│   ├── introduction/    # Introduction documentation
│   ├── api/             # API reference
│   └── index.md         # Homepage
├── scripts/             # Utility scripts
│   ├── deploy.ps1       # Full deployment script
│   └── quick-deploy.ps1 # Quick deployment script
├── package.json         # Project configuration
└── README.md            # Project description
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is released under the [MIT License](LICENSE).

## Acknowledgments

- [boto3](https://github.com/boto/boto3) - Python SDK for interacting with AWS services
- [tqdm](https://github.com/tqdm/tqdm) - For displaying progress bars
- [VitePress](https://vitepress.dev/) - For building the documentation site

## Contact

If you have any questions or suggestions, please [open an issue](https://github.com/MEKXH/gs3d/issues)

---
