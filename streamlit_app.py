import streamlit as st
import openai
from datetime import datetime

# Set OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page configuration
st.set_page_config(
    page_title="Mompanion",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# CSS for styling
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
    /* Chat bubbles */
    .user-bubble {
        background-color: #F8CF39;
        color: #19B2D6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px;
        max-width: 70%;
        text-align: right;
        margin-left: auto;
        font-weight: bold;
    }
    .assistant-bubble {
        background-color: white;
        color: #19B2D6;
        border: 2px solid #F8CF39;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px;
        max-width: 70%;
        text-align: left;
    }
    /* Force list styling inside assistant replies */
    .assistant-bubble ul,
    .assistant-bubble ol {
        color: #19B2D6;
        margin-left: 20px;
    }
    /* Input box styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 15px;
        color: #19B2D6 !important;
        font-weight: bold;
    }
    ::placeholder {
        color: #19B2D6 !important;
        opacity: 0.7;
    }
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0f7a9b;  /* solid darker blue */
        text-align: center;
        font-size: 0.9em;
        color: white;
        padding: 10px 0;
        z-index: 100;
    }
    /* Make chat scrollable without overlap */
    .block-container {
        padding-bottom: 20vh !important;
    }
    </style>
""", unsafe_allow_html=True)

# Logo + tagline
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
    <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
    <p style="margin-top: 15px; color: white; font-size: 18px; text-align: center;">
        A safe space to navigate feelings and mom guilt. Powered by OMG.
    </p>
</div>
""", unsafe_allow_html=True)

# Input label
st.markdown(
    "<div style='text-align: center; font-size: 24px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Chat input
chat_input = st.text_input("Type your message here...", key="chat_input", placeholder="Type your message...")

# Generate response
if chat_input:
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Clear input after submit
    st.session_state.chat_input = ""

# Display conversation
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
