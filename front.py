# front.py
import streamlit as st
from gtts import gTTS
import os
import tempfile
from langchain_core.messages import HumanMessage
from agent_config import agent  # Ton agent avec le tool get_restaurants

# Configuration de la page Streamlit
st.set_page_config(page_title="Assistant Hôtel California", layout="centered")
st.title("🏨 Assistant IA – Hôtel California")

# Initialisation de l'historique utilisateur
if "history" not in st.session_state:
    st.session_state.history = []

# 🔊 Fonction pour lire le texte avec gTTS
def speak(text):
    tts = gTTS(text=text, lang='fr')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# 💬 Interface du chat
user_input = st.chat_input("Posez une question sur les restaurants, les spas, etc.")
if user_input:
    # Affichage de la question de l'utilisateur
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ajouter le message utilisateur à l'historique
    st.session_state.history.append(HumanMessage(content=user_input))

    # Appel à l'agent
    response = agent.invoke(user_input)  # ← Renvoie un dict avec 'input' et 'output'

    # Affichage de la réponse de l'assistant
    with st.chat_message("assistant"):
        st.markdown(response["output"])   # ✅ On récupère juste le texte à afficher
        speak(response["output"])         # ✅ Et on le lit avec gTTS

    # Ajouter la réponse dans l'historique
    st.session_state.history.append(response["output"])
