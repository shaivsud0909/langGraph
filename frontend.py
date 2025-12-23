import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Render history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

thread_id = "1"
CONFIG = {"configurable": {"thread_id": thread_id}}

user_input = st.chat_input("type here")

if user_input:
    # Save user message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.text(user_input)

    # STREAMING RESPONSE
    with st.chat_message("assistant"):
        placeholder = st.empty()
        assistant_text = ""
#chatbot.stream() returns an iterator that yields a tuple
# (message_chunk, metadata) on each step.
# We use message_chunk to render streamed text and usually ignore metadata.
        for message_chunk, metadata in chatbot.stream(   
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages",
        ):
            if message_chunk.content:
                chunk_text = message_chunk.content[0]["text"]
                assistant_text += chunk_text
                placeholder.text(assistant_text)

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": assistant_text}
    )
