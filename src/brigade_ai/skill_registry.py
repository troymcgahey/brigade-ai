from pathlib import Path
from pydantic import BaseModel
from brigade_ai.recipe_loader import load_recipe, Recipe

class RecipeSkill(BaseModel):
    name: str
    directory: Path
    skill_path: Path
    recipe_path: Path
    recipe: Recipe

class SkillRegistry:
    def __init__(self, skills_root: Path):
        self.skills_root = skills_root
        self._skills: dict[str, RecipeSkill] = {}

    def discover(self) -> None:
        for directory in self.skills_root.iterdir():
            if not directory.is_dir():
                continue
            
            skill_path = directory / "SKILL.md"

            if not skill_path.is_file():
                continue

            recipe_path = directory / "references" / "recipe.json"

            recipe = load_recipe(recipe_path)

            recipeSkill = {
                "name": recipe.name,
                "directory": directory,
                "skill_path": skill_path,
                "recipe_path": recipe_path,
                "recipe": recipe,
            }

            self._skills[directory] = recipeSkill 

    def get(self, name: str) -> RecipeSkill:
        """Returns the requested skill. Raises error if skill cannot be found."""

        return self._skills[name]

    def list_skills(self) -> list[RecipeSkill]:
        """Returns all skills sorted by name."""

        skills = []
        for key in sorted(self._skills.keys()):
            skills.append(self._skills[key])

        return skills

def main():
    registry = SkillRegistry(Path("skills"))
    registry.discover()

    for skill in registry.list_skills():
        print(f"SSSSSSSSS----------- {skill} ------------SSSSSSSSSSSS")
        print(skill["name"], "-", skill["recipe"].Recipe.name)

    herb_chicken = registry.get("prepare-herb-chicken")
    print(herb_chicken)


if __name__ == "__main__":
    main()

