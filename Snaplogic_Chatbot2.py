import streamlit as st
import requests
from io import BytesIO
from gtts import gTTS   # NEW

# ────────────────────────────────────────────────────────────────────────────────
# Config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SnapLogic Customer Success Story Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 SnapLogic Customer Success Story Chatbot")
st.caption("Ask anything related to customer stories and digital EDI workflows.")

# ────────────────────────────────────────────────────────────────────────────────
# Session-state chat history
# ────────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I’m your SnapLogic Agent. How can I help you today?"
        }
    ]

# ────────────────────────────────────────────────────────────────────────────────
# API details
# ────────────────────────────────────────────────────────────────────────────────
API_URL = (
    "https://emea.snaplogic.com/api/1/rest/slsched/feed/"
    "ConnectFasterInc/snapLogic4snapLogic/Bootcamp_EMEA_June_2025/"
    "AgentDriver_Customer_story_Agent_GI_Trig_Task"
)
HEADERS = {
    "Authorization": "Bearer ij6UhQJJWE9a7vIDVJANBnzqZ1bEuZNk",
    "Content-Type": "application/json"
}

def fetch_snaplogic_response(user_prompt: str) -> str:
    """Call SnapLogic pipeline and return plain-text reply (or error text)."""
    payload = [{"prompt": user_prompt}]
    try:
        r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json().get("response", "✅ Request successful, but no response content.")
        elif r.status_code == 500:
            return "🚨 Server Error 500: Something went wrong in the SnapLogic pipeline."
        else:
            return f"❌ Error {r.status_code}: {r.text}"
    except requests.exceptions.RequestException as exc:
        return f"⚠️ Request failed: {exc}"

# ────────────────────────────────────────────────────────────────────────────────
# Text-to-speech helper
# ────────────────────────────────────────────────────────────────────────────────
def text_to_speech(text: str) -> BytesIO:
    """
    Turn `text` into an in-memory MP3 and return it as BytesIO.
    gTTS supports up to ~5 k chars in one call; chunking logic omitted for brevity.
    """
    mp3 = BytesIO()
    gTTS(text, lang="en", slow=False).write_to_fp(mp3)
    mp3.seek(0)
    return mp3

# ────────────────────────────────────────────────────────────────────────────────
# Chat UI
# ────────────────────────────────────────────────────────────────────────────────
# Historic bubbles
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New user input
user_input = st.chat_input("Type your message...")

if user_input:
    # 1️⃣ show user bubble
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2️⃣ fetch reply
    with st.chat_message("assistant"):
        with st.spinner("SnapLogic Agent is thinking..."):
            reply_text = fetch_snaplogic_response(user_input)

        # 3️⃣ show text reply
        st.markdown(reply_text)

        # 4️⃣ synthesize & embed audio player
        audio_bytes = text_to_speech(reply_text)
        st.audio(audio_bytes, format="audio/mp3")

    # 5️⃣ remember assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply_text})
