from langchain.tools import Tool
from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from UseAPI import get_restaurants,create_reservation, get_restaurant_name_to_id_map,get_meal_name_to_id_map
from parser import SafeAgentOutputParser

# Tool
restaurant_tool = Tool.from_function(
    func=get_restaurants,
    name="getRestaurants",
    description="Utilise cette fonction pour obtenir la liste des restaurants disponibles à l'hôtel.",
    verbose=True,
    handle_parsing_errors=True  # important
)

def create_reservation_tool_func(client_id, restaurant_name, date, meal_name, guests, special_requests=""):
    """
    Crée une réservation à partir du nom du restaurant et du nom du repas (ex: dîner, déjeuner).
    """
    name_to_id = get_restaurant_name_to_id_map()
    restaurant_id = name_to_id.get(restaurant_name.lower())

    if not restaurant_id:
        return f"❌ Le restaurant '{restaurant_name}' est introuvable."

    # Mapping du nom de repas → id
    meal_map = get_meal_name_to_id_map()
    meal_id = meal_map.get(meal_name.lower())

    if not meal_id:
        return f"❌ Le repas '{meal_name}' est inconnu. Essayez avec petit déjeuner, déjeuner ou dîner."

    # Appel à l’API
    reservation = create_reservation(client_id, restaurant_id, date, meal_id, guests, special_requests)
    
    if reservation:
        return (
            f"✅ Réservation confirmée pour {reservation['number_of_guests']} personnes "
            f"au restaurant {restaurant_name} le {reservation['date']} pour {meal_name}."
        )
    else:
        return "❌ La réservation a échoué."

    
create_reservation_tool = Tool.from_function(
    func=create_reservation_tool_func,
    name="createReservation",
    description=(
        "Crée une réservation pour un client dans un restaurant. "
        "Utilise le nom du restaurant au lieu de l'ID. "
        "Arguments : client_id (int), restaurant_name (str), date (str au format YYYY-MM-DD), "
        "meal_id (int), guests (int), special_requests (str optionnel)"
    )
)



load_dotenv()
model = init_chat_model("mistral-large-latest", model_provider="mistralai")



restaurant_tool = Tool.from_function(
    func=get_restaurants,
    name="getRestaurants",
    description="Utilise cette fonction pour obtenir la liste des restaurants disponibles à l'hôtel.",
    
)

def create_reservation_tool_func(client_id, restaurant_name, date, meal_id, guests, special_requests=""):
    """
    Wrapper pour créer une réservation avec un nom de restaurant (au lieu de son ID).
    """
    name_to_id = get_restaurant_name_to_id_map()
    restaurant_id = name_to_id.get(restaurant_name.lower())

    if not restaurant_id:
        return f"❌ Le restaurant '{restaurant_name}' est introuvable."

    reservation = create_reservation(client_id, restaurant_id, date, meal_id, guests, special_requests)
    
    if reservation:
        return (
            f"✅ Réservation confirmée pour {reservation['number_of_guests']} personnes "
            f"au restaurant {restaurant_name} le {reservation['date']} (repas ID {reservation['meal']})."
        )
    else:
        return "❌ La réservation a échoué."
    
create_reservation_tool = Tool.from_function(
    func=create_reservation_tool_func,
    name="createReservation",
    description=(
        "Crée une réservation pour un client dans un restaurant. "
        "Utilise le nom du restaurant et le nom du repas (par exemple : petit déjeuner, déjeuner, dîner). "
        "Arguments : client_id (int), restaurant_name (str), date (YYYY-MM-DD), "
        "meal_name (str), guests (int), special_requests (str, optionnel)."
    )
)



load_dotenv()
model = init_chat_model("mistral-large-latest", model_provider="mistralai")

tools = [restaurant_tool, create_reservation_tool]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"output_parser": SafeAgentOutputParser()},
    max_iterations=5
)

