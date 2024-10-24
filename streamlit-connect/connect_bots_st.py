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


class Connect_bots:
    def __init__(self, gemini_prompt_template, groq_prompt_template):
        self.gemini = Gemini(gemini_prompt_template)
        self.groq = Groq(groq_prompt_template)
        self.groq_response = ""
        self.gemini_response = ""
    
    def input_prompt(self):
        # Use st.text_input with a key and store the result
        input_msg = st.text_input("Let Groq and Bard talk about", key="user_input")
        
        # Initialize session state for conversation if not exists
        if 'conversation_started' not in st.session_state:
            st.session_state.conversation_started = False
            
        # Check if there's new input and the enter key was pressed
        if input_msg and not st.session_state.conversation_started:
            st.session_state.messages = [
                {"role": "USER", "content": input_msg},
                {"role": "bard", "content": f"Hello! I'm Bard. Let's talk about {input_msg}"},
                {"role": "groq", "content": f"Hi! I'm Groq. I'd love to discuss {input_msg}"}
            ]
            self.groq_response = st.session_state.messages[-1]["content"]
            st.session_state.conversation_started = True
            return True
            
        return st.session_state.conversation_started

    async def converse(self):
        exit_chat = 5
        
        # Display existing messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        while exit_chat > 0:
            # If last message is not from gemini, generate a new response
            if st.session_state.messages[-1]["role"] != "bard":
                with st.chat_message("bard"):
                    with st.spinner("Thinking..."):
                        self.gemini_response = self.gemini.chat_with_gemini(self.groq_response)
                        st.write(self.gemini_response)
                        message = {"role": "bard", "content": self.gemini_response}
                        st.session_state.messages.append(message)
                        
            if st.session_state.messages[-1]["role"] != "groq":
                with st.chat_message("groq"):
                    with st.spinner("brooding"):
                        self.groq_response = self.groq.chat_with_groq(self.gemini_response)
                        st.write(self.groq_response)
                        message = {"role": "groq", "content": self.groq_response}
                        st.session_state.messages.append(message)
            exit_chat -= 1

class Groq:
    def __init__(self,prompt_template):
        self.groq_chat = ChatGroq(
            groq_api_key = groq_api_key,
            # max_output_tokens=100,
            model_name = "Mixtral-8x7b-32768"
            )
        self.groq_conversation = ConversationChain(memory=st.session_state.chat_memory, 
                                                llm=self.groq_chat,
                                                # verbose=True,
                                                prompt = prompt_template)

    def chat_with_groq(self,prompt):
        groq_response = self.groq_conversation.predict(input = prompt)
        return groq_response

class Gemini:
    def __init__(self,prompt_template):
        self.gemini_chat = ChatGoogleGenerativeAI(model = "gemini-pro"
                                                #   max_output_tokens=100
                                                  )
        self.gemini_conversation = ConversationChain(memory=st.session_state.chat_memory,     
                                                llm=self.gemini_chat,
                                                # verbose=True,
                                                prompt = prompt_template)

    def chat_with_gemini(self,prompt):
        gemini_response = self.gemini_conversation.predict(input = prompt)
        return gemini_response
    
    
async def main():

    st.session_state.chat_memory = ConversationBufferWindowMemory(k=3, return_messages=True)
    st.session_state.messages = [
                    # {"role": "USER", "content": "talk about dogs"},
                    {"role": "bard", "content": "I'm bard"},
                    {"role": "groq", "content": "I'm groq"},
                    ]
        

    # if input_msg:

    bard_template = """You are bard and having a friendly discussion with groq which is an AI about whatever the USER has asked. Keep your responses simple, short and concise.

    Previous conversation:
    {history}
    groq: {input}
    bard:

    """
    groq_template = """You are groq and having a friendly discussion with bard which is an AI about whatever the USER has asked. Keep your responses simple, short and concise.
    Previous conversation:
    {history}
    bard: {input}
    groq: 

    """
    gemini_prompt_template = PromptTemplate(input_variables=["history", "input"], template=bard_template)
    groq_prompt_template = PromptTemplate(input_variables=["history", "input"], template=groq_template)
    connect = Connect_bots(gemini_prompt_template,groq_prompt_template)
    
    if connect.input_prompt():
        await connect.converse()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

