try:
    import mrequests as requests  # MicroPython environment
except ImportError:
    import requests


class ImmichConnector:
    def __init__(self, base_url: str, api_key: str):
        if not base_url.endswith("/api"):
            base_url += "/api"

        self.BASE_URL = base_url
        self.API_KEY = api_key

        self.headers = {
            "x-api-key": f"{api_key}",
            "Accept": "application/json",
        }

    def test_connection(self) -> str:
        ENDPOINT = "auth/validateToken"

        response = requests.post(
            f"{self.BASE_URL}/{ENDPOINT}",
            headers=self.headers,
        )

        if response.status_code == 200:
            return "Connection successful"

        if response.status_code == 401:
            return "Invalid API key"

        return "Connection failed, is the endpoint correct?"

    def download_asset_to_file(self, id: str, file_name: str) -> str:
        ENDPOINT = f"assets/{id}/thumbnail?size=preview"

        response = requests.get(
            f"{self.BASE_URL}/{ENDPOINT}",
            headers=self.headers,
        )

        with open(f"{file_name}.jpeg", "wb") as file:
            file.write(response.content)

        return f"Asset downloaded successfully as {file_name}.jpeg"

    def download_asset_to_memory(self, id: str) -> bytes:
        ENDPOINT = f"assets/{id}/thumbnail?size=preview"

        response = requests.get(
            f"{self.BASE_URL}/{ENDPOINT}",
            headers=self.headers,
        )

        return response.content

    def get_asset_from_album(self, id, entry_num=None):
        ENDPOINT = f"albums/{id}"

        response = requests.get(
            f"{self.BASE_URL}/{ENDPOINT}",
            headers=self.headers,
        )

        response_data = response.json()

        if entry_num is not None:
            return response_data["assets"][entry_num]
