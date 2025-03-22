from langchain.tools import Tool
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from UseAPI import get_restaurants

# Tool
restaurant_tool = Tool.from_function(
    func=get_restaurants,
    name="getRestaurants",
    description="Utilise cette fonction pour obtenir la liste des restaurants disponibles à l'hôtel.",
    verbose=True,
    handle_parsing_errors=True  # important
)

# Load model
load_dotenv()
model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# 👇 Agent corrigé ici :
agent = initialize_agent(
    tools=[restaurant_tool],
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ✅ Plus tolérant
    verbose=True,
    handle_parsing_errors=True
)
