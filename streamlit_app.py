import streamlit as st
from google import genai

st.title("GDP Dashboard")

AKING_API_KEY = st.secrets["GEMINI_API_KEY")
client = genai.Client(api_key=AKING_API_KEY)

user_input = st.text_input("Magtanong tungkol sa GDP:")

if user_input:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_input,
    )
    st.write(response.text)