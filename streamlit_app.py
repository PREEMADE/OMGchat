import streamlit as st
import openai
from datetime import datetime

# Secure API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page config
st.set_page_config(
    page_title="Mompanion",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# CSS Styling
st.markdown("""
<style>
.stApp {
    background-color: #19B2D6;
    font-family: 'Helvetica Neue', sans-serif;
}
h1, h2, h3, p {
    text-align: center !important;
    color: white;
}
.logo {
    display: flex;
    justify-content: center;
    margin-bottom: 0px;
}
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 120px; /* space for input + footer */
}
.user-bubble {
    background-color: #F8CF39;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    max-width: 70%;
    align-self: flex-end;
    text-align: right;
}
.assistant-bubble {
    background-color: white;
    color: #19B2D6;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    max-width: 70%;
    align-self: flex-start;
    text-align: left;
}
.timestamp {
    font-size: 0.75em;
    color: #333;
}
.stTextInput {
    position: fixed;
    bottom: 60px; /* above footer */
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    z-index: 999;
}
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #19B2D6;
    text-align: center;
    font-size: 0.9em;
    color: white;
    padding: 10px 0;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# Logo + subtitle
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
    <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
    <p style="margin-top: 20px; color: white; font-size: 18px; text-align: center;">
        A safe space to navigate feelings and mom guilt. Powered by OMG.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3>What's on your mind today? (mom guilt, stress, doubts, anything)</h3>", unsafe_allow_html=True)

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    timestamp = datetime.now().strftime("%H:%M")
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}<br><span class='timestamp'>{timestamp}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input text at bottom
user_input = st.text_input("Type your message here...", key="chat_input")

# Handle submission
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Clear input after sending
    st.session_state.chat_input = ""

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
