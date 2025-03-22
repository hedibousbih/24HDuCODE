import requests

API_KEY = "your_mistral_api_key"
ENDPOINT = "https://api.mistral.ai/generate"

def get_mistral_response(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"prompt": prompt, "max_tokens": 200}
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("text", "No response generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"