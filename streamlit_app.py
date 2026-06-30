import streamlit as st
from google import genai

# Setup ng Page at Icon
st.set_page_config(page_title="Wizard AI", page_icon="🧙‍♂️", layout="centered") 

st.title("🧙‍♂️ Wizard AI")

# 1. Simulan ang memory ng Streamlit (Session State) para sa chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Kunin ang API Key at i-set up ang client
AKING_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=AKING_API_KEY)

# 2. I-display ang mga lumang pinag-usapan (History List) sa screen
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["text"]) 

    else:
        with st.chat_message("assistant", avatar="🧙‍♂️"):
            st.write(message["text"]) 

# 3. Kahon para sa bagong tanong ng user
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
        # Tawagan si Gemini gamit ang buong history ng usapan
        respond = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents="\n".join(api_contents), 
        )
        # IPASOK NATIN ITO SA LOOB NG TRY para mangyari lang kapag SUCCESSFUL si response
        # I-display ang sagot ni Wizard AI at i-save sa history
        with st.chat_message("assistant", avatar="🧙‍♂️"): 
            st.write(response.text) 
        st.session_state.chat_history.append({"role": "assistant", "tetxt": response.text}) 

    except Exception as e:
        # Mas malinaw na error message para alam natin ang dahilan 
        st.error("🚨 Error Wizard AI.") 
        st.warning(f"Detalye ng problema: {e}") 

