from typing import Optional

class FileTrackerSingleton:
    _instance = None
    _cache = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance 