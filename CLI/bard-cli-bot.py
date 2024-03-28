# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import os
import argparse
import pickle

MEMORY_FILE = "conversation_memory.pkl"
MESSAGE_HISTORY_FILE = "message_history.pkl"

def save_memory(memory):
    with open(MEMORY_FILE, 'wb') as file:
        pickle.dump(memory, file)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'rb') as file:
            return pickle.load(file)
    return ConversationBufferWindowMemory(k=10, return_messages=True)

def save_message_history(messages):
    with open(MESSAGE_HISTORY_FILE, 'wb') as file:
        pickle.dump(messages, file)

def load_message_history():
    if os.path.exists(MESSAGE_HISTORY_FILE):
        with open(MESSAGE_HISTORY_FILE, 'rb') as file:
            return pickle.load(file)
    return [{"role": "assistant", "content": "How can I help you today?"}]

def main():
    parser = argparse.ArgumentParser(description='Chat with an AI assistant via command line')
    parser.add_argument('--memory_length', type=int, default=10,
                        help='Conversational Memory Length (default: 10)')
    args = parser.parse_args()

    memory_length = args.memory_length

    os.environ["GOOGLE_API_KEY"] = input("Enter your Google API key: ")

    # Load or initialize conversation memory
    buffer_memory = load_memory()

    # Load or initialize message history
    message_history = load_message_history()

    gemini_chat = ChatGoogleGenerativeAI(model="gemini-pro")

    conversation = ConversationChain(memory=buffer_memory, llm=gemini_chat)

    for message in message_history:
        print(message["role"] + ": " + message["content"])

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = conversation.predict(input=user_input)
        print("AI Assistant:", response)

        # Store user input and AI response in message history
        message_history.append({"role": "user", "content": user_input})
        message_history.append({"role": "assistant", "content": response})

        # Store memory and message history
        save_memory(buffer_memory)
        save_message_history(message_history)

if __name__ == "__main__":
    main()
