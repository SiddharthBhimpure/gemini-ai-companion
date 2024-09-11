import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = gen_ai.start_chat()  # Use appropriate method
    except Exception as e:
        st.error(f"Error initializing chat session: {str(e)}")

# Display the chatbot's title on the page
st.title("🤖 Gemini Pro - ChatBot")

# Display the chat history
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    try:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
