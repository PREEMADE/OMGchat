# Input/Send box at the bottom of the page
st.markdown(
    """
    <style>
    .chat-input-container {
        position: fixed;
        bottom: 50px; /* keeps it above the footer */
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        display: flex;
        gap: 10px;
        z-index: 1000;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .chat-input-container textarea {
        flex: 1;
        resize: none;
        border: none;
        outline: none;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
        color: #333333;
    }
    .send-btn {
        background-color: #19B2D6;
        color: white;
        border: none;
        padding: 0 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .send-btn:hover {
        background-color: #148fa9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container for the input
with st.container():
    chat_input = st.text_area(
        "Type your message...",
        key="chat_input",
        label_visibility="collapsed",
        height=50
    )

    # Display Send button inline with input
    send = st.button("Send", key="send_btn")

# Handle Enter key OR Send button
if chat_input or send:
    if chat_input.strip():
        st.session_state.messages.append({"role": "user", "content": chat_input.strip()})
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.chat_input = ""  # clear after submit
