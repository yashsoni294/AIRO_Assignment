import streamlit as st
import requests
import time

# API URL
API_URL = "http://127.0.0.1:8000/api/query"

# Page Config
st.set_page_config(page_title="Text-to-SQL", layout="wide")

# Custom CSS (THIS IS THE MAGIC)
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.stChatMessage {
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

[data-testid="stChatMessageContent"] {
    font-size: 16px;
}

/* User bubble */
.stChatMessage[data-testid="stChatMessage-user"] {
    background-color: #1f2937;
}

/* Assistant bubble */
.stChatMessage[data-testid="stChatMessage-assistant"] {
    background-color: #111827;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Input box */
.stChatInput textarea {
    border-radius: 12px !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("## ⚙️ Database Settings")

db_type = st.sidebar.selectbox("🗄️ Database Type", ["postgresql", "mysql"])

host = st.sidebar.text_input("🌐 Host", value="localhost")
port = st.sidebar.text_input("🔌 Port", value="5432")
username = st.sidebar.text_input("👤 Username", value="postgres")
password = st.sidebar.text_input("🔒 Password", type="password")
database = st.sidebar.text_input("📦 Database Name", value="ResumeDB")

# Construct DB URL
if password:
    auth = f"{username}:{password}"
else:
    auth = username

if db_type == "postgresql":
    db_url = f"postgresql://{auth}@{host}:{port}/{database}"
else:
    db_url = f"mysql+pymysql://{auth}@{host}:{port}/{database}"

# HEADER
st.markdown("# 🧠 Text-to-SQL Chatbot")
st.markdown("💬 Ask questions about your database in natural language")

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT
user_input = st.chat_input("💡 Ask your database...")

if user_input:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧑‍💻 {user_input}"
    })

    with st.chat_message("user"):
        st.markdown(f"🧑‍💻 {user_input}")

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            start_time = time.time()

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "query": user_input,
                        "top_k": 5,
                        "debug": False,
                        "database_url": db_url
                    }
                )

                data = response.json()

                if data.get("success"):
                    result = data.get("result")

                    if isinstance(result, dict):
                        answer = result.get("data", result)
                    else:
                        answer = result

                    # Display answer
                    if isinstance(answer, list):
                        st.dataframe(answer)
                    else:
                        st.markdown(f"🤖 {answer}")

                    # SQL Section
                    if data.get("sql_query"):
                        with st.expander("🧾 View SQL Query"):
                            st.code(data["sql_query"], language="sql")

                else:
                    answer = data.get("error", "Something went wrong")
                    st.error(f"❌ {answer}")

            except Exception as e:
                answer = f"Error: {str(e)}"
                st.error(answer)

            end_time = time.time()
            st.caption(f"⚡ Response time: {round(end_time - start_time, 2)}s")

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🤖 {answer}"
    })