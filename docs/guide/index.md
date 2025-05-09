# GS3D使用指南

欢迎使用GS3D工具的使用指南。本指南涵盖了GS3D工具的所有功能和用法，从基础到高级。

## 内容概览

- [基本用法](./basic-usage) - 学习GS3D的基本使用方法
- [高级选项](./advanced-options) - 探索更多高级功能和选项
- [匿名访问](./anonymous-access) - 了解如何无需凭证访问公开存储桶
- [目录结构保留](./keep-structure) - 管理下载文件的目录结构
- [故障排除](./troubleshooting) - 解决常见问题和错误

## 快速参考

最常用的GS3D命令：

```bash
# 基本用法
python GS3D.py s3://my-bucket/my-folder/ --output-dir ./downloads

# 匿名访问公开存储桶
python GS3D.py s3://public-bucket/folder/ --anonymous --region us-east-1

# 保留完整目录结构
python GS3D.py s3://my-bucket/folder/ --keep-structure --output-dir ./downloads

# 调整并发下载线程数
python GS3D.py s3://my-bucket/folder/ --max-workers 20

# 组合多个选项
python GS3D.py s3://public-bucket/folder/ --anonymous --region us-east-1 --output-dir ./data --keep-structure
```

## 开始使用

如果你是第一次使用GS3D，建议从[基本用法](./basic-usage)开始，了解工具的基本功能和参数。

如果你已经熟悉基础知识，可以直接查看[高级选项](./advanced-options)了解更多功能，或者参考[API参考](/api/)获取完整的命令行参数列表。