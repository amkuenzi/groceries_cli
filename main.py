"""Main groceries cli script

Creates simple looped control set, not proper cli
TODO: CLI with argparse/ click."""

import json

from storage import jsonStorage
import recipes, pantry, planner

def main():

    groceryLoader = jsonStorage('data')

    header = "Grocery Planner CLI"
    commands_list = "Commands:\n" \
    "  [r] list recipies\n" \
    "  [p] list pantry\n" \
    "  [m] show meal plan\n" \
    "  [a] add to meal plan\n" \
    "  [d] remove from meal plan\n" \
    "  [g] generate shopping list\n" \
    "  [q] quit"

    while True:
        print(header)
        print(commands_list)

        cmd = input("> ").strip()

        if cmd == "q":
            break

        elif cmd == "r":
            # list recipies
            [print(str(r)) 
             for r in recipes.list_recipes(groceryLoader)]
            
        elif cmd == "p":
            # list pantry
            [print(str(i)) 
             for i in pantry.list_items(groceryLoader)]

        elif cmd == "m":
            # show meal plan
            [print(f"{m[0]}: {m[1]}") for m in planner.list_items(groceryLoader)]

        elif cmd == "a":
            # add to meal plan
            [print(f"{m[0]}: {m[1]}") for m in planner.list_items(groceryLoader)]
            r = input("Input recipie to add or modify: ")
            a = input("Input number of portions, [+/-] for delta: ")
            delta = False
            if a.startswith('+') or a.startswith('-'):
                delta = True
            print(planner.adjust_portions(groceryLoader, r, int(a), delta))
            
        elif cmd == "d":
            # remove from meal plan
            r = input("Input recipie to remove: ")
            print(planner.remove_item(groceryLoader, r))

        elif cmd == "g":
            # generate shopping list
            shopping_list = planner.generate_shopping_list(groceryLoader)
            for n, v in shopping_list.items():
                print(f"{n}: {v["quantity"]} {v["unit"]}")

if __name__ == "__main__":
    main()
