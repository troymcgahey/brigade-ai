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
        self._skills.clear()

        for directory in self.skills_root.iterdir():
            if not directory.is_dir():
                continue
            
            skill_path = directory / "SKILL.md"

            if not skill_path.is_file():
                continue

            recipe_path = directory / "references" / "recipe.json"

            if not recipe_path.is_file():
                continue

            recipe = load_recipe(recipe_path)

            recipe_skill = RecipeSkill( 
                name=directory.name,
                directory=directory,
                skill_path=skill_path,
                recipe_path=recipe_path,
                recipe=recipe,
            )

            self._skills[directory.name] = recipe_skill 

    def get(self, name: str) -> RecipeSkill:
        """Returns the requested skill. Raises error if skill cannot be found."""
        
        skill = self._skills.get(name)

        if skill is None:
            available = ", ".join(sorted(self._skills))
            raise ValueError(
                f"Unknown recipe skill {name!r}. "
                f"Available skills: {available or 'none'}"
            )

        return skill

    def list_skills(self) -> list[RecipeSkill]:
        """Returns a list of RecipeSkills sorted by name ascending."""
        return [
            self._skills[name] for name in sorted(self._skills)
        ]

def main():
    registry = SkillRegistry(Path("skills"))
    registry.discover()

    for skill in registry.list_skills():
        print(skill.name, "-", skill.recipe.name)

    try:
        skill = registry.get("does-not-exist")
        print(skill.recipe_path)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

