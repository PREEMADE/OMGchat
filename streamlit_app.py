import streamlit as st
import openai
import datetime

# Secure API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page configuration
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
    color: #19B2D6 !important;
    font-weight: bold;
    caret-color: #19B2D6;
}
.user-bubble {
    background-color: #F8CF39;
    color: #000000;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 8px;
    max-width: 70%;
    float: right;
    clear: both;
}
.assistant-bubble {
    background-color: #ffffff;
    color: #19B2D6;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 8px;
    max-width: 70%;
    float: left;
    clear: both;
}
/* Fix numbered and bulleted list colors */
.assistant-bubble ol, .assistant-bubble ul, .assistant-bubble li {
    color: #19B2D6 !important;
}
.divider {
    clear: both;
    margin: 10px 0;
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
</style>
""", unsafe_allow_html=True)

# Logo & tagline
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 10px;">
    <img src="https://i.imgur.com/iGDWGBX.png" width="222" style="margin-bottom: 5px;"/>
    <p style="margin-top: 20px; color: white; font-size: 18px; text-align: center;">
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

# Input box with key for persistence
chat_input = st.text_input("Type your message here...", key="chat_input")

# Generate assistant response
if chat_input:
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
    # Clear input safely
    st.session_state[chat_input] = ""

# Display conversation
for i, msg in enumerate(st.session_state.messages[1:]):  # skip system prompt
    timestamp = datetime.datetime.now().strftime("%H:%M")
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}<br><small>{timestamp}</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
