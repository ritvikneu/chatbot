import os
import argparse
import pickle
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

MEMORY_FILE = "memory/gemini_conversation_memory.pkl"
MESSAGE_HISTORY_FILE = "memory/gemini_message_history.pkl"

load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")

class GeminiAssistant:
    def __init__(self, memory_length=10):
        self.memory_length = memory_length
        self.buffer_memory = self.load_memory()
        self.message_history = self.load_message_history()

    def load_memory(self):
        """Load or initialize conversation memory."""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'rb') as file:
                return pickle.load(file)
        return ConversationBufferWindowMemory(k=self.memory_length, return_messages=True)

    def save_memory(self):
        """Save conversation memory to file."""
        with open(MEMORY_FILE, 'wb') as file:
            pickle.dump(self.buffer_memory, file)

    def load_message_history(self):
        """Load or initialize message history."""
        if os.path.exists(MESSAGE_HISTORY_FILE):
            with open(MESSAGE_HISTORY_FILE, 'rb') as file:
                return pickle.load(file)
        return [{"role": "assistant", "content": "How can I help you today?"}]

    def save_message_history(self):
        """Save message history to file."""
        with open(MESSAGE_HISTORY_FILE, 'wb') as file:
            pickle.dump(self.message_history, file)

    def chat(self):
        """Initiate conversation with Gemini AI."""
        gemini_chat = ChatGoogleGenerativeAI(google_api_key= google_api_key, model="gemini-pro")
        conversation = ConversationChain(memory=self.buffer_memory, llm=gemini_chat)

        for message in self.message_history:
            print(message["role"] + ": " + message["content"])

        # exit_chat=1
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = conversation.predict(input=user_input)
            print("Gemini Bot:", response)

            # Store user input and AI response in message history
            self.message_history.append({"role": "user", "content": user_input})
            self.message_history.append({"role": "bardbot", "content": response})
            # exit_chat-=1
        
        save_memory = input("save chat history(Y/N): ")
        if save_memory =="Y":
            # Store memory and message history
            self.save_memory()
            self.save_message_history()

    def chat_with_human(self):
        """Initiate conversation with Gemini AI."""
        gemini_chat = ChatGoogleGenerativeAI(google_api_key= google_api_key, model="gemini-pro")
        conversation = ConversationChain(memory=self.buffer_memory, llm=gemini_chat)

        for message in self.message_history:
            print(message["role"] + ": " + message["content"])

        exit_chat=1
        while exit_chat>0:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = conversation.predict(input=user_input)
            print("Gemini Bot:", response)

            # Store user input and AI response in message history
            self.message_history.append({"role": "user", "content": user_input})
            self.message_history.append({"role": "bardbot", "content": response})
            exit_chat-=1

        save_memory = input("save chat history(Y/N): ")
        if save_memory =="Y":
            # Store memory and message history
            self.save_memory()
            self.save_message_history()

    def chat_with_other_bot(self,bot_input,template):
        """Initiate conversation with Gemini AI."""
        gemini_chat = ChatGoogleGenerativeAI(google_api_key= google_api_key, 
                                             model="gemini-pro")
        
        conversation = ConversationChain(memory=self.buffer_memory, 
                                         llm=gemini_chat)
        gemini_response = conversation.predict(input=bot_input)
        return gemini_response

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with an Gemini AI')
    parser.add_argument('--memory_length', type=int, default=10,
                        help='Conversational Memory Length (default: 10)')
    args = parser.parse_args()

    gemini_assistant = GeminiAssistant(memory_length=args.memory_length)
    gemini_assistant.chat_with_human()
