from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, ConfigDict, EmailStr, ValidationError
from decimal import Decimal
from enum import Enum
from datetime import datetime
from typing import List, Dict
from pydantic.alias_generators import to_camel


class GlobalConfig(BaseSettings):
    strict_mode: bool = False

    class Config:
        env_file = ".env"

settings = GlobalConfig() 

class Currency(str, Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'

class TransactionType(str, Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'

class BankTransaction(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        strict=settings.strict_mode,
        coerce_numbers_to_str=False
    )

    currency: Currency
    amount: Decimal = Field(gt=0)
    timestamp: datetime
    transaction_type: TransactionType

class Address(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    
    street: str
    city: str
    zip_code: str = Field(pattern=r'^\d{5}$')

class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        strict=settings.strict_mode
    )

    id: str = Field(pattern=r'^[a-fA-F0-9\-]{36}$|^ACC-\d{4}$')
    email: EmailStr
    age: int = Field(ge=18, le=120)
    address: Address
    social_security_number: str = Field(exclude=True)

def handle_validation_errors(e: ValidationError) -> List[Dict[str, str]]:
    """Konwertuje błędy Pydantic na czytelny raport[cite: 33, 34, 50]."""
    friendly_errors = []
    for error in e.errors():
        loc = " -> ".join([str(x) for x in error['loc']])
        msg = error['msg']
        
        # Niestandardowe wiadomości dla Enum [cite: 35]
        if error['type'] == 'enum':
            allowed = ", ".join([str(v) for v in error['ctx']['expected']])
            msg = f"Please select a valid option: {allowed}"
            
        friendly_errors.append({"location": loc, "message": msg})
    return friendly_errors