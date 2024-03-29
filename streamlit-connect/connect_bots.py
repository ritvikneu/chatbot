import streamlit as st
from streamlit_chat import message
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq #llm system resides here and pass inference parameters
from dotenv import load_dotenv
import os


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
groq_api_key = os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
st.session_state.chat_memory = ConversationBufferWindowMemory(k=10, return_messages=True)
st.session_state.messages = [
                {"role": "gemini", "content": "I'm Gemini Bot"},
                {"role": "groq", "content": "I'm Groq Bot"}
            ]


class connect_bots:
    def converse():
        if prompt := st.chat_input("Your question"): 
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        exit_chat = 5
        groq_response = "Lets have a conversation"
        while exit_chat >0:        
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            gemini_response = Gemini.chat_with_gemini(groq_response)
            st.write(gemini_response)
            message = {"role": "gemini", "content": gemini_response}
            st.session_state.messages.append(message)

            groq_response = Groq.chat_with_groq(gemini_response)
            st.write(groq_response)
            message = {"role": "groq", "content": groq_response}
            st.session_state.messages.append(message) 
            exit_chat-=1

class Groq:
    def chat_with_groq(prompt):
        groq_chat = ChatGroq(
            groq_api_key = groq_api_key,
            model_name = "Mixtral-8x7b-32768"
            )
        conversation = ConversationChain(memory=st.session_state.chat_memory, llm=groq_chat)
        groq_response = conversation.predict(input = prompt)
        return groq_response

class Gemini:
    def chat_with_gemini(prompt):
        memory_length = 3
        gemini_chat = ChatGoogleGenerativeAI(model = "gemini-pro")
        conversation = ConversationChain(memory=st.session_state.chat_memory, llm=gemini_chat)
        gemini_response = conversation.predict(input = prompt)
        return gemini_response

if __name__ == "__main__":
    connect_bots.converse()

