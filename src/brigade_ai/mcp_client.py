import asyncio
import json

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from typing import Any

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

        chop = next(tool for tool in tools if tool.name == "chop")
        mix = next(tool for tool in tools if tool.name == "mix")
        cook = next(tool for tool in tools if tool.name == "cook")

        result = await chop.ainvoke(
            {
                "ingredient": "onion",
                "style": "finely diced",
            }
        )

        text = result[0]["text"]
        parsed = json.loads(text)

        print(type(result))  # list
        print(type(text))    # str
        print(type(parsed))  # dict

        print(parsed["action"])
        print(parsed["ingredient"])
        print(parsed["status"])
        print(parsed["action_number"])

        result = await chop.ainvoke(
            {
                "ingredient": "carrot",
                "style": "julienned",
            }
        )

        text = result[0]["text"]
        parsed = json.loads(text)

        print(parsed["action"])
        print(parsed["ingredient"])
        print(parsed["status"])
        print(parsed["action_number"])

        result = await mix.ainvoke(
            {
                "ingredients": ["onion", "carrot"],
            }
        )

        text = result[0]["text"]
        parsed = json.loads(text)

        print(parsed["action"])
        print(parsed["ingredients"])
        print(parsed["status"])
        print(parsed["action_number"])

        result = await cook.ainvoke(
            {
                "ingredients": ["onion", "carrot"],
            }
        )

        text = result[0]["text"]
        parsed = json.loads(text)

        print(parsed["action"])
        print(parsed["ingredients"])
        print(parsed["status"])
        print(parsed["action_number"])

def _parse_tool_result(result: list[dict[str, Any]]) -> dict[str, Any]:
    text_block = next (
        (
            block
            for block in result
            if block.get("type") == "text"
        ),
    )

    if text_block is None:
        raise ValueError("The MCP result did not contain a text block")

    text = text_block.get("text")

    if not isinstance(text, str):
        raise ValueError("The MCP text block did not contain a string")

    parsed = json.loads(text)

    if not isinstance(parsed, dict):
        raise ValueError("The MCP tool dod not return a JSON object")

    return parsed


if __name__ == "__main__":
    asyncio.run(main())
