from fastapi import FastAPI
from sqlalchemy import text

from showtime.db import engine

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
