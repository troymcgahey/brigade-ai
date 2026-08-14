import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from brigade_ai.chef_graph import build_graph

async def main() -> None:
    client = MultiServerMCPClient(
        {
            "kitchen": {
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    "-m",
                    "brigade_ai.mcp_server",
                ],
                "transport": "stdio",
            }
        }
    )

    async with client.session("kitchen") as session:
        tools = await load_mcp_tools(session)
    
        tools_by_name = {
                tool.name: tool
                for tool in tools
        }

        chef_graph = build_graph(tools_by_name)

        result = await chef_graph.ainvoke(
            {
                "request": "Prepare herb chicken",
                "recipe_path": (
                    "skills/prepare-herb-chicken/"
                    "references/recipe.json"
                ),
            }
        )

        print(result["final_report"])

if __name__ == "__main__":
    asyncio.run(main())
