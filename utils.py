"""General utilities"""

from typing import List, Dict, Union
from functools import wraps

from storage import StorageInterface, StorageData


def select_data_source(func):
    @wraps(func)
    def wrapper(data_source: Union[StorageInterface, StorageData], *args, **kwargs):

        if isinstance(data_source, StorageInterface):
            with data_source.storage_data() as data:
                return func(data, *args, *kwargs)
            
        elif isinstance(data_source, StorageData):
            return func(data_source, *args, **kwargs)
        
        else:
            raise ValueError(f"{repr(func)} data source must be of type: {repr(StorageInterface)} or {repr(StorageData)}")
    
    return wrapper
