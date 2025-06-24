import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="SnapLogic Project Chat Bot", layout="centered")

# API endpoint and headers
API_URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/snapLogic4snapLogic/Bootcamp_EMEA_June_2025/AgentDriver_Customer_story_Agent_GI_Trig_Task"
HEADERS = {
    "Authorization": "Bearer ij6UhQJJWE9a7vIDVJANBnzqZ1bEuZNk",
    "Content-Type": "application/json"
}

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("🤖 Sales Opportunity Chatbot")
st.markdown("Ask me about sales opportunities in negotiation or in manufacturing organizations.")

# Chat input
user_input = st.text_input("You:", placeholder="e.g., What opportunities are in negotiations?")

# On user submit
if st.button("Send") and user_input.strip():
    # Append user question to chat history
    st.session_state.chat_history.append(("user", user_input))
    
    # Prepare API request
    payload = {"Questions": user_input}
    
    try:
        # Send request
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        # Extract answer
        answer = response.json().get("content", "Sorry, I couldn't understand that.")
    except Exception as e:
        answer = f"Error: {str(e)}"
    
    # Append bot answer to chat history
    st.session_state.chat_history.append(("bot", answer))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
