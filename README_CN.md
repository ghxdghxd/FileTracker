# FileTracker 文件跟踪工具

[English](README.md)

## 📝 项目简介

FileTracker 是一个命令行文件跟踪管理工具,专门用于管理和组织大规模文件系统。主要功能包括:

- 📁 递归文件扫描与管理 
- 🏷️ 灵活的文件标签系统
- 🔍 快速文件搜索
- 📊 详细的文件元数据显示

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/file-tracker.git
cd file-tracker

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

### 基本使用

```bash
# 添加文件/目录
ftrack [ -a ] /path/to/file|directory

# 递归添加目录
ftrack -r /path/to/directory

# 搜索文件名
ftrack -n "search_term"

# 按标签搜索
ftrack -t "tag_name"
```

## 💡 使用建议

1. **大型目录处理**
   - 使用 `-r` 选项递归添加
   - 观察进度条了解处理进度
   - 注意检查失败添加的文件数

2. **文件组织**
   - 合理使用标签系统
   - 定期更新数据库
   - 及时清理无效记录

## 📄 许可证

本项目采用 MIT 许可证

*注：本项目仍在积极开发中，欢迎提供反馈和建议！*
