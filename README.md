# CHAT BOTS

**lets make the bots talk**
Do more by learning more <a href="https://www.buildfastwithai.com/#courses">@BuildFastWithAI</a>

## BARD BOT
1. Generate GEMINI API key from <a href="https://aistudio.google.com/app/apikey">Google AI Studio</a>
2. Install dependencies
   - pip install -r requirements.txt
3. Lets use streamlit secrets to store API KEY (do not share/post with anyone)
   - create folder/file .streamlit/secrets.toml and add key against GOOGLE_API_KEY
4. Run locally 
   - streamlit run bard-chat-bot.py 
5. Deploy your app on cloud https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app 

## GROQ BOT
1. Generate GROQ API key from <a href="https://console.groq.com/keys">Groq Console</a>
2. Install dependencies
   - pip install -r requirements.txt
3. Lets use environment variables to store API key
   - create .env file and add key against GROQ_API_KEY   
4. Run locally
   - streamlit run groq-chat-bot.py
5. Deploy your app on cloud https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app 

