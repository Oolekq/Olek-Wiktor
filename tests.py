import unittest
from datetime import datetime, date, timedelta
from decimal import Decimal
from pydantic import ValidationError

from main import (
    Currency, TransactionType, BankTransaction,
    Address, User, handle_validation_errors,
    PolicyStatus, InsurancePolicy
)

class TestModels(unittest.TestCase):

    def test_bank_transaction_valid(self):
        tx = BankTransaction(
            currency=Currency.USD,
            amount=Decimal('100.50'),
            timestamp=datetime.now(),
            transaction_type=TransactionType.DEBIT
        )
        self.assertEqual(tx.currency, Currency.USD)
        self.assertEqual(tx.amount, Decimal('100.50'))

    def test_bank_transaction_invalid_amount(self):
        with self.assertRaises(ValidationError):
            BankTransaction(
                currency=Currency.USD,
                amount=Decimal('-10.00'),
                timestamp=datetime.now(),
                transaction_type=TransactionType.DEBIT
            )

    def test_handle_validation_errors_formatting(self):
        try:

            Address(street="123 Main St", city="New York", zip_code="invalid-zip")
        except ValidationError as e:
            friendly_errors = handle_validation_errors(e)
            self.assertIsInstance(friendly_errors, list)
            self.assertGreater(len(friendly_errors), 0)
            self.assertIn("location", friendly_errors[0])
            self.assertIn("message", friendly_errors[0])
            self.assertEqual(friendly_errors[0]["location"], "zip_code")

    def test_address_valid(self):
        addr = Address(street="123 Main St", city="New York", zipCode="10001")
        self.assertEqual(addr.zip_code, "10001")

    def test_address_invalid_zip(self):
        with self.assertRaises(ValidationError):
            Address(street="123 Main St", city="New York", zip_code="1000")

    def test_user_valid(self):
        user = User(
            id="ACC-1234",
            email="test@example.com",
            age=25,
            address=Address(street="123 Main St", city="NY", zipCode="10001"),
            social_security_number="123-45-6789"
        )
        self.assertEqual(user.id, "ACC-1234")
        
        dumped = user.model_dump()
        self.assertNotIn("social_security_number", dumped)

    def test_user_invalid_age(self):
        with self.assertRaises(ValidationError):
            User(
                id="ACC-1234",
                email="test@example.com",
                age=17,
                address=Address(street="123 Main St", city="NY", zip_code="10001"),
                socialSecurityNumber="123-45-6789"
            )

    def test_insurance_policy_valid(self):
        policy = InsurancePolicy(
            policy_number="ABCDEFGHIJ",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=35),
            status=PolicyStatus.ACTIVE
        )
        self.assertEqual(policy.policy_number, "ABCDEFGHIJ")

    def test_insurance_policy_invalid_number_lower(self):
        with self.assertRaises(ValidationError):
            InsurancePolicy(
                policy_number="abcdefghij",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=35),
                status=PolicyStatus.ACTIVE
            )

    def test_insurance_policy_invalid_date_range(self):
        with self.assertRaises(ValidationError):
            InsurancePolicy(
                policy_number="ABCDEFGHIJ",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=10),
                status=PolicyStatus.ACTIVE
            )
if __name__ == '__main__':
    unittest.main()
