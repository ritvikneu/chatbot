import os
import argparse
import pickle
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

MEMORY_FILE = "memory/groq_conversation_memory.pkl"
MESSAGE_HISTORY_FILE = "memory/groq_message_history.pkl"

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

class GroqAssistant:
    def __init__(self, memory_length=10):
        self.memory_length = memory_length
        self.buffer_memory = self.load_memory()
        self.message_history = self.load_message_history()
        self.groq_api_key = groq_api_key

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'rb') as file:
                return pickle.load(file)
        return ConversationBufferWindowMemory(k=self.memory_length, return_messages=True)

    def save_memory(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, 'wb') as file:
            pickle.dump(self.buffer_memory, file)

    def load_message_history(self):
        if os.path.exists(MESSAGE_HISTORY_FILE):
            with open(MESSAGE_HISTORY_FILE, 'rb') as file:
                return pickle.load(file)
        return [{"role": "assistant", "content": "How can I help you today?"}]

    def save_message_history(self):
        os.makedirs(os.path.dirname(MESSAGE_HISTORY_FILE), exist_ok=True)
        with open(MESSAGE_HISTORY_FILE, 'wb') as file:
            pickle.dump(self.message_history, file)

    def chat_with_human(self):
        models = ["Mixtral-8x7b-32768", "llama2-70b-4096"]
        model = models[0]

        groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=model
        )

        conversation = ConversationChain(memory=self.buffer_memory, llm=groq_chat)

        for message in self.message_history:
            print(message["role"] + ": " + message["content"])

        # exit_chat=10
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = conversation.predict(input=user_input)
            print("Groq Bot:", response)

            # Store user input and AI response in message history
            self.message_history.append({"role": "user", "content": user_input})
            self.message_history.append({"role": "groqbot", "content": response})
            # exit_chat-=1

        save_memory = input("save chat history(Y/N): ")
        if save_memory =="Y":
            # Store memory and message history
            self.save_memory()
            self.save_message_history()

    def chat_with_other_bot(self,bot_input):
        groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="Mixtral-8x7b-32768"
        )

        conversation = ConversationChain(memory=self.buffer_memory, 
                                         llm=groq_chat)
        
        groq_response = conversation.predict(input=bot_input)

        return groq_response
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with a Groq AI')
    parser.add_argument('--memory_length', type=int, default=2,
                        help='Conversational Memory Length (default: 10)')
    args = parser.parse_args()

    groq_assistant = GroqAssistant(memory_length=args.memory_length)
    groq_assistant.chat_with_human()
