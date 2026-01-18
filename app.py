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
        # EZ A TITOK: A stabil v1 végpontot használjuk, 
        # és pontosan azt a modell nevet, amit a Google legutoljára jóváhagyott
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 1024,
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            result = response.json()
            
            if "candidates" in result and result["candidates"]:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            elif "error" in result:
                # Ha még mindig 404-et dob, megpróbáljuk a "gemini-pro" nevet automatikusan
                alt_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                alt_res = requests.post(alt_url, headers=headers, data=json.dumps(payload))
                alt_result = alt_res.json()
                
                if "candidates" in alt_result:
                    answer = alt_result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Google hiba: {result['error']['message']}")
            else:
                st.warning("Nem érkezett válasz az AI-tól. Próbáld újra!")
        except Exception as e:
            st.error(f"Váratlan hiba: {e}")
            
