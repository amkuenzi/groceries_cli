"""Pantry CRUD.

TODO: Normalize ingredient names: lowercase, singular
TODO: Unit conversions, hooks
TODO: Item search/ fuzzy comparisons
TODO: refactor into service classes instead of functions
    TODO: add prompt to generate new pantry item
"""
from typing import List

from storage import StorageData     # Storage class prototype
from models import Ingredient
from utils import select_data_source

class PantryItemNotFoundError(Exception):
    pass

class UnitMismatchError(Exception):
    pass

class InvalidAdjustError(Exception):
    pass

@select_data_source
def add_item(data: StorageData, item: Ingredient) -> tuple[StorageData, str]:
    item.name = item.name.lower()

    if item.name in data.pantry:
        if data.pantry[item.name].unit != item.unit:
            raise UnitMismatchError(f"Pantry: {item.name.lower()} unit '{item.unit}' != '{data.pantry[item.name].unit}'")
        
        data.pantry[item.name].quantity += item
        return data, f"Pantry: {str(data.pantry[item.name])}, increased by {item.quantity} {item.unit}"
    else:
        data.pantry[item.name] = item
        return data, f"Pantry: added {str(data.pantry[item.name])}"

@select_data_source
def take_item(data: StorageData, item: Ingredient) -> tuple[StorageData, str]:
    item.name = item.name.lower()

    if item.name not in data.pantry:
        raise PantryItemNotFoundError(f"Pantry: {item.name} not listed, so cannot take any away")
    
    if item.unit != data.pantry[item.name].unit:
        raise UnitMismatchError(f"Pantry: {item.name.lower()} unit '{item.unit}' != '{data.pantry[item.name].unit}'")
    
    data.pantry[item.name] -= item
    return data, f"Pantry: {str(data.pantry[item.name])}, reduced by {item.quantity} {item.unit}"
    
@select_data_source
def remove_item(data: StorageData, name: str) -> tuple[StorageData, str]:
    name = name.lower()
    if name not in data.pantry:
        raise PantryItemNotFoundError(name)
    
    data.pantry[name].quantity = 0
    return data, f"Pantry: {str(data.pantry[name])}"

@select_data_source
def get_item(data: StorageData, name: str) -> Ingredient:
    name = name.lower()
    if name.lower() in data.pantry:
        return data.pantry[name.lower()]
    else:
        raise PantryItemNotFoundError(name.title())

@select_data_source
def list_items(data: StorageData) -> List[Ingredient]:
    pantry_list = list(data.pantry.values())
    return pantry_list
