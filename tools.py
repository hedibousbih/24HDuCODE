import requests

class RestaurantReservationTool:
    def __init__(self):
        self.api_url = "https://hotel-api.com/restaurant"
        self.api_key = "Token 8jW6Dy4TCHGXTJVTJKi0zK5iBFxAIWOZ"

    def reserve_table(self, reservation_details):
        response = requests.post(
            self.api_url,
            json=reservation_details,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"