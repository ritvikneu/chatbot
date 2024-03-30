from gemini_cli_bot import GeminiAssistant
from groq_cli_bot import GroqAssistant
import argparse

class Mediator:
    def __init__(self, gemini_assistant, groq_assistant):
        self.gemini_assistant = gemini_assistant
        self.groq_assistant = groq_assistant
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

    def communicate(self):
        print("Starting communication between Gemini and Groq assistants.")
        exit_chat = 5
        query = input("Give something to start with:")
        groq_response = query
        while exit_chat>0:
            # Gemini assistant responds to the user
            gemini_response = self.gemini_assistant.chat_with_other_bot(groq_response)
            print("Gemini Bot:", gemini_response)

            # Groq assistant receives the Gemini's response and responds
            groq_response = self.groq_assistant.chat_with_other_bot(gemini_response)
            print("Groq Bot:", groq_response)
            exit_chat-=1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with both Gemini and Groq AI assistants via command line')
    parser.add_argument('--memory_length', type=int, default=10,
                        help='Conversational Memory Length (default: 10)')
    args = parser.parse_args()

    gemini_assistant = GeminiAssistant(memory_length=args.memory_length)
    groq_assistant = GroqAssistant(memory_length=args.memory_length)

    mediator = Mediator(gemini_assistant, groq_assistant)
    mediator.communicate()
