"""Pantry CRUD.

TODO: Normalize ingredient names: lowercase, singular
TODO: Unit conversions, hooks
TODO: Item search/ fuzzy comparisons
TODO: refactor into service classes instead of functions
    TODO: add prompt to generate new pantry item
"""
from typing import List

from storage import Storage     # Storage class prototype
from models import Ingredient

class PantryItemNotFoundError(Exception):
    pass

class UnitMismatchError(Exception):
    pass

class InvalidAdjustError(Exception):
    pass


def add_item(storage: Storage, item: Ingredient) -> str:
    with storage.storage_data() as data:
        if item.name.lower() in data.pantry:
            existing = data.pantry[item.name.lower()]
            if existing.unit != item.unit:
                raise UnitMismatchError(f"Item: {item.name.lower()} unit '{item.unit}' != '{existing.unit}'")
            
            existing.quantity += item.quantity
        else:
            data.pantry[item.name.lower()] = item
    return f"Added {item.name.lower()}: {item.quantity} {item.unit}"


def get_item(storage: Storage, name: str) -> Ingredient:
    with storage.storage_data() as data:
        if name.lower() in data.pantry:
            found = data.pantry[name.lower()]
        else:
            raise PantryItemNotFoundError(name.lower())


def remove_item(storage: Storage, name: str) -> str:
    with storage.storage_data() as data:
        if name.lower() not in data.pantry:
            raise PantryItemNotFoundError(name)
        
        del data.pantry[name.lower()]
    return f"Removed {name.lower()}"


def list_items(storage: Storage) -> List[Ingredient]:
    with storage.storage_data() as data:
        pantry_list = list(data.pantry.values())
    return pantry_list
    

def adjust_quantity(storage: Storage, name: str, amount: float, delta: bool=True) -> str:
    """TODO: add unit adjustments"""
    with storage.storage_data() as data:
        if name.lower() not in data.pantry:
            raise PantryItemNotFoundError(name.lower())
        
        if not delta:
            if amount < 0:
                raise InvalidAdjustError("Cannot set quantity to below zero.")
            else:
                data.pantry[name.lower()].quantity = amount
        else:
            data.pantry[name.lower()].quantity += amount
            if data.pantry[name.lower()].quantity < 0:
                del data.pantry[name.lower()]
