import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  # Change to your FastAPI server's endpoint

st.title(" 🍁 RAG-Chatbot 🍁 ")

st.sidebar.header("Configuration")
session_id = st.sidebar.text_input("Session ID", value="default_session")
user_input = st.text_area("Enter your input:", height=70)

if st.button("Get Response"):
    if not user_input.strip():
        st.warning("Please enter some input.")
    else:
        with st.spinner("Processing..."):
            try:
                payload = {"session_id": session_id, "userInput": user_input}
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Response received!")
                    st.json(result)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
