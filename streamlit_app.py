import streamlit as st
import openai
import datetime

# Set API Key
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
.logo {
    display: flex;
    justify-content: center;
    margin-bottom: 0px;
}
.user-bubble {
    background-color: #F8CF39;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    max-width: 75%;
    align-self: flex-end;
    font-weight: bold;
}
.assistant-bubble {
    background-color: white;
    color: #19B2D6;
    padding: 10px 15px;
    border: 2px solid #F8CF39;
    border-radius: 15px;
    margin: 5px;
    max-width: 75%;
    align-self: flex-start;
}
.chat-container {
    display: flex;
    flex-direction: column;
    margin: 20px auto;
    width: 90%;
    max-width: 700px;
}
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #19B2D6; /* Solid brand blue */
    text-align: center;
    font-size: 0.9em;
    color: white;
    padding: 10px 0;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)

# Logo
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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input field with key that updates
user_input = st.text_input("Type your message here...", key=f"input_{len(st.session_state.messages)}")

# Process input
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.datetime.now().strftime("%H:%M")
    })

    # Get AI response
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reply = response.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "time": datetime.datetime.now().strftime("%H:%M")
    })

# Display conversation
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']} <br><small>{msg['time']}</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-bubble'>{msg['content']} <br><small>{msg['time']}</small></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    💕 Built with love by the OMG Team | 🌟 Mom Guilt Companion © 2025
</div>
""", unsafe_allow_html=True)
