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

# Inject CSS styling
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
    .logo {
        display: flex;
        justify-content: center;
        margin-bottom: 0px;
    }
    /* Input box */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
        color: #19B2D6 !important; /* brand blue text */
    }
    ::placeholder {
        color: #19B2D6 !important;
        opacity: 0.7;
    }
    /* Chat bubbles */
    .user-bubble {
        background-color: #F8CF39;
        color: #000;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px;
        max-width: 75%;
        align-self: flex-end;
        text-align: right;
    }
    .assistant-bubble {
        background-color: #fff;
        color: #19B2D6;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px;
        max-width: 75%;
        align-self: flex-start;
        text-align: left;
        border: 2px solid #F8CF39;
    }
    /* Chat container */
    #response-container {
        display: flex;
        flex-direction: column;
        max-height: 400px;
        overflow-y: auto;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    /* Footer solid */
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
    </style>
    """,
    unsafe_allow_html=True
)

# Logo + subtitle
st.markdown(
    """
    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
        <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
        <p style="margin-top: 20px; color: white; font-size: 18px; text-align: center;">
            A safe space to navigate feelings and mom guilt. Powered by OMG.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Input label
st.markdown(
    "<div style='text-align: center; font-size: 22px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.text_input("Type your message here...", key="chat_input")

# When user submits
if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M")}
    )
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}]
            + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append(
            {"role": "assistant", "content": reply, "time": datetime.now().strftime("%H:%M")}
        )
    # Clear input safely
    if "chat_input" in st.session_state:
        st.session_state["chat_input"] = ""

# Chat display
if st.session_state.messages:
    st.markdown('<div id="response-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='assistant-bubble'>{msg['content']}<br><small>{msg['time']}</small></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-scroll
    st.markdown(
        """
        <script>
        const container = document.getElementById('response-container');
        if (container) { container.scrollTop = container.scrollHeight; }
        </script>
        """,
        unsafe_allow_html=True,
    )

# Footer
st.markdown(
    """
    <div class="footer">
        💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
    </div>
    """,
    unsafe_allow_html=True
)
