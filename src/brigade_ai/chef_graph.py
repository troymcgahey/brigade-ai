from typing import TypedDict
from langgraph.graph import END, START, StateGraph

class ChefState(TypedDict, total=False):
    request: str
    ingredient: str
    chop_style: str
    cook_method: str
    cook_minutes: int
    plan_summary: str


def plan_recipe(state: ChefState) -> dict[str, object]:
    return {
            "ingredient": "chicken breast",
            "chop_style": "bite-sized pieces",
            "cook_method": "plan sear",
            "cook_minutes": 12,
    }

def summarize_plan(state: ChefState) -> dict[str, str]:
    summary = "Prepare chicken breast as bite-sized pieces, then pan sear it for 12 minutes."

    return {"plan_summary": summary}

def build_graph():
    builder = StateGraph(ChefState)

    builder.add_node("plan_recipe", plan_recipe)
    builder.add_node("summarize_plan", summarize_plan)

    builder.add_edge(START, "plan_recipe")
    builder.add_edge("plan_recipe", "summarize_plan")
    builder.add_edge("summarize_plan", END)

    return builder.compile()

def main() -> None:
    chef_graph = build_graph()

    result = chef_graph.invoke(
        {"reqeust": "Make a simple chicken dinner"}
    )

    print(result)

if __name__ == "__main__":
    main()
