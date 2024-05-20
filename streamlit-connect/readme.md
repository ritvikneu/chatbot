## Streamlit Conversational AI with Gemini Pro and Groq

This Streamlit application implements a conversational AI system that seamlessly combines the strengths of Google's Gemini Pro and Groq's Mixtral-8x7b-32768 language models. Users can engage in a dynamic dialogue with these two powerful AI agents, each contributing their unique capabilities to the conversation.

### Features:

* **Dual AI Interaction:**  Leverages both Google's Gemini Pro and Groq's Mixtral-8x7b-32768 for diverse and engaging dialogue.
* **Streamlit Interface:**  Provides a user-friendly web-based interface for interacting with the AI agents.
* **Conversation Memory:**  Maintains conversation context using Langchain's `ConversationBufferWindowMemory` to ensure coherent responses.
* **Customizable Prompts:**  Offers flexible prompt templates for fine-tuning the behavior and style of the AI agents.

### Dependencies:

* **Python 3.8 or higher:** Required for the project's libraries and functionalities.
* **Streamlit:** Install the Streamlit library: `pip install streamlit`
* **Langchain:** Install the Langchain library: `pip install langchain`
* **Langchain-Google-Genai:** Install the Langchain-Google-Genai library: `pip install langchain-google-genai`
* **Langchain-Groq:** Install the Langchain-Groq library: `pip install langchain_groq`
* **dotenv:** Install the dotenv library: `pip install python-dotenv`

### Setup:

1. **Google Cloud Platform (GCP) Project:**
   * Create a new GCP project.
   * Enable the Google Generative AI API for your project.
   * Obtain a Google API key for your project and store it securely (e.g., in a `.env` file).

2. **Groq API Key:**
   * Create a Groq account and get your API key.
   * Store the API key securely (e.g., in a `.env` file).

3. **Streamlit Secrets:**
   * Create a `secrets.toml` file in the Streamlit application's root directory.
   * Add your Google API key and Groq API key as secrets:
     ```toml
     [secrets]
     GOOGLE_API_KEY = "your_google_api_key"
     GROQ_API_KEY = "your_groq_api_key"
     ```
   * **Important:** Replace `"your_google_api_key"` and `"your_groq_api_key"` with your actual API keys.

4. **Environment Variables:**
   * Optionally, you can use environment variables to manage API keys.
   * Set the following environment variables before running the Streamlit application:
     ```bash
     export GOOGLE_API_KEY="your_google_api_key"
     export GROQ_API_KEY="your_groq_api_key"
     ```

### Running the Application:

1. **Installation:** Install the required dependencies (see "Dependencies" section).
2. **Run:** Execute the Streamlit application: `streamlit run app.py`
3. **Access:**  Open the provided URL in your web browser to interact with the conversational AI.

### Usage:

* The application will display a chat interface with two AI agents: "bard" (Gemini Pro) and "groq" (Mixtral-8x7b-32768).
* Type your messages in the text input box and press Enter to send them.
* The AI agents will respond to your messages in the chat window.
* You can continue the conversation by typing new messages.

### Customization:

* **Prompt Templates:**  Modify the `bard_template` and `groq_template` variables in the code to customize the instructions and guidelines for each AI agent.
* **Language Models:**  You can experiment with different language models from Google Generative AI and Groq by modifying the `model` parameter in the respective classes.
* **Conversation Memory:** Adjust the `k` parameter in `ConversationBufferWindowMemory` to control how much of the previous conversation is remembered.

### Notes:

* This application requires active internet access to communicate with the Google Generative AI API and Groq.
* The performance and quality of the AI responses depend on the language models, your internet connection, and the prompt engineering.
* This project is a starting point for exploring dual-AI conversational systems.  You can extend it to include more AI agents, integrate other language models, and implement more sophisticated conversation management techniques.

### Example Interaction:

```
User: Hi, can you tell me about the history of AI?
bard: The history of AI is long and complex, dating back to the early days of computing.
groq: The history of artificial intelligence can be traced back to ancient Greek mythology.
User: Interesting. What are some current AI trends?
bard:  Current trends include advancements in natural language processing, computer vision, and robotics.
groq:  AI is now being used to develop self-driving cars, create personalized medical treatments, and automate many tasks.
```

This project demonstrates a powerful approach to building engaging and informative conversational AI applications. Experiment with the code, customize the prompts, and explore the capabilities of these cutting-edge language models to create your own unique conversational experiences.
