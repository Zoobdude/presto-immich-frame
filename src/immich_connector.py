import requests


class ImmichConnector:
    def __init__(self, base_url: str, API_KEY: str, filters: dict):
        if not base_url.endswith("/api"):
            base_url += "/api"

        self.base_url = base_url
        self.API_KEY = API_KEY
        self.filters = filters

        self.headers = {
            "x-api-key": f"{API_KEY}",
            "Accept": "application/json",
        }

    def test_connection(self):
        ENDPOINT = "auth/validateToken"

        try:
            response = requests.post(
                f"{self.base_url}/{ENDPOINT}",
                headers=self.headers,
            )

        except requests.exceptions.RequestException:
            return "Connection failed, is the endpoint correct?"

        if response.status_code == 200:
            return "Connection successful"

        if response.status_code == 401:
            return "Invalid API key"

    def _download_asset_to_file(self, id: str, file_name: str):
        ENDPOINT = f"assets/{id}/thumbnail?size=preview"

        response = requests.get(
            f"{self.base_url}/{ENDPOINT}",
            headers=self.headers,
        )
        with open(f"{file_name}.jpeg", "wb") as file:
            file.write(response.content)

    def get_asset_from_album(self, id, entry_num=None):
        ENDPOINT = f"albums/{id}"

        response = requests.get(
            f"{self.base_url}/{ENDPOINT}",
            headers=self.headers,
        )

        response_data = response.json()

        if entry_num is not None:
            return response_data["assets"][entry_num]
