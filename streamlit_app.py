import streamlit as st
import openai

# 🔑 Secure API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ⚙️ Page config
st.set_page_config(
    page_title="Mompanion",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 🎨 Global CSS
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
.stTextInput > div > div > input {
    background-color: #ffffff;
    border: 2px solid #19B2D6;
    border-radius: 5px;
    padding: 15px;
    color: #19B2D6 !important;
    font-weight: bold;
    caret-color: #19B2D6;
    animation: blink-caret 1s step-end infinite;
}
@keyframes blink-caret {
    from, to { caret-color: transparent; }
    50% { caret-color: #19B2D6; }
}
/* Sticky input */
.stTextInput {
    position: fixed;
    bottom: 50px; /* above footer */
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    z-index: 999;
}
/* Footer */
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
/* Chat container */
#response-container {
    max-height: 300px;
    overflow-y: auto;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    margin-top: 20px;
}
/* Responsive spacing */
@media (max-width: 768px) {
  .block-container { padding-bottom: 22vh !important; }
}
@media (min-width: 769px) {
  .block-container { paddin
