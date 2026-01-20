"""CLI entry point & command definitions.

Interface:

grocery add-recipe
grocery list-recipes
grocery view-recipe <name>

grocery add-pantry-item
grocery list-pantry
grocery update-pantry

grocery plan-meal
grocery generate-shopping-list

"""

from pathlib import Path

import click

from grocery.models import Recipe, Ingredient
from grocery.storage import StorageInterface, jsonStorage
import grocery.recipes as recipes
import grocery.pantry as pantry
import grocery.planner as planner

# TODO: imporove how data storage works (should have a .groceries folder in "C:\Users\arthu")
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"

def get_storage() -> StorageInterface:
    return jsonStorage(DATA_DIR)

@click.group()
def cli():
    """Grocery CLI — plan meals and generate shopping lists."""
    pass

# ------------------------------
# +++++ Recipe Commands ++++++++
# ------------------------------


@cli.group()
def recipe():
    """Manage recipes."""
    pass

# TODO: recipes.remove_recipe
@recipe.command("remove")
@click.argument("name")
# TODO: recipes.get_recipe
# TODO: recipes.update_recipe

@recipe.command("add")
@click.argument("name", type=)
def add_recipe(name: str):
    """Add a new recipe."""
    storage = get_storage()

    ingredients = []
    click.echo("Enter ingredients (blank to finish):")

    while True:
        ingredient_name: str = click.prompt("Ingredient name", default="", show_default=False)
        if not ingredient_name:
            break

        unit: str = click.prompt("Unit:")
        quantity: float = click.prompt("Quantity:", type=float)

        ingredients.append(
            Ingredient(
                name=ingredient_name.lower(),
                quantity=quantity,
                unit=unit
            )
        )

    recipe_obj = Recipe(name=name.lower(), ingredients=ingredients)

    try:
        data, message = recipes.add_recipe(storage, recipe_obj)
        click.echo(message)
    except recipes.RecipeExistsError as e:
        click.echo(str(e), err=True)
    
@recipe.command("list")
@click.option('-v', '--verbose', count=True)
def list_recipes(verbose: bool):
    """List all recipes.
    
    TODO: optional verbose argument to specify ingredients"""
    storage = get_storage()

    for recipe in recipes.list_recipes(storage):
        if verbose:
            click.echo(str(recipe))
        else:
            click.echo(recipe.name)

# ------------------------------
# +++++ Pantry Commands ++++++++
# ------------------------------

@cli.group()
def pantry_cmd():
    """Manage pantry items."""
    pass

# TODO: pantry.take_item
# TODO: pantry.remove_item
# TODO: pantry.get_item

@pantry_cmd.command("add")
@click.argument("name")
@click.argument("quantity", type=float)
@click.argument("unit")
def add_pantry_item(name, quantity, unit):
    """Add an item to the pantry."""
    storage = get_storage()

    item = Ingredient(
        name=name.lower(),
        quantity=quantity,
        unit=unit
    )

    try:
        data, message = pantry.add_item(storage, item)
        click.echo(message)
    except pantry.UnitMismatchError as e:
        click.echo(str(e), err=True)

@pantry_cmd.command("list")
def list_pantry():
    """List pantry contents."""
    storage = get_storage()

    for item in pantry.list_items(storage):
        click.echo(f"{item.name}: {item.quantity} {item.unit}")


# ------------------------------
# +++++ Planner Commands +++++++
# ------------------------------

@cli.group()
def planner_cmd():
    """Manage meal plan."""
    pass

# TODO: planner.get_item
# TODO: planner.list_items
# TODO: planner.remove_item
# TODO: planner.adjust_portions

@planner_cmd.command("add")
@click.argument("name")
@click.argument("portions")
def add_planner_item(name: str, portions: str):
    """Add an item to the planner."""
    storage = get_storage()

    try:
        data, message = planner.add_item(storage, name, portions)
    except (recipes.RecipeNotFoundError, recipes.RecipeExistsError) as e:
        click.echo(str(e), err=True)

@cli.command("shop")
def generate_shopping_list():
    """Generate a shopping list from selected recipes."""
    storage = get_storage()

    shopping_list = planner.generate_shopping_list(storage)

    click.echo("\n ----- Shopping list -----")
    with open(BASE_DIR / "shoping_list.txt", "w") as f:
        f.write("Shopping list:\n\n")
        for item in shopping_list:
            f.write(str(item) + "\n")
            click.echo(str(item))

if __name__ == "__main":
    cli()