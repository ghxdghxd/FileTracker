import os
import pwd
from datetime import datetime

class FileOps:
    def get_file_info(self, filepath):
        """获取文件信息"""
        try:
            stat = os.stat(filepath)
            creator = self._get_creator_info(stat)
            
            # 如果是目录，计算总大小
            if os.path.isdir(filepath):
                filesize = self._get_dir_size(filepath)
            else:
                filesize = stat.st_size
            
            return {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'filetype': 'directory' if os.path.isdir(filepath) else 'file',
                'filesize': filesize,
                'create_time': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modify_time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'creator': creator,
                'tags': []
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def _get_creator_info(self, stat):
        """获取创建者信息"""
        try:
            pw = pwd.getpwuid(stat.st_uid)
            return {
                'uid': pw.pw_uid,
                'name': pw.pw_name
            }
        except:
            return {
                'uid': stat.st_uid,
                'name': 'unknown'
            }
    
    def _get_dir_size(self, dirpath):
        """递归计算目录总大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(dirpath):
                # 计算文件大小
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):  # 确保文件存在
                        try:
                            total_size += os.path.getsize(filepath)
                        except (OSError, IOError):
                            continue  # 跳过无法访问的文件
                
                # 计算子目录大小
                for dirname in dirnames:
                    dirpath = os.path.join(dirpath, dirname)
                    if os.path.exists(dirpath):  # 确保目录存在
                        try:
                            total_size += os.path.getsize(dirpath)
                        except (OSError, IOError):
                            continue  # 跳过无法访问的目录
        except Exception as e:
            print(f"Error calculating directory size: {e}")
        
        return total_size