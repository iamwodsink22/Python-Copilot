import streamlit as st
import time
from base import BaseAgent
a=BaseAgent()
st.title("Python Assistant using LangChain")
if 'messages' not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message['role']):
      st.markdown(message['content'])

if prompt :=st.chat_input("What do you want to know about python?"):
    with st.chat_message('User'):
        st.markdown(prompt)
    st.session_state.messages.append({'role':'User','content':prompt})
    response=a.chat(prompt)
    with st.chat_message('Assistant'):
        container = st.empty()
        txt=''
        for char in response:
            txt+=char
            container.markdown(f"{txt}")
            time.sleep(0.01)
            
            
       
    st.session_state.messages.append({'role':'Assistant','content':response})
        
    
