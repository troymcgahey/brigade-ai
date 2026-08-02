from mcp.server.fastmcp import FastMCP
from itertools import count
from typing import Annotated
from pydantic import Field

mcp = FastMCP("Brigade Kitchen")

action_numbers = count(1)

def _completed_action(
        action: str, 
        action_number: int, 
        **details: object,
) -> dict[str, object]:
    return {
        "action": action,
        "status": "completed",
        "action_number": action_number,
        **details,
    }

@mcp.tool()
def chop(ingredient: str, style: str) -> dict[str, object]:
    """Chop an ingredient using the requested cutting style."""
    return _completed_action(
        "chop",
        next(action_numbers),
        ingredient=ingredient,
        style=style,
    )

@mcp.tool()
def mix(ingredients: list[str], method: str) -> dict[str, object]:
    """Mix the ingredient using the requested mixing method."""
    return _completed_action(
        "mix",
        next(action_numbers),
        ingredients=ingredients,
        method=method,
    )

@mcp.tool()
def cook(ingredient: str, method: str, minutes: Annotated[int, Field(gt=0, le=240)]) -> dict[str, object]:
    """Cook the ingredient for the requested number of minutes."""
    return _completed_action(
        "cook",
        next(action_numbers),
        ingredient=ingredient,
        method=method,
        minutes=minutes,
    )

@mcp.tool()
def stir(ingredient: str, duration_seconds: Annotated[int, Field(gt=0, le=600)]) -> dict[str, object]:
    """Stir the ingredient for the requested duration in seconds."""
    return _completed_action(
        "stir",
        next(action_numbers),
        ingredient=ingredient,
        duration_seconds=duration_seconds,
    )

def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


