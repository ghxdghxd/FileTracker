import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        """初始化数据库
        db_path: JSON文件的路径,默认为 filetrack.json
        """
        self.db_path = db_path or 'filetrack.json'
        self._init_db()
    
    def _init_db(self):
        """初始化JSON文件"""
        if not os.path.exists(self.db_path):
            self._save_data({'files': {}})
    
    def _load_data(self):
        """每次需要时从文件加载数据"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'files': {}}
    
    def _save_data(self, data):
        """每次修改后保存到文件"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_file(self, file_info):
        """添加或更新文件记录"""
        try:
            data = self._load_data()
            data['files'][file_info['filepath']] = {
                'filename': file_info['filename'],
                'filetype': file_info['filetype'],
                'filesize': file_info['filesize'],
                'create_time': file_info['create_time'],
                'modify_time': file_info['modify_time'],
                'creator': file_info['creator'],
                'tags': file_info.get('tags', [])
            }
            self._save_data(data)
            return True
        except Exception as e:
            print(f"Error adding file: {e}")
            return False
    
    def search_by_name(self, name):
        """按名称搜索文件"""
        data = self._load_data()
        results = []
        
        for filepath, info in data['files'].items():
            if name.lower() in filepath.lower() or name.lower() in info['filename'].lower():
                results.append(self._format_file_info(filepath, info))
        
        return results
    
    def search_by_tag(self, tag):
        """按标签搜索文件"""
        data = self._load_data()
        results = []
        
        for filepath, info in data['files'].items():
            if tag in info.get('tags', []):
                results.append(self._format_file_info(filepath, info))
        
        return results
    
    def add_tag(self, filepath, tag):
        """为文件添加标签"""
        data = self._load_data()
        if filepath not in data['files']:
            return False
            
        if 'tags' not in data['files'][filepath]:
            data['files'][filepath]['tags'] = []
            
        if tag not in data['files'][filepath]['tags']:
            data['files'][filepath]['tags'].append(tag)
            self._save_data(data)
        return True
    
    def remove_tag(self, filepath, tag):
        """移除文件的标签"""
        data = self._load_data()
        if filepath not in data['files']:
            return False
            
        if tag in data['files'][filepath].get('tags', []):
            data['files'][filepath]['tags'].remove(tag)
            self._save_data(data)
        return True
    
    def _format_file_info(self, filepath, info):
        """格式化文件信息"""
        return {
            'filepath': filepath,
            'filename': info['filename'],
            'filetype': info['filetype'],
            'filesize': info['filesize'],
            'create_time': info['create_time'],
            'modify_time': info['modify_time'],
            'creator': info['creator'],
            'tags': info.get('tags', [])
        }
    
    def list_files(self):
        """列出所有文件"""
        data = self._load_data()
        results = []
        
        for filepath, info in data['files'].items():
            file_info = self._format_file_info(filepath, info)
            results.append(file_info)
            
        return results
    
    def update_all_files(self, file_ops):
        """更新所有文件的信息"""
        data = self._load_data()
        updated_files = {'files': {}}
        updated_count = 0
        failed_count = 0
        
        for filepath in data['files'].keys():
            if os.path.exists(filepath):
                # 获取最新的文件信息
                new_info = file_ops.get_file_info(filepath)
                if new_info:
                    # 保留原有标签
                    new_info['tags'] = data['files'][filepath].get('tags', [])
                    updated_files['files'][filepath] = {
                        'filename': new_info['filename'],
                        'filetype': new_info['filetype'],
                        'filesize': new_info['filesize'],
                        'create_time': new_info['create_time'],
                        'modify_time': new_info['modify_time'],
                        'creator': new_info['creator'],
                        'tags': new_info['tags']
                    }
                    updated_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        # 保存更新后的数据
        self._save_data(updated_files)
        
        return {
            'updated': updated_count,
            'failed': failed_count,
            'total': updated_count + failed_count
        }
    
    def file_exists(self, filepath):
        """检查文件是否存在于数据库中"""
        data = self._load_data()
        return filepath in data['files']