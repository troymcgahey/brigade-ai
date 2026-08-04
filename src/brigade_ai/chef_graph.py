import operator
import json

from typing import TypedDict, Annotated
from collections.abc import Mapping
from langgraph.graph import END, START, StateGraph
from langchain_core.tools import BaseTool

class ChefState(TypedDict, total=False):
    request: str
    ingredient: str
    chop_style: str
    cook_method: str
    cook_minutes: int
    plan_summary: str
    action_log: Annotated[list[dict[str, object]], operator.add]


def plan_recipe(state: ChefState) -> dict[str, object]:
    return {
            "ingredient": "chicken breast",
            "chop_style": "bite-sized pieces",
            "cook_method": "pan sear",
            "cook_minutes": 12,
    }

def summarize_plan(state: ChefState) -> dict[str, str]:
    summary = (
        f"Prepare {state['ingredient']} as {state['chop_style']}, "
        f"then {state['cook_method']} it for "
        f"{state['cook_minutes']} minutes."
    )

    return {"plan_summary": summary}

def build_graph(tools: Mapping[str, BaseTool]):
    builder = StateGraph(ChefState)

    async def chop_ingredient(
        state: ChefState,
    ) -> dict[str, list[dict[str, object]]]:
        result = await tools['chop'].ainvoke(
            {
                "ingredient": state['ingredient'],
                "style": state['chop_style'],
            }
        )

        text = result[0]["text"]
        parsed_result = json.loads(text)

        return {
            "action_log": [parsed_result],
        }

    async def cook_ingredient(
        state: ChefState,
    ) -> dict[str, list[dict[str, object]]]:
        result = await tools['cook'].ainvoke(
            {
                "ingredient": state['ingredient'],
                "method": state['cook_method'],
                "minutes": state['cook_minutes'],
            }
        )

        text = result[0]["text"]
        parsed_result = json.loads(text)

        return {
            "action_log": [parsed_result],
        }

    builder.add_node("plan_recipe", plan_recipe)
    builder.add_node("summarize_plan", summarize_plan)

    builder.add_node("chop_ingredient", chop_ingredient)
    builder.add_node("cook_ingredient", cook_ingredient)

    builder.add_edge(START, "plan_recipe")
    builder.add_edge("plan_recipe", "chop_ingredient")
    builder.add_edge("chop_ingredient", "cook_ingredient")
    builder.add_edge("cook_ingredient", "summarize_plan")
    builder.add_edge("summarize_plan", END)

    return builder.compile()

def main() -> None:
    chef_graph = build_graph()

    result = chef_graph.invoke(
        {"request": "Make a simple chicken dinner"}
    )

    print(result)

if __name__ == "__main__":
    main()
