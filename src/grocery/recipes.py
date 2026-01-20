"""CRUD for recipes.

Create
Read
Update
Delete

### `recipes.py` should:
 - Enforce recipe invariants - rules that all recipes follow
 - Prevent duplicate recipe names
 - Hide storage details
 - Provide clear operations
 - TODO: Normalize ingredient names: lowercase, singular
### It should not:
 - Prompt users
 - Print tables
 - Know file paths
TODO: refactor into service classes instead of functions
    TODO: add prompt to generate new recipe item
TODO: Add transaction-style batching, also to pantry, planner
"""
from typing import List

from grocery.storage import StorageData     # Storage class prototype
from grocery.models import Recipe
from grocery.utils import select_data_source

class RecipeExistsError(Exception):
    pass

class RecipeNotFoundError(Exception):
    pass

@select_data_source
def add_recipe(data: StorageData, new_recipe: Recipe) -> tuple[StorageData, str]:
    new_recipe.name = new_recipe.name.lower()
    if new_recipe.name in data.recipes:
        raise RecipeExistsError(f"recipe: '{new_recipe.name}' already exists")
    
    data.recipes[new_recipe.name] = new_recipe
    return data, f'RecipeLib: added {new_recipe.name.title()}'

@select_data_source
def remove_recipe(data: StorageData, name: str) -> tuple[StorageData, str]:
    if name.lower() not in data.recipes:
        raise RecipeNotFoundError(name.lower)

    del data.recipes[name.lower()]
    return data, f"RecipeLib: deleted {name.lower()}"

@select_data_source
def update_recipe(data: StorageData, new_recipe: Recipe) -> tuple[StorageData, str]:
    new_recipe.name.lower()
    data.recipes[new_recipe.name] = new_recipe
    if new_recipe.name.lower() in data.recipes:
        message = f'Recipe Lib: updated {new_recipe.name.title()}'
    else:
        message = f'Recipe Lib: added {new_recipe.name.title()}'
    return data, message

@select_data_source
def get_recipe(data: StorageData, name: str) -> Recipe:
    try:
        retrieved = data.recipes[name.lower()]
    except KeyError:
        return RecipeNotFoundError(name)
    return retrieved

@select_data_source
def list_recipes(data: StorageData) -> List[Recipe]:
    recipe_list = list(data.recipes.values())
    return recipe_list
