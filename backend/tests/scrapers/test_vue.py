import json
from pathlib import Path

from showtime.scrapers.base import RawCinema
from showtime.scrapers.vue import parse_cinemas

FIXTURES: Path = Path(__file__).resolve().parent.parent / "fixtures"
CINEMA_JSON = json.loads((FIXTURES / "vue" / "cinemas.json").read_text())


def test_parse_cinemas_returns_correct_count() -> None:
    assert len(parse_cinemas(CINEMA_JSON)) == 91


def test_cinema_name_has_correct_external_id() -> None:
    cinemas: list[RawCinema] = parse_cinemas(CINEMA_JSON)
    assert cinemas[0].name == "Accrington" and cinemas[0].external_id == "10051"
    assert (
        cinemas[60].name == "Manchester (The Printworks)"
        and cinemas[60].external_id == "10091"
    )
    assert cinemas[82].name == "Swansea" and cinemas[82].external_id == "10058"
