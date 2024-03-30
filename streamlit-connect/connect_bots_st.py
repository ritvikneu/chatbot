import streamlit as st
from streamlit_chat import message
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq #llm system resides here and pass inference parameters
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
import os


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
groq_api_key = os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
st.session_state.chat_memory = ConversationBufferWindowMemory(k=3, return_messages=True)
st.session_state.messages = [
                {"role": "gemini", "content": "I'm Gemini Bot"},
                {"role": "groq", "content": "I'm Groq Bot"},
                {"role": "groq", "content": "Let's have a conversation"}
            ]

template = """The following is a friendly conversation between Gemini and Groq. The AIs are 
talkative but keeps the response simple, short and concise.
If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
{input}
Gemini:
Groq:
"""
prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)

class Connect_bots:
    def __init__(self):
        self.gemini = Gemini(prompt_template)
        self.groq = Groq(prompt_template)
        self.groq_response = st.session_state.messages[-1]["content"]
        self.gemini_response = ""
    

    def converse(self):
        exit_chat = 5
        # groq_response = "Lets have a conversation"
        # while exit_chat >0:        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        while exit_chat>0:
         # If last message is not from gemini, generate a new response
            if st.session_state.messages[-1]["role"] != "gemini":
                with st.chat_message("gemini"):
                    with st.spinner("Thinking..."):
                        self.gemini_response = self.gemini.chat_with_gemini(self.groq_response)
                        st.write(self.gemini_response)
                        message = {"role": "gemini", "content": self.gemini_response}
                        st.session_state.messages.append(message) # Add response to message history
            
            if st.session_state.messages[-1]["role"] != "groq":
                with st.chat_message("groq"):
                    with st.spinner("brooding"):
                        self.groq_response = self.groq.chat_with_groq(self.gemini_response)
                        st.write(self.groq_response)
                        message = {"role":"groq","content":self.groq_response}
                        st.session_state.messages.append(message)
            exit_chat-=1
        return
            

class Groq:
    def __init__(self,prompt_template):
        self.groq_chat = ChatGroq(
            groq_api_key = groq_api_key,
            model_name = "Mixtral-8x7b-32768"
            )
        self.conversation = ConversationChain(memory=st.session_state.chat_memory, 
                                                llm=self.groq_chat,
                                                verbose=True,
                                                prompt = prompt_template)

    def chat_with_groq(self,prompt):
        groq_response = self.conversation.predict(input = prompt)
        return groq_response

class Gemini:
    def __init__(self,prompt_template):
        self.gemini_chat = ChatGoogleGenerativeAI(model = "gemini-pro")
        self.conversation = ConversationChain(memory=st.session_state.chat_memory,     
                                                llm=self.gemini_chat,
                                                verbose=True,
                                                prompt = prompt_template)

    def chat_with_gemini(self,prompt):
        gemini_response = self.conversation.predict(input = prompt)
        return gemini_response

if __name__ == "__main__":
    connect = Connect_bots()
    connect.converse()

