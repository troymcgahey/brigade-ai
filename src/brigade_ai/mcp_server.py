from mcp.server.fastmcp import FastMCP
from itertools import count

mcp = FastMCP("Brigade Kitchen")

action_numbers = count(1)

@mcp.tool()
def chop(ingredient: str, style: str) -> dict[str, object]:
    """Chop an ingredient using the requested cutting style."""
    return _completed_action(
        "chop",
        "completed",
        next(action_numbers),
        ingredient=ingredient,
        style=style,
    )

@mcp.tool()
def mix(ingredient: list[str], method: str) -> dict[str, object]:
    """Mix the ingredient using the requested mixing method."""
    return _completed_action(
        "mix",
        "completed",
        next(action_numbers),
        ingredient=ingredient,
        method=method,
    )

@mcp.tool()
def cook(ingredient: str, method: str, minutes: Annotated[int, Field(gt=0, le=240)]) -> dict[str, object]:
    """Cook the ingredient for the requesed number of minutes."""
    return _completed_action(
        "cook",
        "completed",
        next(action_numbers),
        ingredient=ingrediant,
        method=method,
        minutes=minutes,
    )

@mcp.tool()
def stir(ingredient: str, duration_seconds: Annotated[int, Field(gt=0, le=600)]) -> dict[str, object]:
    """Stir the ingredient for the requested duration in seconds."""
    return _completed_action(
        "stir",
        "completed",
        next(action_numbers),
        ingredient=ingredient,
        duration_seconds=duration_seconds,
        

def _completed_action(action: str, status: str, action_number: int **details: object) -> dict[str, object]:



def main() -> None:
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


