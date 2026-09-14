import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helpers import show_sidebar_info

st.set_page_config(page_title="AI Health Advisor — AQI Shield", page_icon="💬", layout="wide")

st.sidebar.title("🌫️ AQI Shield")
st.sidebar.caption("AI-Powered Air Quality Forecast")
show_sidebar_info()

# ══════════════════════════════════════════════════════════════
st.title("💬 AI Health Advisor")
st.caption("Ask any question about air quality, AQI levels, or health precautions. Powered by Groq LLaMA-3.")
st.divider()

# Read API key from st.secrets (works locally via .streamlit/secrets.toml AND on Streamlit Cloud)
def get_api_key():
    # 1. Try st.secrets first (recommended method)
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key and key != "paste_your_key_here":
            return key
    except Exception:
        pass
    # 2. Fallback: environment variable
    key = os.environ.get("GROQ_API_KEY", "")
    if key and key != "paste_your_key_here":
        return key
    return ""

GROQ_API_KEY = get_api_key()

SYSTEM_PROMPT = """You are an expert Air Quality and Public Health Advisor.
You help users understand AQI (Air Quality Index) levels, health impacts of air pollution,
and safety precautions. You refer to India's CPCB AQI scale:
- Good (0-50): Safe for all
- Satisfactory (51-100): Acceptable, sensitive groups careful
- Moderate (101-200): Sensitive groups affected
- Poor (201-300): Everyone affected, wear mask
- Very Poor (301-400): Serious risk, avoid outdoors
- Severe (401-500): Emergency, stay indoors

Always give clear, simple, actionable advice. Keep answers short and easy to understand.
Do not discuss topics unrelated to air quality or health."""

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Suggested questions
st.write("**💡 Try asking:**")
q1, q2, q3 = st.columns(3)
if q1.button("Is AQI 180 safe for children?", use_container_width=True):
    st.session_state.chat_history.append({"role": "user", "content": "Is AQI 180 safe for children?"})
if q2.button("What mask should I wear outdoors?", use_container_width=True):
    st.session_state.chat_history.append({"role": "user", "content": "What mask should I wear outdoors?"})
if q3.button("How does PM2.5 affect lungs?", use_container_width=True):
    st.session_state.chat_history.append({"role": "user", "content": "How does PM2.5 affect lungs?"})

st.divider()

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input
user_input = st.chat_input("Ask about air quality or health precautions...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    if not GROQ_API_KEY:
        demo_reply = (
            "⚠️ **Demo Mode** — Groq API key not found.\n\n"
            "To enable the real AI advisor:\n"
            "1. Go to https://console.groq.com and get a free API key\n"
            "2. Create a `.env` file in your AQI folder\n"
            "3. Add this line: `GROQ_API_KEY=gsk_xxxxxxxxxx`\n"
            "4. Restart the app"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": demo_reply})
        st.chat_message("assistant").write(demo_reply)
    else:
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state.chat_history
                    ],
                    max_tokens=512,
                    temperature=0.7
                )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
        except Exception as e:
            st.error(f"Error connecting to Groq: {e}")

# Clear chat button
if st.session_state.chat_history:
    st.write("")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
