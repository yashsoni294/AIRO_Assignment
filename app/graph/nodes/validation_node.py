import logging
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

FORBIDDEN_KEYWORDS = [
"DELETE",
"UPDATE",
"INSERT",
"DROP",
"ALTER",
"TRUNCATE"
]

def validation_node(state: GraphState) -> GraphState:
    """
    Validate SQL query for safety before execution
    """
    logger.info("Starting validation node")
    try:
        if state.get("steps") is not None:
            state["steps"].append("Validation started")

        sql_query = state.get("sql_query")
        logger.info(f"Validating SQL query: {sql_query}")

        # If no SQL found, skip validation
        if not sql_query:
            logger.info("No SQL query found, skipping validation")
            if state.get("steps") is not None:
                state["steps"].append("No SQL to validate (skipped)")
            return state

        upper_sql = sql_query.upper()

        # Block dangerous operations
        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in upper_sql:
                logger.warning(f"Unsafe query detected: {keyword} not allowed")
                state["error"] = f"Unsafe query detected: {keyword} not allowed"

                if state.get("steps") is not None:
                    state["steps"].append(f"Blocked query due to {keyword}")

                return state

        # Optional: enforce LIMIT
        if "LIMIT" not in upper_sql:
            top_k = state.get("top_k", 5)
            state["sql_query"] = sql_query.strip().rstrip(";") + f" LIMIT {top_k};"
            logger.info(f"LIMIT clause enforced: LIMIT {top_k}")

            if state.get("steps") is not None:
                state["steps"].append("LIMIT enforced")

        if state.get("steps") is not None:
            state["steps"].append("Validation passed")

        logger.info("Validation node completed successfully")
        return state

    except Exception as e:
        logger.error(f"Validation node failed with error: {str(e)}")
        state["error"] = f"Validation error: {str(e)}"

        if state.get("steps") is not None:
            state["steps"].append("Validation failed")

        return state
