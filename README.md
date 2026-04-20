# Text-to-SQL AI Application

A sophisticated AI-powered application that converts natural language queries into SQL statements and executes them against your database. Built with FastAPI, LangGraph, LangChain, and Streamlit.

## Overview

This application provides both an API backend and a web interface for querying databases using natural language. It leverages OpenAI's language models through LangChain's SQL toolkit and uses LangGraph for workflow orchestration.

## Features

- **Natural Language to SQL**: Convert plain English questions into SQL queries
- **Multi-Database Support**: Works with PostgreSQL and MySQL
- **Safety Validation**: Built-in SQL injection protection and query validation
- **Interactive Web Interface**: Beautiful Streamlit-based chat interface
- **REST API**: FastAPI backend for programmatic access
- **Debug Mode**: Detailed execution tracing for development
- **Query Routing**: Intelligent classification between database and general queries

## Architecture

### Backend Components

- **FastAPI**: REST API server (`app/main.py`)
- **LangGraph Workflow**: Orchestrates the text-to-SQL pipeline (`app/graph/`)
- **SQL Agent**: LangChain-based SQL generation (`app/toolkit/`)
- **Validation Layer**: Security checks and query sanitization

### Frontend Components

- **Streamlit App**: Interactive chat interface (`app/streamlit_app.py`)
- **Real-time Communication**: API integration with visual feedback

## Project Structure

```
AIRO_Text_To_SQL_Assignment/
|
app/
|
|-- api/
|   |-- routes.py          # FastAPI endpoints
|   `-- schemas.py         # Pydantic models
|
|-- config/
|   `-- settings.py        # Application configuration
|
|-- graph/
|   |-- builder.py         # LangGraph workflow definition
|   |-- state.py           # Shared state management
|   `-- nodes/
|       |-- router_node.py        # Query intent classification
|       |-- agent_node.py         # SQL generation
|       |-- validation_node.py    # Security validation
|       `-- formatter_node.py     # Response formatting
|
|-- services/
|   `-- sql_service.py     # Main business logic
|
|-- toolkit/
|   |-- agent.py           # SQL agent factory
|   |-- sql_toolkit.py     # LangChain SQL toolkit
|   `-- sql_callback_handler.py  # SQL query extraction
|
|-- main.py                # FastAPI application entry
`-- streamlit_app.py       # Streamlit web interface
|
requirements.txt           # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL database
- OpenAI API key

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AIRO_Text_To_SQL_Assignment
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database
   ```

## Usage

### Running the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Running the Streamlit Interface

```bash
streamlit run app/streamlit_app.py
```

The web interface will be available at `http://localhost:8501`

### API Endpoints

#### Query Database
```http
POST /api/query
Content-Type: application/json

{
  "query": "Show me all users from California",
  "top_k": 10,
  "debug": false,
  "database_url": "postgresql://user:pass@localhost:5432/db"
}
```

#### Health Check
```http
GET /api/health
```

## Workflow Process

The application uses a sophisticated LangGraph workflow:

1. **Router Node**: Classifies user intent (database vs. general queries)
2. **Agent Node**: Generates SQL using LangChain's SQL toolkit
3. **Validation Node**: Ensures SQL safety and adds LIMIT clauses
4. **Formatter Node**: Formats response for output

### Query Types

- **Database Queries**: SQL-related questions about data, tables, records
- **General Queries**: Casual chat, greetings, general knowledge

## Security Features

- **SQL Injection Protection**: Blocks dangerous SQL keywords (DELETE, UPDATE, DROP, etc.)
- **Query Limiting**: Automatically adds LIMIT clauses to prevent excessive data retrieval
- **Input Validation**: Comprehensive validation of user inputs and generated queries

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `DATABASE_URL` | Database connection string | Required |

### Database Support

The application supports:
- **PostgreSQL**: `postgresql://user:pass@host:port/db`
- **MySQL**: `mysql+pymysql://user:pass@host:port/db`

## Development

### Debug Mode

Enable debug mode to see detailed execution traces:
```json
{
  "debug": true
}
```

### Logging

The application uses structured logging with different levels:
- Query processing steps
- SQL generation details
- Error tracking
- Performance metrics

## Example Queries

### Database Queries
- "Show me all users from California"
- "What are the top 5 most expensive products?"
- "How many orders were placed last month?"
- "List all employees in the sales department"

### General Queries
- "Hello, how are you?"
- "What's the weather like?"
- "Tell me a joke"

## Error Handling

The application provides comprehensive error handling:
- Database connection errors
- SQL parsing errors
- API rate limiting
- Invalid query formats

## Performance

- **Query Routing**: Intelligent intent classification reduces unnecessary processing
- **Caching**: SQL toolkit caches database schema information
- **Async Processing**: FastAPI provides async request handling
- **Connection Pooling**: Efficient database connection management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the application logs for detailed error information
- Verify database connectivity and credentials
- Ensure OpenAI API key is valid and has sufficient credits

## Technology Stack

- **Backend**: FastAPI, LangGraph, LangChain, SQLAlchemy
- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT models
- **Database**: PostgreSQL, MySQL
- **Python**: 3.8+

---

**Note**: This application is designed for read-only database operations. Write operations are blocked for security reasons.
