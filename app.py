import streamlit as st
import google.generativeai as genai

# Oldal konfiguráció
st.set_page_config(page_title="Saját AI Asszisztens", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiba: Hiányzik az API kulcs a Secrets-ből!")
    st.stop()

# Konfiguráció
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# MODELL DEFINIÁLÁSA - A 404-ES HIBA ELLENI SPECIÁLIS NÉVVEL
# Ez a teljes elérési út segít a Google szervereinek megtalálni a modellt
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# Chat memória
if "messages" not in st.session_state:
    st.session_state.messages = []

# Üzenetek megjelenítése
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Beviteli mező
if prompt := st.chat_input("Írj valamit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generálás
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Ha még mindig baj van, megpróbáljuk a Pro modellt is
            try:
                alt_model = genai.GenerativeModel(model_name='models/gemini-pro')
                response = alt_model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"Hiba történt: {e}")
                st.info("Kérlek, várj pár percet, amíg a Google aktiválja az új kulcsodat!")
                
