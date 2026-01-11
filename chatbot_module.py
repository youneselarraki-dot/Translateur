import streamlit as st
from transformers import pipeline

# ===============================
# LOAD MODEL (cached)
# ===============================
@st.cache_resource
def load_chatbot():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )

# ===============================
# CHATBOT PAGE
# ===============================
def page():
    st.title("🤖 AI Chatbot")

    st.write("Ask me anything 👇")

    chatbot = load_chatbot()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Type your message")

    if user_input:
        # Add user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot(
                    f"Answer clearly and helpfully: {user_input}",
                    max_length=200
                )[0]["generated_text"]

                st.markdown(response)

        # Save bot response
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

    # Clear chat
    if st.button("🗑 Clear chat"):
        st.session_state.chat_history = []
        st.rerun()
