import requests
from modules.constants import THESPEAR_API_BASE_URL, THESPEAR_API_VERSION

class LoadSheddingAPI:
    def __init__(self, base_url=THESPEAR_API_BASE_URL, version=THESPEAR_API_VERSION):
        self.base_url = base_url
        self.version = version

    def get_status(self):
        url = f"{self.base_url}/{self.version}/status"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            status_code = data['status_code']
            stage = status_code - 1
            status_text = data['status_text']
            return {
                'status_code': status_code,
                'stage': stage,
                'status_text': status_text
            }
        except requests.RequestException as e:
            print(f"Error fetching status: {e}")
            return None

    def get_provinces(self):
        url = f"{self.base_url}/{self.version}/provinces"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching provinces: {e}")
            return None

    def get_municipalities(self, province_id):
        url = f"{self.base_url}/{self.version}/municipalities/{province_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching municipalities for province ID {province_id}: {e}")
            return None

    def get_suburbs(self, municipality_id):
        url = f"{self.base_url}/{self.version}/suburbs/{municipality_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("suburbs", [])
        except requests.RequestException as e:
            print(f"Error fetching suburbs for municipality ID {municipality_id}: {e}")
            return None

    def get_schedule(self, suburb_id, province_id):
        url = f"{self.base_url}/{self.version}/schedule/{suburb_id}/{province_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'error' in data:
                print(f"Error: {data['error']}")
                return None
            return {
                'area_info': data['area_info'],
                'schedule': data['schedule']
            }
        except requests.RequestException as e:
            print(f"Error fetching schedule for suburb ID {suburb_id} and province ID {province_id}: {e}")
            return None

    def get_combined_schedule(self, *suburb_province_pairs):
        ids = "/".join(suburb_province_pairs)
        url = f"{self.base_url}/{self.version}/combined_schedule/{ids}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching combined schedule for {ids}: {e}")
            return None

    def get_inverted_schedule(self, *suburb_province_pairs):
        ids = "/".join(suburb_province_pairs)
        url = f"{self.base_url}/{self.version}/inverted_schedule/{ids}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching inverted schedule for {ids}: {e}")
            return None

