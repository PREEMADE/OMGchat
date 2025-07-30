import streamlit as st
import openai

# Set OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set page configuration
st.set_page_config(
    page_title="Mompanion",
    page_icon="💬",
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
        padding: 10px;
    }
    .stButton button {
        background-color: #19B2D6;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.5em 1em;
    }
    .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display logo
st.markdown(
    '<div class="logo"><img src="https://i.imgur.com/XTLepWR.png" width="100"/></div>',
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown("<h1>MOMPANION</h1>", unsafe_allow_html=True)
st.markdown("<p>A safe space to navigate feelings and mom guilt—all powered by OMG.</p>", unsafe_allow_html=True)

# Text input
prompt = st.text_input("What's on your mind today? (mom guilt, stress, doubts, anything)")

# Chat response logic
if prompt:
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate, uplifting support companion for mothers navigating guilt, stress, or emotional overwhelm."},
                {"role": "user", "content": prompt}
            ]
        )
        assistant_response = response.choices[0].message.content

        # Scrollable container
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
        st.markdown(assistant_response, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Auto-scroll script
        st.markdown(
            """
            <script>
            const observer = new MutationObserver(() => {
                const container = document.getElementById('response-container');
                if (container) {
                    container.scrollTop = container.scrollHeight;
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
            </script>
            """,
            unsafe_allow_html=True
        )
