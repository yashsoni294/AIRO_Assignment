import logging
from fastapi import APIRouter, HTTPException
import time

from app.api.schemas import QueryRequest, QueryResponse
from app.services.sql_service import run_text_to_sql

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_sql(request: QueryRequest):
    logger.info(f"Received query request: '{request.query}' with top_k={request.top_k}, debug={request.debug}")
    start_time = time.time()

    try:
        logger.info("Calling run_text_to_sql service")
        result = run_text_to_sql(
            query=request.query,
            top_k=request.top_k,
            debug=request.debug
        )

        execution_time = round(time.time() - start_time, 3)
        logger.info(f"Query completed successfully in {execution_time}s")
        return QueryResponse(
            success=True,
            query=request.query,
            sql_query=result.get("sql_query"),
            result=result.get("result"),
            execution_time=execution_time
        )
    except Exception as e:
        logger.error(f"Query failed with error: {str(e)}")
        return QueryResponse(
            success=False,
            query=request.query,
            error=str(e)
        )

@router.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "ok"}
