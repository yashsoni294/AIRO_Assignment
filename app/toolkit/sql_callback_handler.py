from langchain_core.callbacks import BaseCallbackHandler

class SQLCallbackHandler(BaseCallbackHandler):
    """
    Custom callback to capture SQL queries from SQL agent
    """

    def __init__(self):
        self.sql_queries = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        """
        Triggered when a tool is called
        """

        tool_name = serialized.get("name", "")

        # SQL agent uses this tool internally
        if "sql_db_query" in tool_name or "query_sql_db" in tool_name:
            self.sql_queries.append(input_str)

    def get_last_query(self):
        if self.sql_queries:
            return self.sql_queries[-1]
        return None
