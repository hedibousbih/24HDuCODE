# front.py
import streamlit as st
from gtts import gTTS
import os
import tempfile
from langchain_core.messages import HumanMessage, AIMessage
from agent_config import agent  # Ton agent avec le tool get_restaurants

# Configuration de la page Streamlit
st.set_page_config(page_title="Assistant Hôtel California", layout="centered")
st.title("🏨 Assistant IA – Hôtel California")

# Initialisation de l'historique utilisateur
if "history" not in st.session_state:
    st.session_state.history = []  # Contient objets HumanMessage / AIMessage

# 🔊 Fonction pour lire le texte avec gTTS
def speak(text):
    tts = gTTS(text=text, lang='fr')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# ✅ Afficher tout l'historique avant la nouvelle saisie
for msg in st.session_state.history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# 💬 Interface du chat
user_input = st.chat_input("Posez une question sur les restaurants, les spas, etc.")
if user_input:
    # Affichage immédiat du message utilisateur
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.history.append(HumanMessage(content=user_input))

    # Appel à l'agent
    response = agent.invoke(user_input)  # ← dict avec "input" et "output"
    bot_message = response["output"]

    # Affichage du message assistant
    with st.chat_message("assistant"):
        st.markdown(bot_message)
        speak(bot_message)

    # Enregistrer dans l’historique avec type AIMessage
    st.session_state.history.append(AIMessage(content=bot_message))
