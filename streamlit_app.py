import streamlit as st
import openai
from datetime import datetime

# 🔑 OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ⚙️ Page config
st.set_page_config(
    page_title="Mompanion",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 🎨 WhatsApp-style CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ECE5DD; /* WhatsApp background */
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Chat bubbles */
    .user-bubble {
        background-color: #19B2D6;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0;
        display: inline-block;
        float: right;
        clear: both;
        max-width: 70%;
        word-wrap: break-word;
    }
    .assistant-bubble {
        background-color: #f1f0f0;
        color: black;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 8px 0;
        display: inline-block;
        float: left;
        clear: both;
        max-width: 70%;
        word-wrap: break-word;
    }
    .timestamp {
        font-size: 0.7em;
        opacity: 0.7;
        float: right;
        margin-left: 8px;
    }

    /* Input area */
    .input-area {
        position: fixed;
        bottom: 50px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        background-color: white;
        border-radius: 25px;
        padding: 5px 10px;
        display: flex;
        align-items: center;
        box-shadow: 0px 1px 5px rgba(0,0,0,0.2);
    }
    .stTextInput > div > div > input {
        border: none;
        outline: none;
        color: black !important;
        font-size: 1em;
    }
    .stButton>button {
        background-color: #19B2D6;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        border: none;
        font-size: 1.2em;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #19B2D6;
        text-align: center;
        font-size: 0.9em;
        color: white;
        padding: 5px 0;
        z-index: 1000;
    }

    /* Add space so chat doesn’t overlap input */
    .block-container {
        padding-bottom: 140px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 📝 Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📜 Chat history
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    st.markdown(
        f"<div class='{bubble_class}'>{msg['content']}<span class='timestamp'>{msg['time']}</span></div>",
        unsafe_allow_html=True,
    )

# 📥 Input area (WhatsApp style)
with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([10, 1])
    with cols[0]:
        user_input = st.text_input("Type a message...", key="chat_box", label_visibility="collapsed")
    with cols[1]:
        send_clicked = st.form_submit_button("✈️")

# 🚀 Handle new message
if user_input and send_clicked:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })

    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "time": datetime.now().strftime("%H:%M")
    })
    st.experimental_rerun()

# 📌 Footer
st.markdown(
    """
    <div class="footer">
        💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
    </div>
    """,
    unsafe_allow_html=True
)
