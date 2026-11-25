from showtime.scrapers.base import ChainScraper
from showtime.scrapers.vue import VueClient

SCRAPERS: dict[str, type[ChainScraper]] = {"vue": VueClient}
