from tools import RestaurantReservationTool
from langchain_setup import create_chain

def process_query(query):
    # Initialize the tool
    restaurant_tool = RestaurantReservationTool()

    # Determine the action based on user query
    if "reserve" in query:
        context = restaurant_tool.reserve_table({"date": "2025-03-23", "time": "20:00", "guests": 2})
    else:
        context = {"info": "General information about Hôtel California."}

    # Use LangChain to generate a response
    chain = create_chain()
    response = chain.run(context=context, query=query)
    return response