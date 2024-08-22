import streamlit as st
import requests
import base64
import json

# App title
st.title("📁 Jinbaflow: File to Webhook")

# File uploader
uploaded_file = st.file_uploader("Choose a file to upload", type=["csv", "txt", "json", "xlsx"])

# Webhook URL input
webhook_url = st.text_input("Enter the Webhook URL", placeholder="https://your-webhook-url.com")

# Submit button
if st.button("Send File"):
    if uploaded_file is not None and webhook_url:
        try:
            # Read the file bytes and encode it to base64
            file_bytes = uploaded_file.read()
            encoded_file = base64.b64encode(file_bytes).decode('utf-8')

            # Prepare JSON payload
            payload = {
                "filename": uploaded_file.name,
                "filedata": encoded_file,
                "filetype": uploaded_file.type
            }

            # Send POST request with JSON payload
            response = requests.post(webhook_url, json=payload, verify=False)

            # Handle the response
            if response.status_code == 200:
                st.success("File sent successfully!")
            else:
                st.error(f"Failed to send file. Status code: {response.status_code}")
                st.write(response.text)  # Display response text for debugging
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload a file and provide a webhook URL.")
