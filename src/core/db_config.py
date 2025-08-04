from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


base_path = Path(__file__).resolve().parent.parent


class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=base_path / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    db_host: str = Field(alias="POSTGRES_HOST")
    db_port: int = Field(alias="POSTGRES_PORT")
    db_name: str = Field(alias="POSTGRES_NAME")
    db_user: str = Field(alias="POSTGRES_USER")
    db_pass: str = Field(alias="POSTGRES_PASSWORD")

    @computed_field
    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


db_settings = DataBaseSettings()
