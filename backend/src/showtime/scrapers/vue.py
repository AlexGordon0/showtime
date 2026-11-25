import time
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Self
from zoneinfo import ZoneInfo

import httpx

from showtime.scrapers.base import (
    USER_AGENT,
    RawCinema,
    RawFilm,
    RawShowtime,
    ScraperError,
)

MIN_REQUEST_INTERVAL = 1.0  # seconds

BASE_URL = "https://www.myvue.com"
CINEMAS_PATH = "/api/microservice/showings/cinemas"

LONDON = ZoneInfo("Europe/London")


class VueClient:
    name = "Vue"
    slug = "vue"
    website = BASE_URL

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

    def fetch_cinemas(self) -> list[RawCinema]:
        try:
            return parse_cinemas(self._get(CINEMAS_PATH))
        except (ValueError, TypeError, KeyError) as e:
            raise ScraperError("Vue: unexpected response shape") from e

    def fetch_showtimes(self, cinema_external_id: str) -> list[RawShowtime]:
        try:
            path = f"{CINEMAS_PATH}/{cinema_external_id}/films"
            return parse_showtimes(self._get(path, params={"includesSession": "true"}))
        except (ValueError, TypeError, KeyError) as e:
            raise ScraperError("Vue: unexpected response shape") from e

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
        except JSONDecodeError as e:
            raise ScraperError(f"Vue: expected JSON from {path}.") from e
        if body.get("responseCode") != 0:
            raise ScraperError(
                f"Vue: {body.get('responseCode')}: {body.get('errorMessage')}"
            )
        return body

    def _fetch_token(self) -> str:
        self._request("/")
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
        try:
            self._throttle()
            response = self._http.get(path, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as e:
            raise ScraperError(f"Vue: request to {path} failed: {e}") from e

    def _throttle(self) -> None:
        if self._last_request_at is not None:
            time_elapsed = time.monotonic() - self._last_request_at
            if time_elapsed < MIN_REQUEST_INTERVAL:
                time.sleep(MIN_REQUEST_INTERVAL - time_elapsed)
        self._last_request_at = time.monotonic()


def parse_cinemas(data: dict[str, Any]) -> list[RawCinema]:
    return [
        RawCinema(
            external_id=cinema["cinemaId"],
            name=cinema["fullName"],
            city=cinema["cinemaName"],
        )
        for flat_cinemas in data["result"]
        for cinema in flat_cinemas["cinemas"]
    ]


def parse_showtimes(data: dict[str, Any]) -> list[RawShowtime]:
    return [
        RawShowtime(
            film=_parse_film(film_data),
            external_id=showing["sessionId"],
            starts_at=_parse_time(showing["startTime"]),
            screen=showing["screenName"],
            booking_url=BASE_URL + showing["bookingUrl"],
        )
        for film_data in data["result"]
        for showing_group in film_data["showingGroups"]
        for showing in showing_group["sessions"]
    ]


def _parse_film(data: dict[str, Any]) -> RawFilm:
    return RawFilm(
        title=data["filmTitle"],
        runtime_minutes=_runtime(data),
        certificate=_certificate(data["certificate"]["name"]),
        poster_url=data["posterImageSrc"],
    )


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=LONDON)


def _runtime(film: dict[str, Any]) -> int | None:
    return film["runningTime"] if not film["isDurationUnknown"] else None


def _certificate(name: str | None) -> str | None:
    if name is None or name.lower() == "tbc":
        return None
    return name.upper()
