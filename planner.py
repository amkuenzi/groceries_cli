"""Planner CRUD and shopping list logic.

TODO: shopping list unit conversions
TODO: refactor into service classes instead of functions
    TODO: add prompt to generate new planner item
TODO: check all planner keys are in recipies
"""

from typing import List, Dict

from storage import StorageData     # Storage class prototype
from models import Ingredient
from recipes import RecipeNotFoundError, RecipeExistsError
import pantry
from utils import select_data_source


@select_data_source
def add_item(data: StorageData, name:str, portions:int) -> tuple[StorageData, str]:
    name = name.lower()
    if name in data.planner:
        raise RecipeExistsError(f"Planner: already contains {name}")
    if name not in data.recipes:
        raise RecipeNotFoundError(f"Planner: {name} not in recipe library")
    
    data.planner[name] = portions
    return data, f"Planner: added {name.capitalize()} ({portions} portions)"

@select_data_source
def remove_item(data: StorageData, name:str) -> tuple[StorageData, str]:
    if name.lower() not in data.planner:
        raise RecipeNotFoundError(f"{name} not in planner")
    else:
        del data.planner[name]
        return data, f"Planner: removed {name} from planner"

@select_data_source
def get_item(data: StorageData, name:str) -> int:
    if name.lower() not in data.planner:
        raise RecipeNotFoundError(f"{name} not in planner")
    else:
        return data.planner[name]

@select_data_source
def list_items(data: StorageData) -> List[tuple[str, int]]:
    return [(name, portions) for name, portions in data.planner.items()]

@select_data_source
def adjust_portions(data: StorageData, name:str, portions:str) -> tuple[StorageData, str]:
    name = name.lower()
    portions = portions.replace(" ", "")
    sign = portions[0]
    portions = int(portions)
    if sign == "-":
        data.planner[name] += portions
        if data.planner[name] <= 0:
            return remove_item(data=data, name=name)
        else:
            return data, f"Planner: reduced {name} by {portions} portions to {data.planner[name]}"
    
    if name not in data.planner:
        return add_item(data, name, portions)
    else:
        data.planner[name] += portions
        return data, f"Planner: increased {name} by {portions} portions to {data.planner[name]}"

@select_data_source
def generate_shopping_list(data: StorageData) -> Dict[str, Ingredient]:
    # scale recipies by plan portions
    allowed_recipes = data.planner.keys() & data.recipes.keys()
    for k in data.planner.copy().keys():
        if k not in allowed_recipes:
            print(f"{k} not in RecipeLib, removing")
            remove_item(data, k)
    
    scaled_recipes: Dict[str, List[Ingredient]] = {
        name: data.recipes[name].scaled_ingredients(portions) 
        for name, portions in data.planner.items()
        }
    
    # collate ingredients from all recipes
    shopping_ingredients = {}
    for _, ingredList in scaled_recipes.items():
        for i in ingredList:
            if i.name not in shopping_ingredients.keys():
                shopping_ingredients[i.name] = i
            else:
                shopping_ingredients[i.name] += i

    # subtract pantry contents
    for n, i in shopping_ingredients.items():
        # print(pantry.get_item(data=data, name="rice"))
        try:
            shopping_ingredients[n] -= pantry.get_item(data, n)
        except pantry.PantryItemNotFoundError:
            continue
    return shopping_ingredients
 