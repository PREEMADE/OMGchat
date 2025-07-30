import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Mom Guilt Companion Chat", page_icon="💬")
# Set page config
st.set_page_config(
    page_title="Mom Guilt Companion",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS styling
st.markdown("""
    <style>
    .stApp {
        background-color: #19B2D6;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main {
        color: #000000;
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
    .stMarkdown h1 {
        color: #19B2D6;
    }
    .stMarkdown p {
        font-size: 1.1em;
    }
    .logo {'<div class="logo"><img src="https://imgur.com/a/QEOExIK" width="100"/></div>'
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Show logo (host this somewhere like GitHub or Streamlit static folder)
st.markdown(
    '<div class="logo"><img src="https://YOUR_IMAGE_URL_HERE" width="100"/></div>',
    unsafe_allow_html=True
)

st.title("💬 Mom Guilt Companion")
st.write("A safe space to navigate feelings and mom guilt—all powered by GPT‑3.5 turbo.")

# Secure entry of API key
import openai
import streamlit as st

# Use secret key from Streamlit Cloud
openai_api_key = st.secrets["OPENAI_API_KEY"]
import openai
openai.api_key = openai_api_key


# Prompt input
prompt = st.text_input("What's on your mind today? (mom guilt, stress, doubts, anything)")

if prompt:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a compassionate companion for moms experiencing stress and guilt. "
                    "Provide empathetic support, affirmations, and helpful suggestions."
                )},
                {"role": "user", "content": prompt}
            ],
        )
        assistant_response = response.choices[0].message.content
        st.success("Here’s a response from your companion:")
        st.write(assistant_response)
