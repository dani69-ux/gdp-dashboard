import streamlit as st
from google import genai

st.set_page_config(page_title="Wizard AI", page_icon="🧙‍♂️")

st.title("Wizard AI")

AKING_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=AKING_API_KEY)

user_input = st.text_input("Magtanong kay Wizard AI:")

if user_input:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_input,
    )
    st.write(response.text)