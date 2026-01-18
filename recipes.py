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
from typing import List, Union

from storage import Storage, StorageData     # Storage class prototype
from models import Recipe


class RecipeExistsError(Exception):
    pass


class RecipeNotFoundError(Exception):
    pass


def add_recipe(storage: Storage, new_recipe: Recipe) -> str:
    with storage.storage_data() as data:
        # Prevent duplicate names
        if new_recipe.name.lower() in data.recipes:
            raise RecipeExistsError(f"recipe: '{new_recipe.name}' already exists")
        
        # add recipe
        data.recipes[new_recipe.name.lower()] = new_recipe
    return f'Added {new_recipe.name.lower()}'


def get_recipe(storage: Storage, name: str) -> Recipe:
    with storage.storage_data() as data:
        try:
            retrieved =  data.recipes[name.lower()]
        except KeyError:
            return RecipeNotFoundError(name)
    return retrieved


def list_recipes(storage: Storage) -> List[Recipe]:
    with storage.storage_data() as data:
        recipe_list = list(data.recipes.values())
    return recipe_list


def update_recipe(storage: Storage, new_recipe: Recipe) -> str:
    with storage.storage_data() as data:
        data.recipes[new_recipe.name.lower()] = new_recipe
        if new_recipe.name.lower() in data.recipes:
            message = f'Updated: {new_recipe.name.lower()}'
        else:
            message = f'Added: {new_recipe.name.lower()}'
    return message


def delete_recipe(storage: Storage, name: str) -> str:
    with storage.storage_data() as data:
        if name.lower() not in data.recipes:
            raise RecipeNotFoundError(name.lower)

        del data.recipes[name.lower()]
    return f"Deleted: {name.lower()}"
