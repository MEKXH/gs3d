# 目录结构保留

S3下载工具提供了灵活的目录结构管理选项，让你可以根据需要选择是否保留完整的S3存储桶目录结构。本页面详细介绍目录结构保留功能。

## 目录结构选项

S3下载工具提供两种目录结构处理模式：

1. **默认模式**：只保留相对于指定前缀的路径
2. **保留结构模式**：保留完整的S3目录结构

## 默认模式 - 相对路径

在默认模式下，脚本会将文件下载到输出目录，只保留相对于指定前缀的路径：

```bash
python G3SD.py s3://my-bucket/deep/nested/folder/ --output-dir ./downloads
```

这将把 `deep/nested/folder/` 下的文件直接下载到 `./downloads` 目录，不会创建 `deep/nested/folder/` 的额外目录结构。

### 示例

假设S3存储桶中有以下文件：
- `s3://my-bucket/deep/nested/folder/file1.txt`
- `s3://my-bucket/deep/nested/folder/subfolder/file2.txt`

在默认模式下，下载后的结构将是：
```
downloads/
  ├── file1.txt
  └── subfolder/
      └── file2.txt
```

## 保留完整目录结构

使用 `--keep-structure` 或 `-k` 参数可以保留完整的目录结构：

```bash
python G3SD.py s3://my-bucket/deep/nested/folder/ --output-dir ./downloads --keep-structure
```

这将把文件下载到 `./downloads/deep/nested/folder/` 目录，完整保留原始目录结构。

### 示例

使用相同的S3文件：
- `s3://my-bucket/deep/nested/folder/file1.txt`
- `s3://my-bucket/deep/nested/folder/subfolder/file2.txt`

在保留结构模式下，下载后的结构将是：
```
downloads/
  └── deep/
      └── nested/
          └── folder/
              ├── file1.txt
              └── subfolder/
                  └── file2.txt
```

## 实际使用场景

### 场景一：GEOS-Chem气候数据

从GEOS-Chem存储桶下载2024年2月的数据：

#### 不保留目录结构
```bash
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --output-dir ./climate-data
```

结果：
```
climate-data/
  ├── file1.nc
  ├── file2.nc
  └── ...
```

#### 保留目录结构
```bash
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --output-dir ./climate-data --keep-structure
```

结果：
```
climate-data/
  └── GEOS_2x2.5/
      └── MERRA2/
          └── 2024/
              └── 02/
                  ├── file1.nc
                  ├── file2.nc
                  └── ...
```

### 场景二：多月份数据下载

当你需要下载多个月份的数据时，目录结构管理尤为重要：

#### 不保留结构（单独下载）
```bash
# 单独下载每个月，放在不同目录
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/01/ --anonymous --output-dir ./data-01
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --output-dir ./data-02
```

#### 保留结构（统一目录）
```bash
# 下载到同一个目录，保留结构以避免冲突
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/01/ --anonymous --output-dir ./climate-data --keep-structure
python G3SD.py s3://geos-chem/GEOS_2x2.5/MERRA2/2024/02/ --anonymous --output-dir ./climate-data --keep-structure
```

## 选择合适的模式

### 适合默认模式的情况

- 你只关心文件内容，不需要额外的目录结构
- 你只下载特定的单个文件夹内容
- 你想要简化文件组织，减少嵌套层级
- 所有文件名都是唯一的，不会出现冲突

### 适合保留结构模式的情况

- 你需要保留原始数据集的组织方式
- 你要处理多个不同路径但可能有同名文件的情况
- 目录结构本身包含重要信息（如时间序列、分类等）
- 你希望