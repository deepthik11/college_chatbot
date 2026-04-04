import streamlit as st
from chatbot import ask_bot

# Page settings
st.set_page_config(page_title="VCET Chatbot", page_icon="🎓")

st.title("🎓 VCET College Chatbot")
st.write("Ask anything about the college 👇")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.chat_input("Type your question here...")

# When user sends message
if user_input:
    st.session_state.messages.append(("user", user_input))

    # Get bot response
    response = ask_bot(user_input)

    st.session_state.messages.append(("bot", response))

# Display chat messages
for role, message in st.session_state.messages:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)
    else:
        with st.chat_message("assistant"):
            st.markdown(message)