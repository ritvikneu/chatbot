import streamlit as st
from streamlit_chat import message
import os
from groq import Groq
import random
from langchain.chains import ConversationChain #conversation chain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory #memory
from langchain_groq import ChatGroq #llm system resides here and pass inference parameters
from langchain.prompts import PromptTemplate #prompt template

from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY")

def main():
    st.title("🗣️ Groq Chatbot")
    st.sidebar.title("🗣️ Groq Chatbot")
    st.subheader("㈻ Simple Chat Interface for Groq")

    model = st.sidebar.selectbox("Choose a Model", ["Mixtral-8x7b-32768", "llama2-70b-4096"])

    #consideration of memory length
    memory_length = st.sidebar.slider("Conversational Memory Length", 1, 15, 10)  

    #store the memory
    conversational_memory = ConversationBufferWindowMemory(k=memory_length, return_messages=True)

    user_question = st.text_area("What is the question")

    # Session state variables
    if 'chat_memory' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            conversational_memory.save_context({'input': message['human']},{'output': message['AI']})
    
    groq_chat = ChatGroq(
        groq_api_key = groq_api_key,
        model_name = model
        )
    
    conversation = ConversationChain(
        llm = groq_chat,
        memory = conversational_memory
    )

    if user_question:
        response = conversation(user_question)
        message = {'human': user_question, 'AI': response['response']}
        st.session_state.chat_history.append(message)
        st.write('ChatBot:',response['response'])



if __name__ == "__main__":
    main()

