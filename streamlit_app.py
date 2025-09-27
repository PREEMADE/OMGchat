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
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 15px;
        color: #19B2D6 !important; /* brand blue */
        font-weight: bold;
    }
    ::placeholder {
        color: #19B2D6 !important;
        opacity: 0.7;
    }
    /* Chat bubbles */
    .user-bubble {
        background-color: #F8CF39;
        color: #19B2D6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px;
        text-align: right;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .assistant-bubble {
        background-color: #ffffff;
        color: #19B2D6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px;
        text-align: left;
        max-width: 70%;
        float: left;
        clear: both;
    }
    small {
        font-size: 0.7em;
        color: gray;
    }
    /* Solid footer */
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
        z-index: 100;
        border-top: 2px solid white;
    }
    /* Responsive padding */
    .block-container {
        padding-bottom: 20vh !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
    <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
    <p style="margin-top: 20px; color: white; font-size: 18px; text-align: center;">
        A safe space to navigate feelings and mom guilt. Powered by OMG.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align: center; font-size: 24px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Input box
user_input = st.text_input("Type your message here...", key="chat_input")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })

    # Generate assistant reply
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "time": datetime.now().strftime("%H:%M")
    })

    # Clear input after send
    st.session_state.chat_input = ""

# Display chat
for msg in st.session_state.messages[1:]:  # skip system
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    timestamp = msg.get("time", "")

    if role == "user":
        st.markdown(
            f"<div class='user-bubble'>{content}<br><small>{timestamp}</small></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='assistant-bubble'>{content}<br><small>{timestamp}</small></div>",
            unsafe_allow_html=True
        )

# Footer
st.markdown("""
    <div class="footer">
        💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
    </div>
""", unsafe_allow_html=True)
