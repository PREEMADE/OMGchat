import streamlit as st
import openai

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
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 15px;
        color: #19B2D6 !important;
        font-weight: bold;
        caret-color: #19B2D6;
    }
    .stButton button {
        background-color: #F8CF39;
        color: #19B2D6;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.5em 1em;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
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
        z-index: 100;
    }
    /* Sticky input at bottom */
    .chat-input-container {
        position: fixed;
        bottom: 60px; /* keep above footer */
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display logo + subtitle
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

# Section header
st.markdown(
    "<div style='text-align: center; font-size: 24px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Display conversation bubbles
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background-color:#F8CF39; color:black; padding:10px 15px; border-radius:15px; margin:5px; text-align:right; display:inline-block; max-width:70%; float:right;'>{msg['content']}</div><div style='clear:both;'></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:white; color:#19B2D6; padding:10px 15px; border-radius:15px; margin:5px; text-align:left; display:inline-block; max-width:70%; float:left;'>{msg['content']}</div><div style='clear:both;'></div>",
            unsafe_allow_html=True,
        )

# Chat input (fixed at bottom)
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

    user_input = st.text_input(
        "Type your message here...",
        key="chat_input",
        value=st.session_state.get("chat_input", ""),
        label_visibility="collapsed"
    )
# Input text pinned at bottom
user_input = st.text_input(
    "Type your message here...",
    key="chat_input",
    value=st.session_state.get("chat_input", ""),
    label_visibility="collapsed"
)

# Handle submission
if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Clear safely (avoid Streamlit API exception)
    st.session_state["chat_input"] = ""


    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
    </div>
    """,
    unsafe_allow_html=True
)
