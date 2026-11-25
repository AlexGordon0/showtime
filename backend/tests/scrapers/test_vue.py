import json
from datetime import datetime, timedelta
from pathlib import Path

from showtime.scrapers.base import RawCinema, RawFilm, RawShowtime
from showtime.scrapers.vue import LONDON, _certificate, parse_cinemas, parse_showtimes

FIXTURES: Path = Path(__file__).resolve().parent.parent / "fixtures"
CINEMAS_JSON = json.loads((FIXTURES / "vue" / "cinemas.json").read_text())
SHOWINGS_JSON = json.loads((FIXTURES / "vue" / "showing_groups.json").read_text())

CINEMAS = parse_cinemas(CINEMAS_JSON)
SHOWTIMES = parse_showtimes(SHOWINGS_JSON)


def _cinema(cid: str) -> RawCinema:
    return next(c for c in CINEMAS if c.external_id == cid)


def _film(title: str) -> RawFilm:
    return next(s.film for s in SHOWTIMES if s.film.title == title)


def _session(sid: str) -> RawShowtime:
    return next(s for s in SHOWTIMES if s.external_id == sid)


def test_parse_cinemas_returns_correct_count() -> None:
    assert len(CINEMAS) == 91


def test_parse_showtimes_returns_correct_count() -> None:
    assert len(SHOWTIMES) == 202


def test_cinema_ids_are_unique() -> None:
    assert len({c.external_id for c in CINEMAS}) == len(CINEMAS)


def test_session_ids_are_unique() -> None:
    assert len({s.external_id for s in SHOWTIMES}) == len(SHOWTIMES)


def test_cinema_has_correct_names() -> None:
    cinema_0 = _cinema("10051")
    assert cinema_0.name == "Accrington - The Viaduct"
    assert cinema_0.city == "Accrington"
    cinema_1 = _cinema("10091")
    assert cinema_1.name == "Manchester Printworks"
    assert cinema_1.city == "Manchester (The Printworks)"
    cinema_2 = _cinema("10058")
    assert cinema_2.name == "Swansea - York Street"
    assert cinema_2.city == "Swansea"


def test_random_session_parsed_correctly() -> None:
    showtime = _session("141272")
    assert showtime.external_id == "141272"
    assert showtime.starts_at == datetime(2026, 12, 21, 19, 15, tzinfo=LONDON)
    assert showtime.formats == ()
    assert showtime.screen == "Screen 3"
    assert (
        showtime.booking_url
        == "https://www.myvue.com/book-tickets/summary/10051/HO00020262/141272"
    )


def test_random_film_parsed_correctly() -> None:
    rocky = _film("I Play Rocky")
    assert rocky.title == "I Play Rocky"
    assert rocky.year is None
    assert rocky.runtime_minutes == 128
    assert rocky.certificate == "12A"
    assert (
        rocky.poster_url
        == "https://www.myvue.com/-/media/vuecinemas/img/import/e8ae03e7-805f-4633-86dd-507d68433149_i-play-rocky_posters_iplayrocky_screenres_712px.jpg?rev=7689e6000d084c7c92994efa4af6c5bf"
    )


def test_timezone_is_applied_to_every_start_time() -> None:
    assert all(showtime.starts_at.tzinfo is not None for showtime in SHOWTIMES)


def test_tbc_certificate_is_none() -> None:
    focker = _film("Focker-in-Law")
    assert focker.certificate is None


def test_unknown_runtime_is_none() -> None:
    doomsday = _film("Avengers: Doomsday")
    assert doomsday.runtime_minutes is None


throwaway_showings_json = {
    "result": [
        {
            "showingGroups": [
                {
                    "sessions": [
                        {
                            "sessionId": "100000",
                            "startTime": "2026-07-15T19:30:00",
                            "bookingUrl": "/book-tickets/x",
                            "screenName": "Screen 10",
                        }
                    ]
                }
            ],
            "filmId": "HO00020283",
            "filmTitle": "The Hunger Games: Sunrise On The Reaping",
            "releaseDate": "2026-11-18T00:00:00",
            "certificate": {"name": "15"},
            "posterImageSrc": "https://www.myvue.com/-/media/vuecinemas/img/import/4e807691-17ef-406a-8ef8-a5bdff8b4e3c_the-hunger-games-sunrise-on-the-reaping_posters_gb_english_sols.jpg?rev=531c4e48f6bb4f7087b26f94435591ac",
            "isDurationUnknown": False,
            "runningTime": 158,
        }
    ]
}


def test_time_works_with_bst() -> None:
    showing = parse_showtimes(throwaway_showings_json)[0]
    assert showing.starts_at.utcoffset() == timedelta(hours=1)


def test_certificate_parsing() -> None:
    assert _certificate("tbc") is None
    assert _certificate("u") == "U"
    assert _certificate("U") == "U"
    assert _certificate("12a") == "12A"
    assert _certificate("12A") == "12A"
    assert _certificate("18") == "18"
