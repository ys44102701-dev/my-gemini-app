import streamlit as st
import google.generativeai as genai

# Oldal beállítása (mobilbarát nézet)
st.set_page_config(page_title="Saját AI Asszisztens", page_icon="🤖")

st.title("🤖 Saját Gemini App")

# API kulcs beállítása (biztonságosabb, ha titkosított környezeti változóként tárolod)
api_key = st.secrets["GOOGLE_API_KEY"]

# Modell beállítása
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat előzmények inicializálása
if "messages" not in st.session_state:
    st.session_state.messages = []

# Korábbi üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Felhasználói input
if prompt := st.chat_input("Miben segíthetek?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Válasz generálása
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
      
