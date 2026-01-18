import streamlit as st
import google.generativeai as genai
import os

# Oldal konfiguráció
st.set_page_config(page_title="Saját AI Asszisztens", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiba: Hiányzik az API kulcs a Secrets-ből!")
    st.stop()

# KÉNYSZERÍTETT KONFIGURÁCIÓ A STABIL v1 API-HOZ
# Ez a sor javítja ki a 404-es hibát
os.environ["GOOGLE_API_VERSION"] = "v1"
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Modell definiálása
model = genai.GenerativeModel('gemini-1.5-flash')

# Chat memória inicializálása
if "messages" not in st.session_state:
    st.session_state.messages = []

# Korábbi üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Felhasználói bemenet
if prompt := st.chat_input("Írj valamit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Válasz generálása
            response = model.generate_content(prompt)
            if response and response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Az AI nem küldött választ. Próbáld meg újra!")
        except Exception as e:
            st.error(f"Technikai hiba: {e}")
            st.info("Tipp: Ha most hoztad létre a kulcsot, várj 5 percet és nyomj egy Reboot-ot!")
