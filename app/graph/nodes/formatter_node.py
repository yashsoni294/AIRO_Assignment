from app.graph.state import GraphState
from langchain_openai import ChatOpenAI
from app.config.settings import settings

# Initialize LLM once
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=0.7,  # slightly higher for natural responses
    api_key=settings.OPENAI_API_KEY
)

def formatter_node(state: GraphState) -> GraphState:
    """
    Final node to format output before returning response
    """

    try:
        if state.get("steps") is not None:
            state["steps"].append("Formatter started")

        # If error exists
        if state.get("error"):
            state["result"] = None

            if state.get("steps") is not None:
                state["steps"].append("Error detected, formatting error response")

            return state

        # Handle GENERAL queries using LLM
        if state.get("intent") == "general":
            user_query = state.get("query")

            response = llm.invoke(f"""
            You are a helpful AI assistant.

            Respond naturally and conversationally.

            User: {user_query}
            """)

            state["result"] = [{
                "response": response.content
            }]

            if state.get("steps") is not None:
                state["steps"].append("General response generated")

            return state

        # DB flow (unchanged)
        if not state.get("result"):
            state["result"] = [{"message": "No data found"}]

        # Debug mode
        if state.get("debug"):
            state["result"] = {
                "data": state["result"],
                "sql_query": state.get("sql_query"),
                "steps": state.get("steps"),
                "raw_agent_output": state.get("raw_agent_output")
            }

        if state.get("steps") is not None:
            state["steps"].append("Formatter completed")

        return state

    except Exception as e:
        state["error"] = f"Formatter error: {str(e)}"

        if state.get("steps") is not None:
            state["steps"].append("Formatter failed")

        return state