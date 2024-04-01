from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Set environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize conversation memory and messages
chat_memory = ConversationBufferWindowMemory(k=3, 
                                             human_prefix= "gemini",
                                             ai_prefix="groq",
                                             return_messages=True)
messages = [
    {"role": "gemini", "content": "I'm Gemini Bot"},
    {"role": "groq", "content": "I'm Groq Bot"},
    {"role": "groq", "content": "Let's have a conversation"}
]

# Define conversation prompt template
template = """The following is a friendly conversation. The AI is
talkative but keeps the response simple, short and concise.
If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
{input}
gemini:
groq:
"""
prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)


class ConnectBots:
    def __init__(self):
        self.gemini = Gemini(prompt_template)
        self.groq = Groq(prompt_template)
        self.groq_response = messages[-1]["content"]
        self.gemini_response = ""

    def converse(self):
        exit_chat = 3
        while exit_chat > 0:
            for message in messages:
                print(message["role"] + ": " + message["content"])

            # If last message is not from gemini, generate a new response
            if messages[-1]["role"] != "gemini":
                self.gemini_response = self.gemini.chat_with_gemini(self.groq_response)
                print("Gemini: " + self.gemini_response)
                messages.append({"role": "gemini", "content": self.gemini_response})

            # If last message is not from groq, generate a new response
            if messages[-1]["role"] != "groq":
                self.groq_response = self.groq.chat_with_groq(self.gemini_response)
                print("Groq: " + self.groq_response)
                messages.append({"role": "groq", "content": self.groq_response})

            exit_chat -= 1
        return


class Groq:
    def __init__(self, prompt_template):
        self.groq_chat = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="Mixtral-8x7b-32768",
            max_output_tokens=100
        )
        self.groq_conversation = ConversationChain(memory=chat_memory,
                                               llm=self.groq_chat,
                                               verbose=True,
                                               prompt=prompt_template)

    def chat_with_groq(self, prompt):
        groq_response = self.groq_conversation.predict(input=prompt)
        return groq_response


class Gemini:
    def __init__(self, prompt_template):
        self.gemini_chat = ChatGoogleGenerativeAI(model="gemini-pro",
                                                  max_output_tokens=100,
                                                  )
        self.gemini_conversation = ConversationChain(memory=chat_memory,
                                               llm=self.gemini_chat,
                                               verbose=True,
                                               prompt=prompt_template)

    def chat_with_gemini(self, prompt):
        gemini_response = self.gemini_conversation.predict(input=prompt)
        return gemini_response


if __name__ == "__main__":
    connect = ConnectBots()
    connect.converse()
