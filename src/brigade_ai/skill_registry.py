from pathlib import Path
from pydantic import BaseModel
from brigade_ai.recipe_loader import Recipe

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
            #

    def get(self, name: str) -> RecipeSkill:
        """Returns the requested skill. Raises error if skill cannot be found."""

    def list_skills(self) -> list[RecipeSkill]:
        """Returns all skills sorted by name."""
