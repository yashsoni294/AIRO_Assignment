import streamlit as st
import requests
import time

# API URL
API_URL = "http://127.0.0.1:8000/api/query"

st.set_page_config(page_title="Text-to-SQL", layout="wide")

st.title("Text-to-SQL Chatbot")
st.markdown("Ask questions about your database in natural language")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your database...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "query": user_input,
                        "top_k": 5,
                        "debug": False
                    }
                )

                data = response.json()

                if data["success"]:
                    result = data.get("result")

                    # Handle both debug/non-debug
                    if isinstance(result, dict):
                        answer = result.get("data", result)
                    else:
                        answer = result

                    # 🔹 Display answer
                    if isinstance(answer, list):
                        st.dataframe(answer)
                    else:
                        st.markdown(answer)

                    # Show SQL (optional)
                    if data.get("sql_query"):
                        with st.expander("🧾 SQL Query"):
                            st.code(data["sql_query"], language="sql")

                else:
                    answer = data.get("error", "Something went wrong")
                    st.error(answer)

            except Exception as e:
                answer = f"Error: {str(e)}"
                st.error(answer)

            end_time = time.time()
            st.caption(f"⏱ Response time: {round(end_time - start_time, 2)}s")

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": str(answer)
    })