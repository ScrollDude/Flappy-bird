from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATABASE_URL(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"


settings = Settings()
