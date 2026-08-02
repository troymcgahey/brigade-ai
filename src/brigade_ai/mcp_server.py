from mcp.server.fastmcp import FastMCP
from itertools import count

mcp = FastMCP("Brigade Kitchen")

action_numbers = count(1)

@mcp.tool()
def chop(ingredient: str, style: str) -> dict[str, object]:
    """Chop an ingredient using the requested cutting style."""
    return {
        "action": "chop",
        "ingredient": ingredient,
        "style": style,
        "status": "completed",
        "action_number": next(action_numbers)
    }

@mcp.tool()
def mix(ingredients: [str]) -> dict[str, object]:
    return {
            "action": "mix",
            "ingredients": ingredients,
            "status": "completed",
            "action_number": next(action_numbers),
    }

@mcp.tool()
def cook(ingredients: [str]) -> dict[str, object]:
    return {
        "action": "cook",
        "ingredients": ingredients,
        "status": "completed",
        "action_number": next(action_numbers),
    }

def main() -> None:
    #TODO: Run the server over stdio.
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


