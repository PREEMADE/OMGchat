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
        caret-color: #19B2D6; /* caret matches brand color */
        animation: blink-caret 1s step-end infinite;
    }
    @keyframes blink-caret {
        from, to { caret-color: transparent; }
        50% { caret-color: #19B2D6; }
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: transparent;
        text-align: center;
        font-size: 0.9em;
        color: white;
        padding: 10px 0;
        z-index: 100;
    }
    .input-label {
        font-size: 1.3em;
        font-weight: bold;
        color: white;
        text-align: center;
        display: block;
        margin-top: 11px;
    }
    /* Sticky input at bottom */
    .stTextInput {
        position: fixed;
        bottom: 50px; /* leave space above footer */
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        z-index: 999;
    }
    /* Responsive spacing */
    @media (max-width: 768px) {
      .block-container {
        padding-bottom: 20vh !important;
      }
    }
    @media (min-width: 769px) {
      .block-container {
        padding-bottom: 10vh !important;
      }
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

# Input label above chatbox
st.markdown(
    "<div style='text-align: center; font-size: 24px; font-weight: bold;'>What's on your mind today? (mom guilt, stress, doubts, anything)</div>",
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."}
    ]

## Fixed input bar at the bottom
st.markdown(
    """
    <style>
    .chat-input-container {
        position: fixed;
        bottom: 50px; /* sits just above footer */
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        display: flex;
        gap: 10px;
        z-index: 999;
    }
    .chat-input-box {
        flex: 1;
    }
    .send-btn {
        background-color: #F8CF39;
        color: #19B2D6;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5em 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container for input + send button
chat_input_col, send_button_col = st.columns([8, 1])

with chat_input_col:
    prompt = st.text_input("Type your message here...", key="chat_input", label_visibility="collapsed")

with send_button_col:
    send_pressed = st.button("📨", key="send_button")

# Process input when Enter pressed OR Send clicked
if (prompt and prompt.strip()) or send_pressed:
    if prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

        # Clear input after sending
        st.session_state["chat_input"] = ""

        # Add a send button
        send_pressed = st.form_submit_button("Send")

    # Handle input when Enter or Send is pressed
    if send_pressed and user_input.strip():
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown('</div>', unsafe_allow_html=True)

# Display conversation
if len(st.session_state.messages) > 1:
    st.markdown(
        """
        <div id="response-container" style="
            max-height: 300px;
            overflow-y: auto;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        ">
        """,
        unsafe_allow_html=True
    )
    for msg in st.session_state.messages[1:]:
        speaker = "**You:**" if msg["role"] == "user" else "**Companion:**"
        st.markdown(f"{speaker} {msg['content']}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-scroll to bottom
    st.markdown(
        """
        <script>
        const container = document.getElementById('response-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
        </script>
        """,
        unsafe_allow_html=True
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
