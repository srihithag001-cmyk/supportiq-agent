import os
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# Setup Clients
hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)
bank_id = os.getenv("HINDSIGHT_BANK_ID")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="SupportIQ | Hindsight Agent", layout="wide")
st.title("🎧 SupportIQ: Customer Support Agent")
st.caption("Powered by Vectorize Hindsight Memory & Groq LLM")

# Layout: 2 Columns (Chat on Left, Hindsight Memory Inspector on Right)
col1, col2 = st.columns([2, 1])

with col1:
    customer_id = st.text_input("Customer Email / Identifier", value="alex@acmecorp.com")
    user_query = st.text_area("Customer Issue / Message", placeholder="E.g., How do I start the web server container?")
    
    if st.button("Submit Support Ticket", type="primary"):
        if not user_query.strip():
            st.warning("Please type a question or issue first.")
        else:
            with st.spinner("1. Querying Hindsight for customer history..."):
                # Recall past interactions
                recall_resp = hindsight.recall(
                    bank_id=bank_id,
                    query=f"Customer {customer_id}: {user_query}"
                )
                
                memories_text = "\n".join([f"- {m.text}" for m in recall_resp.results])
                st.session_state["last_memory"] = memories_text

            with st.spinner("2. Groq LLM analyzing history & formulating solution..."):
                system_prompt = f"""You are an elite enterprise IT and Customer Support engineer.
You are assisting customer: {customer_id}

PERSISTENT CUSTOMER CONTEXT (FROM HINDSIGHT MEMORY):
{memories_text if memories_text else "No prior ticket history on file."}

CRITICAL INSTRUCTIONS:
1. Use the memory context above (OS, environment, communication preferences, past resolutions).
2. DO NOT suggest troubleshooting steps that have previously failed.
3. If the user previously stated preferences (e.g. direct CLI commands, concise tone), strictly follow them.
4. Keep the answer accurate, actionable, and reference their known environment when relevant."""

                chat_completion = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.3
                )
                agent_reply = chat_completion.choices[0].message.content
                st.session_state["last_reply"] = agent_reply

            # Automatically retain this new interaction into Hindsight
            with st.spinner("3. Retaining interaction into Hindsight..."):
                hindsight.retain(
                    bank_id=bank_id,
                    content=f"Customer {customer_id} ticket: '{user_query}'. Resolution/Advice: '{agent_reply[:250]}'"
                )

    # Display Agent Output
    if "last_reply" in st.session_state:
        st.subheader("Agent Response")
        st.success(st.session_state["last_reply"])

with col2:
    st.subheader("🧠 Hindsight Memory Inspector")
    st.caption("Live context recalled for this specific user:")
    if "last_memory" in st.session_state and st.session_state["last_memory"]:
        st.info(st.session_state["last_memory"])
    else:
        st.write("Submit a ticket to inspect live retrieved memory tokens.")