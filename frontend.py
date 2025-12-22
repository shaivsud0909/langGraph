import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])    

thread_id='1'
CONFIG={'configurable':{'thread_id':thread_id}}

# {'role':'user','content':'hi'}

# with st.chat_message('user'):
#     st.text('hi')

# with st.chat_message('assistant'):
#     st.text('Hi,How are u?')    

user_input=st.chat_input("type here")    

if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
     
    response=chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)
    assistant_text = response['messages'][-1].content[0]["text"]
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': assistant_text})   
    with st.chat_message('assistant'):
        st.text(assistant_text)    
