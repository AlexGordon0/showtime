from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, Self

USER_AGENT = "showtime-scraper/0.1 (+https://github.com/AlexGordon0/showtime)"


class ScraperError(Exception):
    """Exception raised for errors when scraping."""


@dataclass(frozen=True, kw_only=True)
class RawCinema:
    external_id: str
    name: str
    city: str | None = None
    postcode: str | None = None
    latitude: float | None = None
    longitude: float | None = None


@dataclass(frozen=True, kw_only=True)
class RawFilm:
    title: str
    year: int | None = None
    runtime_minutes: int | None = None
    certificate: str | None = None
    poster_url: str | None = None


class Format(StrEnum):
    THREE_D = "3d"
    SUBTITLED = "subtitled"
    AUDIO_DESCRIBED = "audio-described"
    AUTISM_FRIENDLY = "autism-friendly"
    OVER_18 = "over-18"


@dataclass(frozen=True, kw_only=True)
class RawShowtime:
    film: RawFilm
    external_id: str
    starts_at: datetime
    formats: tuple[Format, ...] = ()
    screen: str | None = None
    booking_url: str | None = None


class ChainScraper(Protocol):
    name: str
    slug: str
    website: str

    def __enter__(self) -> Self: ...
    def __exit__(self, *exc: object) -> None: ...

    def fetch_cinemas(self) -> list[RawCinema]: ...
    def fetch_showtimes(self, cinema_external_id: str) -> list[RawShowtime]: ...
