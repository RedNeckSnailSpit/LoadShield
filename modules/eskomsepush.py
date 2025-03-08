import requests
from modules.constants import ESP_API_BASE_URL

class EskomSePushAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = ESP_API_BASE_URL
        self.headers = {
            'Token': f'{self.api_token}'
        }

    def get_status(self):
        url = f"{self.base_url}/status"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching status: {e}")
            return

    def get_area_info(self, area_id):
        url = f"{self.base_url}/area?id={area_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching area info: {e}")
            return None

    def get_areas_nearby(self, lat, lon):
        url = f"{self.base_url}/areas_nearby?lat={lat}&lon={lon}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching nearby areas: {e}")
            return None

    def search_areas(self, text):
        url = f"{self.base_url}/areas_search?text={text}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching areas: {e}")
            return None

    def check_allowance(self):
        url = f"{self.base_url}/api_allowance"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            allowance = response.json().get('allowance', {})
            allowance['remaining'] = allowance.get('limit', 0) - allowance.get('count', 0)
            return allowance
        except requests.RequestException as e:
            print(f"Error checking allowance: {e}")
            return None
