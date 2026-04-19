from typing import TypedDict, Optional, List, Any

class GraphState(TypedDict, total=False):
    """
    Shared state across all LangGraph nodes
    """

    # User Input
    query: str
    top_k: int
    debug: bool

    # LLM / Agent Outputs
    sql_query: Optional[str]
    raw_agent_output: Optional[Any]

    # Execution Results
    result: Optional[List[Any]]

    # Metadata
    execution_time: Optional[float]

    # Error Handling
    error: Optional[str]

    # Debug / Trace (VERY IMPORTANT)
    steps: Optional[List[str]]

    intent: Optional[str]

    database_url: Optional[str]

