import streamlit as st
import google.generativeai as genai

# Oldal beállítása
st.set_page_config(page_title="Saját AI Asszisztens")
st.title("🤖 Saját Gemini App")

# API kulcs biztonságos betöltése a Secrets-ből
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiba: Az API kulcs nincs beállítva a Secrets menüben!")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# MODELL BEÁLLÍTÁSA - A legstabilabb névvel
# Ha a 'gemini-1.5-flash' nem megy, ez a verzió automatikusan próbálkozik
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    model = genai.GenerativeModel('gemini-pro')

# Chat előzmények inicializálása
if "messages" not in st.session_state:
    st.session_state.messages = []

# Korábbi üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Felhasználói bemenet
if prompt := st.chat_input("Miben segíthetek?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Válasz generálása
    with st.chat_message("assistant"):
        try:
            # Itt történik a hívás
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sajnos hiba történt: {e}")
            st.info("Tipp: Ellenőrizd, hogy az API kulcsod érvényes-e a Google AI Studio-ban!")
            
