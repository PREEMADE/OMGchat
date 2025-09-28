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

    /* Extra space so messages don't overlap footer */
    .block-container {
        padding-bottom: 120px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🖼️ Logo + header
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

# 📜 Chat history
for msg in st.session_state.messages:
    current_date = datetime.now().strftime("%A, %B %d")
    if st.session_state.last_date != current_date:
        st.markdown(f"<div class='divider'>{current_date}</div>", unsafe_allow_html=True)
        st.session_state.last_date = current_date

    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>", unsafe_allow_html=True)

# 📥 Input pinned at
