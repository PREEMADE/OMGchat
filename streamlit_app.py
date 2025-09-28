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
.stTextInput > div > div > input {
    background-color: #ffffff;
    border: 2px solid #19B2D6;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
    color: #19B2D6 !important; /* brand blue */
}
::placeholder {
    color: #19B2D6 !important;
    opacity: 0.7;
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
    border: 2px solid #F8CF39;
}
/* Make list items inside assistant bubbles visible */
.assistant-bubble ol, .assistant-bubble ul, .assistant-bubble li {
    color: #000000 !important; /* black text */
}
#response-container {
    display: flex;
    flex-direction: column;
    max-height: 400px;
    overflow-y: auto;
    background-color: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
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
    border-top: 2px solid white;
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

/* Keep chat input fixed above footer */
.stTextInput {
    position: fixed;
    bottom: 0px; /* leaves room for footer */
    left: 50%;
    transform: translateX(-50%);
    width: 80%;  /* adjust width as you like */
    z-index: 999;
}

st.markdown(
    "<div style='text-align: center; font-size: 22px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

# Callback function to handle input
def handle_input():
    user_input = st.session_state.chat_input
    if user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M")})
        # Generate assistant reply
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}]
                + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] in ["user","assistant"]]
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%H:%M")})
    # Clear input automatically
    st.session_state.chat_input = ""

# Input box
st.text_input("Type your message here...", key="chat_input", on_change=handle_input)

# Display conversation
if len(st.session_state.messages) > 1:
    st.markdown("<div id='response-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages[1:]:  # skip system
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}<br><small>{msg.get('time','')}</small></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-bubble'>{msg['content']}<br><small>{msg.get('time','')}</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-scroll to bottom
    st.markdown("""
    <script>
    const container = document.getElementById('response-container');
    if (container) { container.scrollTop = container.scrollHeight; }
    </script>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
