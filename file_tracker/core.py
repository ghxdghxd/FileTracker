from .database import Database
from .file_ops import FileOps
import os
from datetime import datetime

class FileTracker:
    def __init__(self, db_path=None):
        self.db = Database(db_path)
        self.file_ops = FileOps()
    
    def add_file(self, filepath):
        """添加文件到追踪系统"""
        if not os.path.exists(filepath):
            return False
            
        file_info = self.file_ops.get_file_info(filepath)
        if not file_info:
            return False
            
        return self.db.add_file(file_info)
    
    def list_files(self):
        """列出所有追踪的文件"""
        return self.db.list_files()
    
    def search_by_name(self, name):
        """按名称搜索文件"""
        return self.db.search_by_name(name)
    
    def search_by_tag(self, tag):
        """按标签搜索文件"""
        return self.db.search_by_tag(tag)
    
    def add_tag(self, filepath, tag):
        """为文件添加标签"""
        return self.db.add_tag(filepath, tag)
    
    def remove_tag(self, filepath, tag):
        """移除文件的标签"""
        return self.db.remove_tag(filepath, tag)
    
    def update_database(self):
        """更新数据库中的文件信息"""
        return self.db.update_all_files(self.file_ops)
    
    def file_exists(self, filepath):
        """检查文件是否已被追踪"""
        return self.db.file_exists(filepath)
