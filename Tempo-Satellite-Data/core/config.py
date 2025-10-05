from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    # Database Ayarları
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_USER: str = Field("root", env="DB_USER")
    DB_PASS: str = Field("...", env="DB_PASS")
    DB_NAME: str = Field("openweather", env="DB_NAME")

    # Alternatif: Tek satırda bağlantı stringi (opsiyonel)
    DATABASE_URL: str | None = Field(None, env="DATABASE_URL")

    # API Key’ler
    OPENWEATHER_API_KEY: str = Field(..., env="OPENWEATHER_API_KEY")
    NASA_API_KEY: str | None = Field(None, env="NASA_API_KEY")
    EARTHDATA_USER: str | None = Field(None, env="EARTHDATA_USER")
    EARTHDATA_PASS: str | None = Field(None, env="EARTHDATA_PASS")

    # Scheduler Ayarları
    TEMPO_DAILY_HOUR: int = Field(2, env="TEMPO_DAILY_HOUR")
    AIRNOW_INTERVAL_MINUTES: int = Field(30, env="AIRNOW_INTERVAL_MINUTES")
    OPENWEATHER_INTERVAL_MINUTES: int = Field(30, env="OPENWEATHER_INTERVAL_MINUTES")

    # Model yolu
    ml_model_dir: Path = Field(Path("data/models"), env="ML_MODEL_DIR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()