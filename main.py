from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, ConfigDict, EmailStr, ValidationError, field_validator, model_validator
from decimal import Decimal
from enum import Enum
from datetime import datetime, date, timedelta
from typing import List, Dict
from pydantic.alias_generators import to_camel


class GlobalConfig(BaseSettings):
    strict_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env")

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

class PolicyStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    ELAPSED = 'ELAPSED'
    PENDING = 'PENDING'

class InsurancePolicy(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    policy_number: str = Field(min_length=10, max_length=10)
    start_date: date
    end_date: date
    status: PolicyStatus

    @field_validator('policy_number')
    @classmethod
    def must_be_upper(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError("Policy number must be strictly uppercase")
        return v

    @model_validator(mode='after')
    def validate_date_range(self) -> 'InsurancePolicy':
        if self.end_date < self.start_date + timedelta(days=30):
            raise ValueError("End date must be at least 30 days after start_date")
        return self

    class Account(BaseModel):
        model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

        user: User
        transactions: List[BankTransaction]

        @property
        def total_portfolio_value(self):
            return sum(t.amount for t in self.transactions)

        @computed_field
        @property
        def risk_score(self) -> str:
            total = self.total_portfolio_value
            age = self.user.age

            if total > 50000 and age > 60:
                return "Low"
            elif total > 10000 and age < 25:
                return "High"
            return "Medium"
