from mcp.server.fastmcp import FastMCP
from itertools import count

mcp = FastMCP("Brigade Kitchen")

action_numbers = count()

@mcp.tool()
def chop(ingredient: str, style: str) -> dict[str, str]:
    """Chop an ingredient using the requested cutting style."""
    return {
        "action": "chop",
        "ingredient": ingredient,
        "style": style,
        "status": "completed",
        "action_numbers": str(next(action_numbers))
    }

def main() -> None:
    #TODO: Run the server over stdio.
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


