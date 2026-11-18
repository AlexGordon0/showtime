from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://showtime:devpassword@localhost:5432/showtime"
    )


settings = Settings()
