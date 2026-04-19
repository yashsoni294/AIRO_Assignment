import logging
from app.toolkit.agent import get_sql_agent
from app.toolkit.sql_callback_handler import SQLCallbackHandler
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

def agent_node(state: GraphState) -> GraphState:
    """
    LangGraph node that uses LangChain SQL Agent with SQL callback extraction
    """

    logger.info("Starting agent node")

    try:
        # 🔹 Initialize agent
        logger.info("Initializing SQL agent")
        agent = get_sql_agent()

        user_query = state["query"]
        logger.info(f"Processing user query: '{user_query}'")

        if state.get("steps") is not None:
            state["steps"].append("Agent started")

        # 🔥 Initialize SQL callback
        sql_callback = SQLCallbackHandler()

        # 🔥 Invoke agent with callback
        logger.info("Invoking SQL agent with callback")
        response = agent.invoke(
            {"input": user_query},
            config={"callbacks": [sql_callback]}
        )

        logger.info("Agent invocation completed")

        # 🔹 Store raw response
        state["raw_agent_output"] = response

        # 🔹 Extract final answer
        output = response.get("output")
        state["result"] = [{"response": output}]

        logger.info(f"Agent final output: {output}")

        # 🔥 Primary: Get SQL from callback
        extracted_sql = sql_callback.get_last_query()

        # 🔁 Fallback: Try intermediate steps (safety net)
        if not extracted_sql:
            logger.warning("Callback did not capture SQL, trying fallback extraction")

            intermediate_steps = response.get("intermediate_steps", [])

            for step in intermediate_steps:
                try:
                    action, _ = step

                    if hasattr(action, "tool_input"):
                        tool_input = action.tool_input

                        if isinstance(tool_input, str) and "select" in tool_input.lower():
                            extracted_sql = tool_input
                            logger.info(f"Fallback SQL extracted: {extracted_sql}")
                            break

                except Exception as parse_error:
                    logger.warning(f"Failed to parse step: {parse_error}")

        # 🔹 Save SQL if found
        if extracted_sql:
            state["sql_query"] = extracted_sql
            logger.info(f"Final SQL captured: {extracted_sql}")
        else:
            logger.warning("No SQL query could be captured")

        # 🔹 Track step
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