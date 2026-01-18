"""Handle data storage

TODO: handle archiving of pantry data
TODO: 2 stage writes

API:
 - jsonStorage handler class
 - load() -> StorageData containter
 - save(data:StorageData) saves data to json
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Protocol, runtime_checkable
import json
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

from models import Recipe, Pantry, Ingredient


@dataclass
class StorageData:
    recipes: Dict[str, Recipe] = field(default_factory=dict)
    pantry: Dict[str, Ingredient] = field(default_factory=dict)
    planner: Dict[str, int] = field(default_factory=dict)


@runtime_checkable
class StorageInterface(Protocol):
    def load(self) -> StorageData:
        ...

    def save(self, data: StorageData) -> None:
        ...
    
    @contextmanager
    def storage_data(self):
        # Code to acquire resource, e.g.:
        data = self.load()
        try:
            yield data
        finally:
            # Code to release resource, e.g.:
            self.save(data)
    
    @classmethod
    @contextmanager
    def use_storage_data(cls, data: StorageData):
        yield data
        

class jsonStorage(StorageInterface):

    def __init__(self, path: str):
        super().__init__()
        self.data_dir = Path(path)
        self.data_file = self.data_dir / "data.json"
        self._storage_data = None

    def load(self) -> StorageData:
        if not self.data_dir.exists():
            return StorageData()
        
        with open(self.data_file, 'r') as f:
            raw = json.load(fp=f)
        
        recipes = {
            name: Recipe(
                name=name.lower(),
                portions=recipe['portions'],
                ingredients=[
                    Ingredient(**i) for i in recipe["ingredients"]
                ]
            )
            # get() protects against recipes being empty.
            #   To make missing data not throw an error, make default 
            #   the same type as recipes, a dict in this case
            for name, recipe in raw.get("recipes", {}).items()
        }
        
        pantry = {
            name: Ingredient(**i)
            for name, i in raw.get('pantry', {}).items()
        }
        
        planner = {name.lower(): p for name, p in raw.get("planner", {}).items()}

        return StorageData(recipes=recipes, pantry=pantry, planner=planner)      

    def save(self, data: StorageData) -> None:
        # self.data_dir.mkdir(self.data_dir, parents=True, exist_ok=True)

        serialised = {
            "recipes": {
                name: asdict(r)
                for name, r in data.recipes.items()
            },
            "pantry": {
                name: asdict(i)
                for name, i in data.pantry.items()
            },
            "planner":{
                name: p
                for name, p in data.planner.items()
            }
        }

        # backup
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup = self.data_dir / "backup" / (timestamp+"_data.json")
        self.data_file.replace(backup)


        # two-stage write
        tmp_file = self.data_file.with_suffix(".tmp")
        with tmp_file.open("w", encoding="utf-8") as f:
            json.dump(serialised, f, indent=2)

        tmp_file.replace(self.data_dir / "data.json")
