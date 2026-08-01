from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Brigade Kitchen")

@mcp.tool()
def chop(ingredient: str, style: str) -> dict[str, str]:
    """Chop an ingredient using the requested cutting style."""
    return {
        "action": "chop",
        'ingredient': ingredient,
        'style': style,
        'status': "completed",
    }

def main() -> None:
    #TODO: Run the server over stdio.
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


