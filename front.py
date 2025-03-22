# app.py
import streamlit as st
from gtts import gTTS
import os
import tempfile
from langchain_core.messages import HumanMessage

# Simulation d'un agent (remplace plus tard par `from agent import app`)
def fake_response(history):
    return type("FakeResponse", (), {"content": " saha chribtek stack over harissa 🤖."})()

# Streamlit config
st.set_page_config(page_title="Assistant Hôtel California", layout="centered")
st.title("🏨 Assistant IA – Hôtel California")

# Mémoire de conversation utilisateur
if "history" not in st.session_state:
    st.session_state.history = []

# 🔊 Synthèse vocale
def speak(text):
    tts = gTTS(text=text, lang='fr')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# 💬 Interface chat
user_input = st.chat_input("Posez une question...")
if user_input:
    # Affiche la question de l'utilisateur
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ajouter à l'historique
    st.session_state.history.append(HumanMessage(content=user_input))

    # 🔁 Appel simulé à un agent (remplace plus tard par `app.invoke(...)`)
    response = fake_response(st.session_state.history)

    # Affiche la réponse de l’assistant
    with st.chat_message("assistant"):
        st.markdown(response.content)
        speak(response.content)

    # Ajouter à l’historique
    st.session_state.history.append(response)
