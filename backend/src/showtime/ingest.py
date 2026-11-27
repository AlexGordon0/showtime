from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from showtime.models import Chain, Cinema, Film, Showtime
from showtime.scrapers.base import ChainScraper, RawCinema, RawFilm, RawShowtime


def upsert_chain(session: Session, scraper: ChainScraper) -> int:
    stmt = insert(Chain).values(
        slug=scraper.slug, name=scraper.name, website=scraper.website
    )
    stmt_conflict = stmt.on_conflict_do_update(
        index_elements=[Chain.slug],
        set_={
            "name": stmt.excluded.name,
            "website": stmt.excluded.website,
        },
    ).returning(Chain.id)

    return session.execute(stmt_conflict).scalar_one()


def upsert_cinemas(
    session: Session, chain_id: int, cinemas: Sequence[RawCinema]
) -> dict[str, int]:
    """external_ids must be unique within batch, otherwise insert fails"""
    if not cinemas:
        return {}

    rows = [
        {
            "chain_id": chain_id,
            "external_id": cinema.external_id,
            "name": cinema.name,
            "city": cinema.city,
            "postcode": cinema.postcode,
            "latitude": cinema.latitude,
            "longitude": cinema.longitude,
        }
        for cinema in cinemas
    ]

    stmt = insert(Cinema).values(rows)
    stmt_conflict = stmt.on_conflict_do_update(
        index_elements=[Cinema.chain_id, Cinema.external_id],
        set_={
            "name": stmt.excluded.name,
            "city": stmt.excluded.city,
            "postcode": stmt.excluded.postcode,
            "latitude": stmt.excluded.latitude,
            "longitude": stmt.excluded.longitude,
        },
    ).returning(Cinema.external_id, Cinema.id)

    result = session.execute(stmt_conflict)
    return {row.external_id: row.id for row in result}


def get_or_create_film(session: Session, raw: RawFilm) -> int:
    """only fills NULL fields, never overwrites already filled data."""
    # TODO: match on normalised title / film aliases
    film = session.scalar(select(Film).where(Film.title == raw.title))

    if film is None:
        film = Film(
            title=raw.title,
            year=raw.year,
            runtime_minutes=raw.runtime_minutes,
            certificate=raw.certificate,
            poster_url=raw.poster_url,
        )
        session.add(film)
        session.flush()
        return film.id

    if film.year is None:
        film.year = raw.year
    if film.runtime_minutes is None:
        film.runtime_minutes = raw.runtime_minutes
    if film.certificate is None:
        film.certificate = raw.certificate
    if film.poster_url is None:
        film.poster_url = raw.poster_url

    session.flush()
    return film.id


def upsert_showtimes(
    session: Session, cinema_id: int, showtimes: Sequence[RawShowtime]
) -> int:
    """external_ids must be unique within batch, otherwise insert fails"""
    if not showtimes:
        return 0

    films = {s.film for s in showtimes}
    film_to_id = {film: get_or_create_film(session, film) for film in films}

    rows = [
        {
            "cinema_id": cinema_id,
            "film_id": film_to_id[s.film],
            "external_id": s.external_id,
            "starts_at": s.starts_at,
            "formats": list(s.formats),
            "screen": s.screen,
            "booking_url": s.booking_url,
        }
        for s in showtimes
    ]

    stmt = insert(Showtime).values(rows)
    stmt_conflict = stmt.on_conflict_do_update(
        index_elements=[Showtime.cinema_id, Showtime.external_id],
        set_={
            "film_id": stmt.excluded.film_id,
            "starts_at": stmt.excluded.starts_at,
            "formats": stmt.excluded.formats,
            "screen": stmt.excluded.screen,
            "booking_url": stmt.excluded.booking_url,
            "scraped_at": func.now(),
        },
    )

    session.execute(stmt_conflict)
    return len(rows)
