import requests


BASE_URL = "https://swapi.dev/api/"


class SWAPIError(Exception):
    """Base exception for errors while communicating with SWAPI."""


class SWAPIRequestError(SWAPIError):
    """Raised when SWAPI cannot be reached."""


class SWAPIResponseError(SWAPIError):
    """Raised when SWAPI returns invalid data."""


class SWAPIClient:
    def fetch_all(self, resource):
        url = BASE_URL + resource
        all_results = []

        while url:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
            except requests.Timeout as exc:
                raise SWAPIRequestError(
                    "The request to SWAPI timed out."
                ) from exc
            except requests.RequestException as exc:
                raise SWAPIRequestError(
                    "Could not retrieve data from SWAPI."
                ) from exc

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as exc:
                raise SWAPIResponseError(
                    "SWAPI returned an invalid JSON response."
                ) from exc

            if not isinstance(data, dict) or not isinstance(
                data.get("results"), list
            ):
                raise SWAPIResponseError(
                    "SWAPI returned an unexpected response format."
                )

            next_url = data.get("next")

            if next_url is not None and not isinstance(next_url, str):
                raise SWAPIResponseError(
                    "SWAPI returned an invalid pagination URL."
                )

            all_results.extend(data["results"])
            url = next_url

        return all_results