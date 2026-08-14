import operator
import json

from typing import TypedDict, Annotated, Literal
from collections.abc import Mapping
from langgraph.graph import END, START, StateGraph
from langchain_core.tools import BaseTool

from brigade_ai.recipe_loader import Recipe, load_recipe
from pathlib import Path

class ChefState(TypedDict, total=False):
    request: str
    recipe_path: str
    recipe: Recipe
    current_step_index: int
    action_log: Annotated[
        list[dict[str, object]], 
        operator.add
    ]
    final_report: str


def load_recipe_node(state: ChefState) -> dict[str, object]:
    recipe_path = Path(state["recipe_path"])
    recipe = load_recipe(recipe_path)

    return {
        **state,
        "recipe": recipe,
        "current_step_index": 0,
        "action_log": [],
    }

def summarize_meal(state: ChefState) -> dict[str, object]:

    report = f"{state["recipe"].name} completed for {state["recipe"].servings}.\nActions:"

    for action in state["action_log"]:
        report += f"\n{action["action_number"]}. {action["action"]} - {action["status"]}"

    return {
        **state,
        "final_report": report,
    }

def route_after_step(state: ChefState) -> Literal["more_steps", "complete"]:
    if state["current_step_index"] < len(state["recipe"].steps):
        return "more_steps"

    return "complete"

def build_graph(tools: Mapping[str, BaseTool]):
    builder = StateGraph(ChefState)

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

        return {
            **state,
            "action_log": [parsed_result],
            "current_step_index": step_index + 1,
        }

    builder.add_node("load_recipe", load_recipe_node)
    builder.add_node("execute_step", execute_step)
    builder.add_node("summarize_meal", summarize_meal)

    builder.add_edge(START, "load_recipe")
    builder.add_edge("load_recipe", "execute_step")
    builder.add_edge("summarize_meal", END)

    builder.add_conditional_edges(
        "execute_step",
        route_after_step,
        {
            "more_steps": "execute_step",
            "complete": "summarize_meal",
        },
    )

    return builder.compile()

def main() -> None:
    chef_graph = build_graph()

    print(result)

if __name__ == "__main__":
    main()
