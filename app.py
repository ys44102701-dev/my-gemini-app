import streamlit as st
import google.generativeai as genai

# Oldal konfiguráció
st.set_page_config(page_title="Saját AI", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiányzik az API kulcs!")
    st.stop()

# SPECIÁLIS KONFIGURÁCIÓ: A stabil v1 verzió kényszerítése
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')

# Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

# Üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bevitel
if prompt := st.chat_input("Írj valamit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Itt a titok: a legstabilabb modell nevet használjuk
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hiba: {e}")
            st.info("Ha most hoztad létre a kulcsot, adj a Google-nek 10 percet!")
            
