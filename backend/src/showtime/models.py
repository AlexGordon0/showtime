from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Chain(Base):
    __tablename__ = "chains"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    website: Mapped[str]


class Cinema(Base):
    __tablename__ = "cinemas"
    __table_args__ = (UniqueConstraint("chain_id", "external_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    chain_id: Mapped[int] = mapped_column(ForeignKey("chains.id"))
    external_id: Mapped[str]
    name: Mapped[str]
    city: Mapped[str | None]
    postcode: Mapped[str | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]


class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int | None]
    runtime_minutes: Mapped[int | None]
    certificate: Mapped[str | None]
    poster_url: Mapped[str | None]
    tmdb_id: Mapped[int | None] = mapped_column(unique=True)


class Showtime(Base):
    __tablename__ = "showtimes"
    __table_args__ = (UniqueConstraint("cinema_id", "external_id"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id", ondelete="CASCADE"))
    external_id: Mapped[str]
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    formats: Mapped[list[str]] = mapped_column(ARRAY(String), server_default="{}")
    screen: Mapped[str | None]
    booking_url: Mapped[str | None]
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
