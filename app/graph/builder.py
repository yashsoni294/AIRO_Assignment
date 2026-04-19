import logging
from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.nodes.router_node import router_node
from app.graph.nodes.agent_node import agent_node
from app.graph.nodes.validation_node import validation_node
from app.graph.nodes.formatter_node import formatter_node

logger = logging.getLogger(__name__)

def get_graph():
    """
    Build and return the LangGraph workflow with routing
    """
    logger.info("Building LangGraph workflow")

    builder = StateGraph(GraphState)

    # Add Nodes
    logger.info("Adding nodes: router, agent, validation, formatter")
    builder.add_node("router", router_node)
    builder.add_node("agent", agent_node)
    builder.add_node("validation", validation_node)
    builder.add_node("formatter", formatter_node)

    # Entry Point (UPDATED)
    logger.info("Setting entry point to 'router'")
    builder.set_entry_point("router")

    # Conditional Routing
    def route_decision(state: GraphState):
        intent = state.get("intent")

        logger.info(f"Routing decision based on intent: {intent}")

        if intent == "db":
            return "agent"
        else:
            return "formatter"

    builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "agent": "agent",
            "formatter": "formatter"
        }
    )

    # Existing Flow
    logger.info("Adding edges: agent -> validation -> formatter -> END")
    builder.add_edge("agent", "validation")
    builder.add_edge("validation", "formatter")
    builder.add_edge("formatter", END)

    # Compile Graph
    logger.info("Compiling graph")
    graph = builder.compile()

    logger.info("Graph built successfully with router")

    return graph