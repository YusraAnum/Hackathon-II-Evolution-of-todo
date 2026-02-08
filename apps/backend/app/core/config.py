from pydantic_settings import Settings


class Settings(Settings):
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "https://localhost",
        "https://localhost:3000",
        "https://localhost:8000",
        "https://localhost:8080",
    ]


settings = Settings()