import streamlit as st
import requests

API_URL = "web-production-7cbcc.up.railway.app/chat"

st.set_page_config(page_title="Djed AI", page_icon="👴")
st.title("👴 Razgovor s djedom")

if "messages" not in st.session_state:
    st.session_state.messages = []

# prikaz poruka
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input
if prompt := st.chat_input("Reci nešto..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Djed razmišlja..."):
            r = requests.post(API_URL, json={"prompt": prompt})
            reply = r.json()["reply"]

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})