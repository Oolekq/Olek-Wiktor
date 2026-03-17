from pydantic_settings import BaseSettings
from pydantic import (
    BaseModel, Field, EmailStr, ConfigDict, 
    field_validator, model_validator, ValidationError, computed_field
)
from pydantic.alias_generators import to_camel

class GlobalConfig(BaseSettings):
    strict_mode: bool = False

    class Config:
        env_file = ".env"

settings = GlobalConfig() 

class Address(BaseModel):
    """Zagnieżdżony model adresu[cite: 9]."""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    
    street: str
    city: str
    zip_code: str = Field(pattern=r'^\d{5}$')  # 5-cyfrowy kod [cite: 9]

class User(BaseModel):
    """Model użytkownika z walidacją tożsamości[cite: 5, 6]."""
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        strict=settings.strict_mode
    )