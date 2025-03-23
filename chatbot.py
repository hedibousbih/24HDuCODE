import os
import uuid
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv, find_dotenv
from agent_config import agent

load_dotenv(find_dotenv())
print("Bienvenue à l’Hôtel California ! Camille est là pour vous aider.")
print("Tapez 'exit' pour quitter.")

while True:
    user_input = input("Vous > ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Camille > Merci pour votre visite. À bientôt ! 🌟")
        break

    response = agent.invoke(user_input)
    print("Camille >", response)

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

# Charger la clé API Mistral
if not os.environ.get("MISTRAL_API_KEY"):
    from getpass import getpass
    os.environ["MISTRAL_API_KEY"] = getpass("Enter Mistral API key: ")

# Initialiser le modèle Mistral
model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Créer le prompt de Camille
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "Tu es Camille, l'assistante virtuelle de l’Hôtel California. "
        "Tu es serviable, polie, toujours prête à aider les clients. "
        "Tu parles plusieurs langues, principalement le français et l’anglais. "
        "Adapte ta réponse à la langue du client automatiquement. "
        "Si tu ne comprends pas, demande poliment plus de détails. "
        "Fais tout ton possible pour créer une expérience agréable."
        "Ne réponds pas directement à l'utilisateur et n'indique pas la réponse finale tant que tu n'as pas terminé tous les appels d'outils nécessaires."
        "Si l'utilisateur parle d’un moment de la journée (ex: ce soir, ce midi), associe-le automatiquement à un repas disponible."
        "Ne donne jamais la réponse finale tant que tous les outils nécessaires n'ont pas été appelés et que toutes les observations ont été reçues."
        "Quand l’utilisateur mentionne un repas comme 'déjeuner', 'dîner', ou 'souper', "
        "traduis-le automatiquement en nom exact de repas disponible via l’API, comme 'Lunch' ou 'Dinner'. "
        "N’utilise que les noms de repas attendus par l’API ('Breakfast', 'Lunch', 'Dinner')."
        "Important : Dans chaque réponse, ne produis soit une action (avec Action: ...), soit une réponse finale (avec Final Answer: ...), mais jamais les deux en même temps. Sinon, le système échouera."


    )),
    MessagesPlaceholder(variable_name="messages")
])

# Fonction de traitement des messages
def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": state["messages"] + [response]}

# Créer le graph LangGraph
workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Mémoire persistante
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Initialiser la session utilisateur
user_id = input("Entrez votre prénom : ").strip().lower()
config = {"configurable": {"thread_id": f"user_{user_id}"}}
messages = []

print("\nBienvenue à l'Hôtel California ! Camille est là pour vous aider 😊")
print("Tapez 'exit' pour quitter.\n")

# Boucle de conversation
while True:
    user_input = input(f"{user_id} > ").strip()
    if user_input.lower() in {"exit", "quit"}:
        print("Camille > Merci de votre visite. À bientôt ! 🌟")
        break

    messages.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": messages}, config)
    response = result["messages"][-1]
    messages = result["messages"]

    print(f"Camille > {response.content}")
