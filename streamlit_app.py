import streamlit as st
from openai import OpenAI
import os
#from dotenv import load_dotenv

# Load the environment variables from the .env file
#load_dotenv()

#openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai_api_key = os.getenv('OPENAI_API_KEY')

st.title("🦜🔗 To je Forward chat")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=openai_api_key)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

         # Add user message to chat history

# Accept user input
if prompt := st.chat_input("What is up?"):
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})