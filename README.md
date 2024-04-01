# CHAT BOTS


**Learn more by doing more, here's where you start <a href="https://www.buildfastwithai.com/#courses">@BuildFastWithAI</a>**

## GEMINI BOT
1. Generate GEMINI API key from <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a>
2. Install dependencies
   - pip install -r requirements.txt
3. Let's use streamlit secrets to store API KEY (do not share/post anywhere it's a secret)
   - create folder/file .streamlit/secrets.toml and add key against GOOGLE_API_KEY
4. Run locally 
   - streamlit run gemini_chat_bot_st.py 
5. Deploy your app on cloud, refer <a href="https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app">Streamlit Docs</a> 

## GROQ BOT
1. Generate GROQ API key from <a href="https://console.groq.com/keys">Groq Console</a>
2. Install dependencies
   - pip install -r requirements.txt
3. Let's use environment variables to store API key (do not share/post anywhere it's a secret)
   - create .env file and add key against GROQ_API_KEY   
4. Run locally
   - streamlit run groq_chat_bot_st.py
5. Deploy your app on cloud, refer <a href="https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app">Streamlit Docs</a> 


Together AI is a platform which provides access to many different available models. Create an <a href="https://api.together.xyz/settings/api-keys"> Together API key here</a>


## Interested in making the two bots talk:
