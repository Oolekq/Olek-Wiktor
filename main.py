from pydantic_settings import BaseSettings, BaseModel, Field, ConfigDict
from decimal import Decimal
from enum import Enum
from datetime import datetime
from pydantic.aliases_generation import to_camel

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