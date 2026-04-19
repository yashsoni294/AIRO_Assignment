from app.graph.state import GraphState
from langchain_openai import ChatOpenAI
from app.config.settings import settings

llm = ChatOpenAI(
model=settings.OPENAI_MODEL,
temperature=0,
api_key=settings.OPENAI_API_KEY
)

def router_node(state: GraphState) -> GraphState:
    """
    Classifies query intent:
    - db → database query
    - general → normal chat
    """
    query = state["query"]

    prompt = f"""
    Classify the user query into one of the following categories:

    1. db → if it's related to database (SQL, tables, data, records)
    2. general → greetings, casual chat, weather, general knowledge

    Only return ONE word: db or general

    Query: {query}
    """

    try:
        response = llm.invoke(prompt)
        intent = response.content.strip().lower()

        state["intent"] = intent

        if state.get("steps") is not None:
            state["steps"].append(f"Intent classified as: {intent}")

        return state

    except Exception as e:
        state["error"] = f"Router error: {str(e)}"
        return state
