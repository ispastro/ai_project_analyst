from langgraph.graph import StateGraph, END
from pipeline.state import ProjectState
from pipeline.nodes import (
    extract_key_points,
    generate_requirements,
    generate_user_stories,
    suggest_tech_stack,
    estimate_timeline,
)


def build_graph():
    graph = StateGraph(ProjectState)

    # Register nodes
    graph.add_node("extract_key_points", extract_key_points)
    graph.add_node("generate_requirements", generate_requirements)
    graph.add_node("generate_user_stories", generate_user_stories)
    graph.add_node("suggest_tech_stack", suggest_tech_stack)
    graph.add_node("estimate_timeline", estimate_timeline)

    # Define edges (execution order)
    graph.set_entry_point("extract_key_points")
    graph.add_edge("extract_key_points", "generate_requirements")
    graph.add_edge("generate_requirements", "generate_user_stories")
    graph.add_edge("generate_user_stories", "suggest_tech_stack")
    graph.add_edge("suggest_tech_stack", "estimate_timeline")
    graph.add_edge("estimate_timeline", END)

    return graph.compile()