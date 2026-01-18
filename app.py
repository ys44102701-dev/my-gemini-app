import streamlit as st
import requests
import json

st.set_page_config(page_title="Saját AI", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs betöltése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiányzik az API kulcs a Secrets-ből!")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

# Memória
if "messages" not in st.session_state:
    st.session_state.messages = []

# Megjelenítés
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bevitel
if prompt := st.chat_input("Írj valamit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Ez a biztos URL a 1.5-flash modellel
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if "candidates" in result:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = result.get('error', {}).get('message', 'Ismeretlen hiba')
                st.error(f"Google hiba: {error_msg}")
        except Exception as e:
            st.error(f"Hiba: {e}")
            
