import json

from typing import Any, Literal
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from pathlib import Path

class RecipeStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    number: int = Field(gt=0)
    tool: Literal["chop", "mix", "stir", "cook"]
    arguments: dict[str, Any]

class Recipe(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    servings: int = Field(gt=0)
    steps: list[RecipeStep] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_step_order(self) -> Self:
        actual_numbers = [
            step.number
                for step in self.steps
        ]

        expected_numbers = list(
            range(1, len(self.steps) + 1)
        )

        if actual_numbers != expected_numbers:
            raise ValueError(
                "Recipe steps must be numbered sequentially "
                f"starting at 1; received {actual_numbers}"
            )

        return self

def load_recipe(path: Path) -> Recipe:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return Recipe.model_validate(data)
