import streamlit as st
import requests
import json

st.set_page_config(page_title="Saját AI", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiányzik az API kulcs!")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Írj valamit..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # EZ A SPECIÁLIS URL A MEGOLDÁS:
        # v1beta-t használunk, és pontosan azt a nevet adjuk meg, amit a szerver kér
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
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
                # Ha ez sem megy, megpróbáljuk a flash-el is automatikusan
                url_flash = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                response = requests.post(url_flash, headers=headers, data=json.dumps(payload))
                result = response.json()
                if "candidates" in result:
                    answer = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Google válasza: {result.get('error', {}).get('message', 'Ismeretlen hiba')}")
        except Exception as e:
            st.error(f"Hiba: {e}")
