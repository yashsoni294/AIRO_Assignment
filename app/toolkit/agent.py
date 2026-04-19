import logging
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from app.toolkit.sql_toolkit import get_sql_toolkit

logger = logging.getLogger(__name__)

def get_sql_agent():
    """
    Create SQL Agent using LangChain toolkit
    """
    logger.info("Creating SQL agent")
    toolkit = get_sql_toolkit()
    logger.info("SQL toolkit obtained")

    agent = create_sql_agent(
        llm=toolkit.llm,
        toolkit=toolkit,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    logger.info("SQL agent created successfully")

    return agent