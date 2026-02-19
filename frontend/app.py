import streamlit as st
import re
import os
import requests

st.set_page_config(
    page_title="Automated AI Article Analyzer", 
    page_icon="📝",
    layout="centered"
)

st.title("Automated AI Article Analyzer")
st.write("Enter your email and an article URL")

backend_process_url = os.getenv("BACKEND_PROCESS_URL", "http://127.0.0.1:8000/process")

email = st.text_input("Email", placeholder="student@example.com")
article_url = st.text_input("Article URL", placeholder="https://example.com/article")

#validation functions
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

if st.button("Submit"):

    if not email or not article_url:
        st.error("Please fill in both fields.")

    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")

    elif not is_valid_url(article_url):
        st.error("Article URL must start with http:// or https://")

    else:
        try:
            with st.spinner("Sending request to backend..."):
                response = requests.post(
                    backend_process_url,
                    json={"email": email.strip(), "article_url": article_url.strip()},
                    timeout=25,
                )
                response.raise_for_status()
                result = response.json()

            st.success("Submitted successfully. n8n workflow has started.")
            st.write("Session ID:", result.get("session_id"))
            st.info("Check your email and Google Sheet for results.")
        except requests.HTTPError as e:
            st.error("Could not process request right now. Please try again.")
        except requests.RequestException as e:
            st.error("Could not connect to backend server.")
