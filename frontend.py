import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#utility fuctions
def genrate_thread_id():
    thread_id=uuid.uuid4()  
    return thread_id  #random thread

def reset_chat():
    thread_id= genrate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])# if reset we need to add the thread
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

#session setup
if "message_history" not in st.session_state:
    st.session_state["message_history"] = [] # history

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=genrate_thread_id() # genrate new thtread for new chat

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[] #adding thread to the side bar

add_thread(st.session_state['thread_id']) #calling the add function

#side bar ui
st.sidebar.title("langGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My conversations")

for thread_id in st.session_state['chat_threads']:
    st.sidebar.button(str(thread_id))


# Render history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


CONFIG = {"configurable": {"thread_id":st.session_state['thread_id']}}

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
