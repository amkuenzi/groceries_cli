"""Planner CRUD and shopping list logic.

TODO: shopping list unit conversions
TODO: refactor into service classes instead of functions
    TODO: add prompt to generate new planner item
TODO: check all planner keys are in recipies
"""

from typing import List, Dict, Union

from models import Ingredient
from storage import Storage, StorageData     # Storage class prototype
from recipes import RecipeNotFoundError
from pantry import InvalidAdjustError

def add_item(storage: Union[Storage, StorageData], name:str, portions:int) -> str:
    if isinstance(storage, Storage):
        cm: StorageData = storage.storage_data()
    else:
        cm: StorageData = Storage.use_storage_data(storage)
    with cm as data:
        if name.lower() in data.planner:
            data.planner[name] += portions      # add portions if meal already exists
        else:
            data.planner[name] = portions
    return f"Added {portions} portions of {name.lower()}"


def get_item(storage: Storage, name:str) -> int:
    with storage.storage_data() as data:
        if name.lower() not in data.planner:
            raise RecipeNotFoundError(f"{name} not in planner")
        else:
            return data.planner[name]

def remove_item(storage: Storage, name:str) -> str:
    with storage.storage_data() as data:
        if name.lower() not in data.planner:
            raise RecipeNotFoundError(f"{name} not in planner")
        else:
            del data.planner[name]
            return f"Removed {name} from planner"

def list_items(storage: Storage) -> List[tuple[str, int]]:
    with storage.storage_data() as data:
        return [(name, portions) for name, portions in data.planner.items()]

def adjust_portions(storage: Storage, name:str, amount:int, delta: bool=False) -> str:
    with storage.storage_data() as data:
        if not delta:
            if amount < 0:
                raise InvalidAdjustError(f"Planner adjust: {name}, portions cannot be < 0")
            if name.lower() not in data.planner:
                message = add_item(storage=data, name=name, portions=amount)
            else:
                data.planner[name.lower()] = amount
                message = f"Set {name} portions to {amount}"
        else:
            data.planner[name.lower()] += amount
            message = f"Set {name} portions to {amount}"
            if data.planner[name.lower()] < 0:
                message = remove_item(storage=storage, name=name)
    return message


def generate_shopping_list(storage: Storage) -> Dict[str, Ingredient]:
    with storage.storage_data() as data:
        # 1 select recipes by planner
        selected_recipes = data.recipes.keys() & data.planner.keys()
        # 2 get scaling factors
        scaling_factors = {
            name: data.planner[name] / data.recipes[name].portions
            for name in selected_recipes
            }
        # 3 scale recipes
        scaled_recipe_ingredients: Dict[str,List[Ingredient]] = {
            name: [i * scaling_factors[name] 
                   for i in data.recipes[name].ingredients]
            for name in selected_recipes
            }
        # 4 flatten ingredients
        shopping_ingredients = {}
        for rname, ingredList in scaled_recipe_ingredients.items():
            for i in ingredList:
                if i.name not in shopping_ingredients.keys():
                    shopping_ingredients[i.name] = {'quantity': i.quantity, "unit": i.unit}
                else:
                    shopping_ingredients[i.name]["quantity"] += i.quantity
        
        return shopping_ingredients
 