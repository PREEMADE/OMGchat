import streamlit as st
import openai

# Set up OpenAI key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set page config
st.set_page_config(
    page_title="OMG Companion",
    
    layout="centered",
    initial_sidebar_state="collapsed",
)
# Inject custom styles
st.markdown("""
    <style>
    /* Input field text color fix */
    input[type="text"], textarea {
        color: #19B2D6 !important;
        font-weight: bold;
    }
    ::placeholder {
        color: #19B2D6 !important;
        opacity: 0.7;
    }
    .stApp {
        background-color: #19B2D6;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main {
        color: #19B2D6;
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
    .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Show logo (make sure the image is accessible)
st.markdown(
    '<div class="logo"><img src="https://i.imgur.com/XTLepWR.png" width="100"/></div>',
    unsafe_allow_html=True
)

st.title("Mom Guilt Companion")")
st.write("A safe space to navigate feelings and mom guilt—all powered by OMG.")

# Prompt input
prompt = st.text_input("What's on your mind today? (mom guilt, stress, doubts, anything)")

if prompt:
    with st.spinner("Thinking..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        assistant_response = response.choices[0].message.content
        st.success("Here’s a response from your companion:")
        st.write(assistant_response)
