from pydantic_settings import BaseSettings

class GlobalConfig(BaseSettings):
    strict_mode: bool = False

    class Config:
        env_file = ".env"

settings = GlobalConfig() 
