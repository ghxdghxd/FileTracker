# FileTracker

A command-line file tracking and management system for organizing large-scale filesystems.

[中文文档](README_CN.md)

## ✨ Key Features

- 📁 Recursive file scanning and management
- 🏷️ Flexible file tagging system  
- 🔍 Fast file search capabilities
- 📊 Detailed file metadata display

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Git (for installation from source)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/file-tracker.git
cd file-tracker

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Basic Usage

```bash
# Add file/directory
ftrack [ -a ] /path/to/file|directory

# Recursively add directory
ftrack -r /path/to/directory 

# Search by filename
ftrack -n "search_term"

# Search by tag
ftrack -t "tag_name"
```

## 💡 Best Practices

1. **Large Directory Processing**
   - Use `-r` flag for recursive adding
   - Monitor progress via progress bar
   - Check failed file count

2. **File Organization**
   - Use tags effectively
   - Update database regularly
   - Clean invalid records

## 📄 License

This project is licensed under the MIT License

*Note: This project is under active development. Feedback and suggestions welcome!*
