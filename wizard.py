import streamlit as st
from google import genai

st.set_page_config(page_title="WIZARD AI", page_icon=" ", layout="centered")

# Iniwan nating blanko para sa kaligtasan sa internet
AKING_API_KEY = st.secret["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else ""

try:
    client = genai.Client(api_key=AKING_API_KEY)
except Exception:
    client = None 

st.markdown(""" 
    <style>
    .stApp { background-color: #f5f7fb; color: #1e1428; } 
    .stChatMessage { 
        background-color: #ffffff}
        color: #1e1428 !important; 
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0,05); 
    } 
    h1 { color: #3a225d; text-align: center; font-family: 'Arial'; font-weight: bold; }
    </style> 
""", unsafe_allow_html=True) 

st.title("WIZARD AI")

gabay = (
    "Ikaw si WIZARD, ang tapat at matalinong AI Assistant ni Dani. "
    "Alam mo na si Dani ay isang computer engineer, " 
    "nakatira sa Washington, masipag tumakbo sa treadmill, at mag-code sa Mac. " 
    "Palaging maging magalang, medyo may konting wit o pagiging astig, at sagutin siya sa English o Tagalog." 
)

if "message" not in st.session_state: 
    st.session_state.message =[{"role": "assistant", "content": "Magandang araw! Ako si Wizard, ang AI assistant ni Dani. Handa na akong tumulong!"}] 

for msg in st.session_state.message:
    with st.chat_message(msg["role"]): 
        st.write(msg["content"]) 

if tanong := st.chat_input("Iutos kay Wizard..."):
    with st.chat_message("user"): 
        st.write(tanong)
    st.session_state.message.append({"role": "user", "content": tanong}) 

    if not AKING_API_KEY:
        sagot = "Wizard: Kailangan ko ng tamang API Key sa Streamlit Secrets para gumana!" 
    else: 
        try: 
            response = client.models.generate_content( 
                model='gemini-2.5-flash', 
                contents=tanong, 
                config={'system_instruction': gabay} 
            )
            sagot = response.text
        except Exception as e: 
            sagot = f"Sorry master, may error sa koneksyon: {e}" 

    with st.chat_message("assistant"):
        st.write(sagot) 
    st.session_state.message.append({"role": "assistant", "content": sagot}) 

if st.button("Burajhin ang Chat"):
    st.session_state.messages = [{"role": "assistant", "content": "Nabura na ang chat. Handa na ulit ako!"}]  
    st.rerun()
