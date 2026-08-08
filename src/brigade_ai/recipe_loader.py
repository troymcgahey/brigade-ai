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

    return self
    #TODO:
    # 1. Collect each step.number
    # 2. Construct the expected sequence: [1, 2, ..., len(steps)].
    # 3. Raise ValueError if the actual sequence differs.
    # 4. Return self.

def load_recipe(path: Path) -> Recipe:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return Recipe.model_validate(data)
