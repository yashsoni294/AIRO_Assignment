from pydantic import BaseModel, Field
from typing import Optional, Any, List

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query from user")
    top_k: Optional[int] = Field(5, description="Limit number of rows returned")
    debug: Optional[bool] = Field(False, description="Return intermediate steps")

class QueryResponse(BaseModel):
    success: bool
    query: str
    sql_query: Optional[str] = None
    result: Optional[List[Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
