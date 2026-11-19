from showtime.models import Base


def test_models_register_expected_tables() -> None:
    assert set(Base.metadata.tables) == {"chains", "cinemas", "films", "showtimes"}
