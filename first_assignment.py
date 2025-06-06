import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client with api_key
client = OpenAI(api_key=api_key)

# Streamlit App title
st.title("Chatbot using OpenAI 🚀")

# Initialize chat history in session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input prompt
if prompt := st.chat_input("Say something"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI API to get response
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content.strip()

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
