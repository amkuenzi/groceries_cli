from storage import jsonStorage
from models import Ingredient, Recipe, Pantry
import recipes, pantry, planner


def main():
    groceryLoader = jsonStorage(path='data')
    data = groceryLoader.load()
    print(data)

    chilli = Recipe("chilli con carne",
                       [Ingredient('ground beef', 500, 'g'),
                        Ingredient('kidney beans', 2, 'tins'),
                        Ingredient('red pepper', 2, 'units'),
                        Ingredient('chili flakes', 2, 'pinches'),
                        Ingredient('onions', 2.5, 'units'),
                        ],
                        portions=4)
    carbonara = Recipe("carbonara",
                       [Ingredient('spaghetti', 250, 'g'),
                        Ingredient('eggs', 2, 'units'),
                        Ingredient('parmegiano reggiano', 200, 'g'),
                        Ingredient('garlic', 2, 'cloves'),
                        Ingredient('bacon lardons', 100, 'g'),
                        ], portions=2)
    
    # test recipes
    
    response = recipes.add_recipe(groceryLoader, chilli)
    print(response)
    print(groceryLoader.load())
    response = recipes.add_recipe(groceryLoader, carbonara)
    print(response)
    print(groceryLoader.load())
    response = recipes.get_recipe(groceryLoader, 'chicken tikka masala')
    print(response)
    response = recipes.list_recipes(groceryLoader)
    print(response)
    chilli.portions += 4
    response = recipes.update_recipe(groceryLoader, chilli)
    print(response)
    print(groceryLoader.load())
    response = recipes.delete_recipe(groceryLoader, "chicken tikka masala")
    print(response)
    print(groceryLoader.load())



if __name__ == "__main__":
    main()
