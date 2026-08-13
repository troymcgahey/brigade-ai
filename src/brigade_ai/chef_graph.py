import operator
import json

from typing import TypedDict, Annotated
from collections.abc import Mapping
from langgraph.graph import END, START, StateGraph
from langchain_core.tools import BaseTool

from brigade_ai.recipe_loader import Recipe
from pathlib import Path

class ChefState(TypedDict, total=False):
    request: str
    recipe_path: str
    recipe: Recipe
    current_step_index: int
    action_log: Annotated[list[dict[str, object]], operator.add]
    final_report: str


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

def load_recipe_node(state: ChefState) -> dict{str, object]:
    # Read state["recipe_path"].
    # Convert it into a Path.
    # Call load_recipe().
    # Initialize current_step_index to zero.
    # Initialize action_log to an empty list.

def build_graph(tools: Mapping[str, BaseTool]):
    builder = StateGraph(ChefState)

    builder.add_node("load_recipe", load_recipe)

    async def execute_step(
        state: ChefState,
    ) -> dict[str, object]:

        recipe = state["recipe"]
        step_index = state["current_step_index"]
        step = recipe.steps[step_index]
        tool = tools[step.tool]

        raw_result = await tool.ainvoke(step.arguments)

        text = raw_result[0]["text"]
        parsed_result = json.loads(text)

    return builder.compile()

def main() -> None:
    chef_graph = build_graph()

    result = chef_graph.invoke(
        {"request": "Make a simple chicken dinner"}
    )

    print(result)

if __name__ == "__main__":
    main()
