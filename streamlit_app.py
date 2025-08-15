import streamlit as st
import openai

# Set OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page configuration
st.set_page_config(
    page_title="",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject CSS styling
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
    input[type="text"], textarea {
        color: #19B2D6 !important;
        font-weight: bold;
    }
    ::placeholder {
        color: #19B2D6 !important;
        opacity: 0.7;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #19B2D6;
        border-radius: 5px;
        padding: 15px;
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
        margin-top: 50px;
        text-align: center;
        font-size: 0.9em;
        color: white;
    }
    .input-label {
        font-size: 1.3em;
        font-weight: bold;
        color: white;
        text-align: center;
        display: block;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display logo
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
        <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
        <p style="margin-top: 5px; color: white; font-size: 18px; text-align: center;">
            A safe space to navigate feelings and mom guilt. Powered by OMG.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Simulate blinking cursor after placeholder */
input::placeholder {
    font-weight: bold;
    color: #19B2D6;
    animation: blink-caret 1s step-end infinite;
}

@keyframes blink-caret {
    1, 100% { border-right: .15em solid transparent; }
    50% { border-right: .15em solid #19B2D6; }
}
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Input prompt label
st.markdown("""
<span class="input-label">What's on your mind today? (mom guilt, stress, doubts, anything)</span>
""", unsafe_allow_html=True)

# Input prompt
prompt = st.text_input("")

# Generate response
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Display conversation
if len(st.session_state.messages) > 1:
    st.markdown("""
    <div id="response-container" style="
        max-height: 300px;
        overflow-y: auto;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    ">
    """, unsafe_allow_html=True)
    for msg in st.session_state.messages[1:]:
        speaker = "**You:**" if msg["role"] == "user" else "**Companion:**"
        st.markdown(f"{speaker} {msg['content']}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <script>
        const container = document.getElementById('response-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
        </script>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
