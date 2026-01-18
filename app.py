import streamlit as st
import google.generativeai as genai

# Oldal konfiguráció
st.set_page_config(page_title="Saját AI Asszisztens", layout="centered")
st.title("🤖 Saját Gemini App")

# API kulcs ellenőrzése
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hiba: Hiányzik az API kulcs a Secrets-ből!")
    st.stop()

# Konfiguráció kényszerítése v1 verzióra (ez a lényeg!)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Modell definiálása a legbiztosabb névvel
# A 1.5-flash jelenleg a leggyorsabb és leginkább támogatott
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # Generálás hibakezeléssel
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Ha még mindig 404, kiírjuk a pontos okot
            st.error(f"Technikai hiba: {e}")
            if "404" in str(e):
                st.info("Próbálkozom a régebbi modellel...")
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    response = alt_model.generate_content(prompt)
                    st.markdown(response.text)
                except:
                    st.warning("Úgy tűnik, az API kulcsod még nem aktiválódott teljesen a Google-nél. Várj 5 percet!")
