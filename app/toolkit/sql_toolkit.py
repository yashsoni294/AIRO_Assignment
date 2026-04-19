import logging
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from app.config.settings import settings

logger = logging.getLogger(__name__)

def get_sql_toolkit():
    """
    Initialize SQLDatabaseToolkit
    """
    logger.info("Initializing SQL toolkit")
    
    # Database connection
    logger.info(f"Connecting to database with URL: {settings.DATABASE_URL}")
    db = SQLDatabase.from_uri(settings.DATABASE_URL)
    logger.info("Database connection established")
    
    # LLM
    logger.info(f"Initializing LLM with model: {settings.OPENAI_MODEL}")
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY
    )
    logger.info("LLM initialized successfully")
    
    # Toolkit
    logger.info("Creating SQL database toolkit")
    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )
    logger.info("SQL toolkit created successfully")
    
    return toolkit