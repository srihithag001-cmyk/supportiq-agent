# SupportIQ - Enterprise Support Agent with Persistent Hindsight Memory

SupportIQ is an AI customer support agent powered by **Hindsight** memory and **Groq** LLMs. 
Unlike stateless support bots that forget users after every session, SupportIQ retains customer environments, previous ticket resolutions, and user preferences across conversations.

## Features
- **Persistent Cross-Session Memory:** Retains OS details, configuration history, and previous failure modes using Vectorize Hindsight.
- **Adaptive Communication:** Adapts its tone and technical brevity based on learned user preferences.
- **Real-Time Memory Inspection:** Live sidebar displaying recalled contextual tokens before formulating resolutions.

## Setup
1. Clone repository
2. Install requirements: `pip install -r requirements.txt`
3. Add `.env` with `HINDSIGHT_API_KEY`, `HINDSIGHT_BANK_ID`, and `GROQ_API_KEY`
4. Run: `streamlit run app.py`