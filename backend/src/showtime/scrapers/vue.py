import time
from json import JSONDecodeError
from typing import Any, Self

import httpx

from showtime.scrapers.base import USER_AGENT, RawCinema, RawShowtime, ScraperError

MIN_REQUEST_INTERVAL = 1.0  # seconds

BASE_URL = "https://www.myvue.com"
CINEMAS_PATH = "/api/microservice/showings/cinemas"


class VueClient:
    slug = "vue"

    def fetch_cinemas(self) -> list[RawCinema]:
        return parse_cinemas(self._get(CINEMAS_PATH))

    def fetch_showtimes(self, cinema_external_id: str) -> list[RawShowtime]:
        path = f"{CINEMAS_PATH}/{cinema_external_id}/films"
        return parse_showtimes(self._get(path, params={"includesSession": "true"}))

    def __init__(self) -> None:
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
            timeout=20,
            follow_redirects=True,
        )
        self._token: str | None = None
        self._last_request_at: float | None = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self._http.close()

    def _get(self, path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        if self._token is None:
            self._token = self._fetch_token()
        response = self._send(path, params)
        if response.status_code == 401:
            self._token = self._fetch_token()
            response = self._send(path, params)

        response.raise_for_status()

        try:
            body: dict[str, Any] = response.json()
        except JSONDecodeError:
            raise ScraperError(f"Vue: expected JSON from {path}.") from JSONDecodeError
        if body.get("responseCode") != 0:
            raise ScraperError(
                f"Vue: {body.get('responseCode')}: {body.get('errorMessage')}"
            )
        return body

    def _fetch_token(self) -> str:
        response = self._request("/")
        response.raise_for_status()
        token = self._http.cookies.get("microservicesToken")
        if token is None:
            raise ScraperError(
                "Vue: homepage response had no microservicesToken cookie"
            )
        return token

    def _send(self, path: str, params: dict[str, str] | None = None) -> httpx.Response:
        headers = {"Authorization": f"Bearer {self._token}"}
        return self._request(path, headers=headers, params=params)

    def _request(self, path: str, **kwargs: Any) -> httpx.Response:
        self._throttle()
        return self._http.get(path, **kwargs)

    def _throttle(self) -> None:
        if self._last_request_at is not None:
            time_elapsed = time.monotonic() - self._last_request_at
            if time_elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - time_elapsed)
        self._last_request_at = time.monotonic()


def parse_cinemas(data: dict[str, Any]) -> list[RawCinema]:
    cinema_list: list[RawCinema] = []
    for starting_letter in data["result"]:
        for cinema in starting_letter["cinemas"]:
            cinema_list.append(
                RawCinema(
                    external_id=cinema["cinemaId"],
                    name=cinema["cinemaName"],
                )
            )
    return cinema_list


def parse_showtimes(data: dict[str, Any]) -> list[RawShowtime]:
    pass
