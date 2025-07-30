import streamlit as st
import openai

st.set_page_config(page_title="Mom Guilt Companion Chat", page_icon="💬")

st.title("💬 Mom Guilt Companion")
st.write("A safe space to navigate feelings and mom guilt—all powered by GPT‑3.5 turbo.")

# Secure entry of API key
openai_api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("Please add your OpenAI API key to continue.")
    st.stop()

# Initialize openai client
client = openai.OpenAI(api_key=openai_api_key)

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
