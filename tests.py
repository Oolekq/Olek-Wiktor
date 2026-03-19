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