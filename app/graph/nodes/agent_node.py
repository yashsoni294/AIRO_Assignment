import logging
from app.toolkit.agent import get_sql_agent
from app.graph.state import GraphState

logger = logging.getLogger(__name__)


def agent_node(state: GraphState) -> GraphState:
    """
    LangGraph node that uses LangChain SQL Agent to generate + execute SQL
    """

    logger.info("Starting agent node")

    try:
        # Initialize agent
        logger.info("Initializing SQL agent")
        agent = get_sql_agent()

        user_query = state["query"]
        logger.info(f"Processing user query: '{user_query}'")

        if state.get("steps") is not None:
            state["steps"].append("Agent started")

        # IMPORTANT: invoke with intermediate steps
        logger.info("Invoking SQL agent with intermediate steps")
        response = agent.invoke({
            "input": user_query
        })

        logger.info("Agent invocation completed")

        # 🔹 Store raw response
        state["raw_agent_output"] = response

        # 🔹 Extract final answer
        output = response.get("output")
        state["result"] = [{"response": output}]

        logger.info(f"Agent final output: {output}")

        # NEW: Extract SQL from intermediate steps
        extracted_sql = None

        intermediate_steps = response.get("intermediate_steps", [])

        logger.info(f"Intermediate steps count: {len(intermediate_steps)}")

        for step in intermediate_steps:
            try:
                action, observation = step

                # Tool input usually contains SQL
                if hasattr(action, "tool_input"):
                    tool_input = action.tool_input

                    if isinstance(tool_input, str) and "select" in tool_input.lower():
                        extracted_sql = tool_input
                        logger.info(f"Extracted SQL: {extracted_sql}")
                        break

            except Exception as parse_error:
                logger.warning(f"Failed to parse step: {parse_error}")

        # Save SQL if found
        if extracted_sql:
            state["sql_query"] = extracted_sql
        else:
            logger.warning("No SQL query could be extracted")

        # Track step
        if state.get("steps") is not None:
            state["steps"].append("Agent completed")

        logger.info("Agent node completed successfully")
        return state

    except Exception as e:
        logger.error(f"Agent node failed with error: {str(e)}")

        state["error"] = f"Agent error: {str(e)}"

        if state.get("steps") is not None:
            state["steps"].append("Agent failed")

        return state