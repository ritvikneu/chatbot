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

groq_api_key = st.secrets["GROQ_API_KEY"]

class GroqStreamLitBot:
    def chat_with_groq():
        st.title("🗣️ Groq Chatbot")
        st.sidebar.title("🗣️ Groq Chatbot")
        st.subheader("㈻ Simple Chat Interface for Groq")

        model = st.sidebar.selectbox("Choose a Model", ["Mixtral-8x7b-32768", "llama2-70b-4096"])

        #consideration of memory length
        memory_length = st.sidebar.slider("Conversational Memory Length", 1, 15, 10)  

        # Initialize session state variables
        if 'chat_memory' not in st.session_state:
            st.session_state.chat_memory = ConversationBufferWindowMemory(k=memory_length, return_messages=True)

        # Initialize the chat message history
        if "messages" not in st.session_state.keys(): 
            st.session_state.messages = [
                {"role": "groq", "content": "How can I help you today?"}
            ]

        groq_chat = ChatGroq(
            groq_api_key = groq_api_key,
            model_name = model
            )
        
        conversation = ConversationChain(
            llm = groq_chat,
            memory = st.session_state.chat_memory
        )

        if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "groq":
            with st.chat_message("groq"):
                with st.spinner("brooding"):
                    response = conversation.predict(input=prompt)
                    st.write(response)
                    message = {"role":"groq","content":response}
                    st.session_state.messages.append(message)



if __name__ == "__main__":
    GroqStreamLitBot.chat_with_groq()

