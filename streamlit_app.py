import streamlit as st
from google import genai

# Setup ng Page at Icon
st.set_page_config(page_title="Wizard AI", page_icon="🧙‍♂️", layout="centered") 

st.title("🧙‍♂️ Wizard AI")
st.write("Ask question.") 

# Simulan ang memory ng Streamlit (Session State) para sa chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Kunin ang API Key at i-set up ang client
AKING_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=AKING_API_KEY)

# I-display ang mga lumang pinag-usapan (History List) sa screen
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["text"]) 

    else:
        with st.chat_message("assistant", avatar="🧙‍♂️"):
            st.write(message["text"]) 

# Kahon para sa bagong tanong ng user
user_input = st.chat_input("Ask Wizard AI...")

if user_input:
    # I-display agad ang tinype ng user at i-save sa history
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # I-format ang buong history para ipadala kay Gemini
    api_contents =[]
    for msg in st.session_state.chat_history: 
        api_contents.append(f"{msg['role']}: {msg['text']}")

    api_contents.append("assistant: ") 

    try:
        # 1. Tawagan si Gimini gamit ang buong historu ng usapan
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="\n".join(api_contents),
        )
        
        # 2. TAMA (may 8 spaces o dalawang tab mula sa kaliwa - kasama dapat sa loob ng try):
        with st.chat_message("assistant", avatar="🧙‍♂️"): 
            st.write(response.text)
        st.session_state.chat_history.append({"role": "assistant", "text": response.text}) 

    except Exception as e:
        # 3. Kapag ubos ang quota (429), dito siya dadaan at hindi magpapakita ang 'response is not defined'
        st.error("🚨 Error Wizard AI.") 
        st.warning(f"Detalye ng problema: {e}")

