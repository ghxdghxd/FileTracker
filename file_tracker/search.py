from typing import List, Dict, Any
from functools import lru_cache

class Search:
    def __init__(self, cache: Dict[str, Any]):
        self._cache = cache
    
    @lru_cache(maxsize=100)
    def by_name(self, name: str) -> List[Dict[str, Any]]:
        """按名称搜索文件"""
        name = name.lower()
        return [
            item for item in self._cache.values() 
            if name in item['filename'].lower()
        ]
    
    @lru_cache(maxsize=100)
    def by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """按标签搜索文件"""
        return [
            item for item in self._cache.values() 
            if tag in item.get('tags', [])
        ]
    
    def clear_cache(self):
        self.by_name.cache_clear()
        self.by_tag.cache_clear() 