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
st.session_state.chat_memory = ConversationBufferWindowMemory(k=10, return_messages=True)
st.session_state.messages = [
                {"role": "gemini", "content": "I'm Gemini Bot"},
                {"role": "groq", "content": "I'm Groq Bot"}
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

class connect_bots:

    def converse():
        exit_chat = 5
        groq_response = "Lets have a conversation"
        # while exit_chat >0:        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        gemini_response = Gemini.chat_with_gemini(groq_response)
        # st.write(gemini_response)
        message = {"role": "gemini", "content": gemini_response}
        st.session_state.messages.append(message)
        st.write(st.session_state.messages[-1])

        groq_response = Groq.chat_with_groq(gemini_response)
        # st.write(groq_response)
        message = {"role": "groq", "content": groq_response}
        st.session_state.messages.append(message) 
        st.write(st.session_state.messages[-1])
            # exit_chat-=1
            

class Groq:
    def chat_with_groq(prompt):
        groq_chat = ChatGroq(
            groq_api_key = groq_api_key,
            model_name = "Mixtral-8x7b-32768"
            )
        conversation = ConversationChain(memory=st.session_state.chat_memory, 
                                         llm=groq_chat,
                                         prompt = prompt_template)
        groq_response = conversation.predict(input = prompt)
        return groq_response

class Gemini:
    def chat_with_gemini(prompt):
        gemini_chat = ChatGoogleGenerativeAI(model = "gemini-pro")
        conversation = ConversationChain(memory=st.session_state.chat_memory, 
                                         llm=gemini_chat,
                                         prompt = prompt_template)
        gemini_response = conversation.predict(input = prompt)
        return gemini_response

if __name__ == "__main__":
    connect_bots.converse()

