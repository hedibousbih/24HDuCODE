import requests

BASE_URL = "https://app-584240518682.europe-west9.run.app/api/"
AUTH_TOKEN = "Token 8jW6Dy4TCHGXTJVTJKi0zK5iBFxAIWOZ"

HEADERS = {
    'Authorization': AUTH_TOKEN,
    'Content-Type': 'application/json'
}

def get_restaurants():
    """Récupère la liste des restaurants"""
    url = BASE_URL + "restaurants/"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()  
        print(f"Erreur {response.status_code}: {response.text}")
        return None

def create_reservation(client_id, restaurant_id, date, meal_id, guests, special_requests=""):
    """Crée une nouvelle réservation"""
    url = BASE_URL + "reservations/"
    data = {
        "client": client_id,
        "restaurant": restaurant_id,
        "date": date,
        "meal": meal_id,
        "number_of_guests": guests,
        "special_requests": special_requests
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code == 201:
        return response.json()  # Retourne la réservation créée
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

def delete_reservation(reservation_id):
    """Supprime une réservation par son ID"""
    url = BASE_URL + f"reservations/{reservation_id}/"
    response = requests.delete(url, headers=HEADERS)
    
    if response.status_code == 204:
        print(f"Réservation {reservation_id} supprimée avec succès.")
        return True
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Récupérer les restaurants
    restaurants = get_restaurants()
    if restaurants:
        print("Restaurants disponibles:", restaurants)

    # Créer une réservation
    reservation = create_reservation(client_id=1038, restaurant_id=19, date="2024-12-25", meal_id=19, guests=4, special_requests="Table près de la fenêtre")
    if reservation:
        print("Réservation créée:", reservation)

    # Supprimer une réservation (exemple avec un ID fictif)
    delete_reservation(42)
