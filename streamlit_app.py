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

# 🎨 CSS styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #19B2D6;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3, p {
        text-align: center !important;
        color: white;
    }

    /* Chat bubbles */
    .user-bubble {
        background-color: #F8CF39;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        display: inline-block;
        float: right;
        clear: both;
    }
    .assistant-bubble {
        background-color: white;
        color: #19B2D6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 10px 0;
        display: inline-block;
        float: left;
        clear: both;
    }

    .assistant-bubble ul, .assistant-bubble ol {
        color: #19B2D6 !important;
        margin-left: 20px;
    }

    /* Fixed input row at very bottom */
    .input-row {
        position: fixed;
        bottom: 55px; /* leave space for footer */
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        z-index: 999;
        display: flex;
        gap: 8px;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 12px;
        color: #19B2D6 !important;
        font-weight: bold;
        caret-color: #19B2D6;
        width: 100%;
    }
    .stButton > button {
        background-color: #F8CF39;
        color: #19B2D6;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.6em 1em;
        border: none;
        cursor: pointer;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
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
        padding: 10px 0;
        z-index: 1000;
    }

    .divider {
        text-align: center;
        margin: 20px 0;
        color: white;
        font-size: 0.8em;
        clear: both;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🖼️ Logo
st.markdown(
    """
    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
        <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
        <p style="margin-top: 10px; color: white; font-size: 18px; text-align: center;">
            A safe space to navigate feelings and mom guilt. Powered by OMG.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div style='text-align: center; font-size: 22px; font-weight: bold;'>What's on your mind today?</div>",
    unsafe_allow_html=True,
)

# 📝 Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_date" not in st.session_state:
    st.session_state.last_date = None
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

# 📥 Input row (pinned to bottom)
with st.container():
    st.markdown("<div class='input-row'>", unsafe_allow_html=True)
    cols = st.columns([6, 1])  
    with cols[0]:
        user_input = st.text_input("Type your message here...", key="chat_input", label_visibility="collapsed")
    with cols[1]:
        send_clicked = st.button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

# 🚀 Handle new message
if (user_input and send_clicked) or (user_input and not send_clicked):
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

    st.session_state.chat_input = ""
    st.experimental_rerun()

# 📜 Chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        current_date = datetime.now().strftime("%A, %B %d")
        if st.session_state.last_date != current_date:
            st.markdown(f"<div class='divider'>{current_date}</div>", unsafe_allow_html=True)
            st.session_state.last_date = current_date

        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)

# 📌 Footer
st.markdown(
    """
    <div class="footer">
        💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
    </div>
    """,
    unsafe_allow_html=True
)
