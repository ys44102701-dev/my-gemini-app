import streamlit as st
import requests
import json

st.set_page_config(page_title="Saját AI", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiányzik az API kulcs a Secrets-ből!")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# Chat memória inicializálása
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
        # KÖZVETLEN V1-ES HÍVÁS (Megkerüli a 404-es hibát)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"

        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            # Válasz kiírása
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Hiba a Google válaszában: {result.get('error', {}).get('message', 'Ismeretlen hiba')}")
        except Exception as e:
            st.error(f"Hálózati hiba: {e}")
            
