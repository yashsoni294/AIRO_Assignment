import logging
from typing import Dict, Any
from app.graph.builder import get_graph

logger = logging.getLogger(__name__)

def run_text_to_sql(query: str, top_k: int, debug: bool, database_url: str) -> Dict[str, Any]:
    """
    Main service function that handles the full Text-to-SQL flow using LangGraph
    """
    logger.info(f"Starting Text-to-SQL processing for query: '{query}' with top_k={top_k}, debug={debug}")
    
    # Initial Graph State
    state = {
        "query": query,
        "top_k": top_k,
        "database_url": database_url,
        "sql_query": None,
        "result": None,
        "error": None,
        "debug": debug,
        "steps": []
    }
    
    logger.info("Initializing LangGraph workflow")

    try:
        # Initialize Graph
        graph = get_graph()
        logger.info("Graph initialized successfully")

        # Execute Graph
        logger.info("Executing graph workflow")
        final_state = graph.invoke(state)
        logger.info("Graph execution completed")

        # Handle Errors from Graph
        if final_state.get("error"):
            logger.error(f"Graph execution failed with error: {final_state.get('error')}")
            return {
                "sql_query": final_state.get("sql_query"),
                "result": None,
                "error": final_state.get("error")
            }

        # Success Response
        logger.info("Text-to-SQL processing completed successfully")
        return {
            "sql_query": final_state.get("sql_query"),
            "result": final_state.get("result")
        }

    except Exception as e:
        # Fallback error (system-level failure)
        logger.error(f"Service-level error occurred: {str(e)}")
        return {
            "sql_query": None,
            "result": None,
            "error": f"Service error: {str(e)}"
        }