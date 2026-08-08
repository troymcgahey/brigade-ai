from pathlib import Path

from brigade_ai.recipe_loader import load_recipe

def main() -> None:
    recipe_path = Path("skills/prepare-herb-chicken/references/recipe.json")

    recipe = load_recipe(recipe_path)

    print("Recipe: ", recipe)
    print("Name: ", recipe.name)
    print(f"Name: {recipe.steps[0].tool}")
    print("First arguments: ", recipe.steps[0].arguments)

if __name__ == "__main__":
    main()
        

