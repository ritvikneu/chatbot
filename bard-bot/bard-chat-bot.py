import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os

class Gemini:
    def chat_with_gemini():
        # os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
        # memory_length = st.sidebar.slider("Conversational Memory Length", 1, 15, 10)  
        memory_length = 3
        # Initialize session state variables
        if 'chat_memory' not in st.session_state:
            st.session_state.chat_memory = ConversationBufferWindowMemory(k=memory_length, return_messages=True)
        # Initialize the chat message history
        if "messages" not in st.session_state.keys(): 
            st.session_state.messages = [
                {"role": "assistant", "content": "How can I help you today?"}
            ]

        gemini_chat = ChatGoogleGenerativeAI(model = "gemini-pro")


        conversation = ConversationChain(memory=st.session_state.chat_memory, llm=gemini_chat)

        if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages: # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = conversation.predict(input = prompt)
                    st.write(response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message) # Add response to message history

if __name__ == "__main__":
    Gemini.chat_with_gemini()

