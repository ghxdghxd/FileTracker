import os

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def count_files(directory):
    """计算目录中的文件数量"""
    count = 0
    for root, _, files in os.walk(directory):
        count += len(files)
    return count 