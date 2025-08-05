from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    tsetmc_username: str
    tsetmc_password: str
    mongo_uri: str

    class Config:
        env_file = ".env"

settings = Settings()
