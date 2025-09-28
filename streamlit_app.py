import streamlit as st
import openai
from datetime import datetime

# 🔑 Set OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ⚙️ Page configuration
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

    /* User + Assistant chat bubbles */
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

    /* Fix list visibility inside assistant bubbles */
    .assistant-bubble ul, .assistant-bubble ol {
        color: #19B2D6 !important;
        margin-left: 20px;
    }

    /* Pinned chat input */
    .stTextInput {
        position: fixed;
        bottom: 60px;  /* sits above footer */
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        z-index: 999;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 12px;
        color: #19B2D6 !important;
        font-weight: bold;
        caret-color: #19B2D6; /* blinking caret in brand blue */
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
        z-index: 1000;
    }

    /* Divider between conversations */
    .divider {
        text-align: center;
        margin: 20px 0;
        color: white;
        font-size: 0.8em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🖼️ Logo and tagline
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

# 💬 Title
st.markdown(
    "<div style='text-align: center; font-size: 22px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True,
)

# 📝 Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_date" not in st.session_state:
    st.session_state.last_date = None

# ⌨️ Chat input
user_input = st.text_input("Type your message here...")

# 🚀 Handle new message
if user_input:
    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })

    # Get AI response
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

    # Clear input safely by rerunning
    st.experimental_rerun()

# 🖼️ Chat history display
for msg in st.session_state.messages:
    # Divider by date
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
