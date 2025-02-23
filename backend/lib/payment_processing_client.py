# lib/jawnt/client.py
import time
from unittest.mock import patch
import uuid
from random import randint

from pydantic import BaseModel

from backend.lib.models import Payment, PaymentStatus
from backend.lib.payment_processing import perform_ach_credit, perform_ach_debit

class PaymentResponse(BaseModel):
	"""
	Represents the response from an external payment service
	Amount is in cents
	"""
	payment_id: str
	status: PaymentStatus
	amount: int

def external_call(*args, amount) -> PaymentResponse: # pylint: disable=unused-argument
	time.sleep(2)

	return PaymentResponse(
		payment_id=str(uuid.uuid4()),
		status=PaymentStatus.PENDING,
		amount=amount,
	)

def long_external_call() -> None:
	time.sleep(30)

	def perform_ach_debit(internal_account_id: str, external_account_id: str, amount: int, idempotency_key: str,) -> PaymentResponse:
		"""
		Amount represents the amount in cents
		e.g $50.00 = 5000
		Technical Screening 7
		"""
		return external_call(
			internal_account_id,
			external_account_id,
			idempotency_key,
			amount=amount,
		)

	def perform_ach_credit(internal_account_id: str, external_account_id: str, amount: int, idempotency_key: str,) -> PaymentResponse:
		"""
		Amount represents the amount in cents
		e.g $50.00 = 5000
		"""
		return external_call(
			internal_account_id,
			external_account_id,
			idempotency_key,
			amount=amount,
		)

def perform_book_payment(internal_account_id: str, external_account_id: str, amount: int, idempotency_key: str,) -> PaymentResponse:
	"""
	Amount represents the amount in cents
	e.g $50.00 = 5000
	Technical Screening 8
	"""
	return external_call(
		internal_account_id,
		external_account_id,
		idempotency_key,
		amount=amount,
	)

def get_payment_status(payment_id: str):
	long_external_call()
	return PaymentStatus.SUCCESS if randint(1, 2) == 1 else Payment

@patch("jawnt.api.jawnt_client.external_call")
def test_perform_ach_debit(mock_external_call):
	mock_external_call.return_value = PaymentResponse(
		payment_id=str(uuid.uuid4()),
		status=PaymentStatus.PENDING,
		amount=5000,
	)

	response = perform_ach_debit(
		"internal_account_id",
		"external_account_id",
		5000,
		"idempotency_key",
	)

	assert response.status == PaymentStatus.PENDING

@patch("jawnt.api.jawnt_client.external_call")
def test_perform_ach_credit(mock_external_call):
	mock_external_call.return_value = PaymentResponse(
		payment_id=str(uuid.uuid4()),
		status=PaymentStatus.PENDING,
		amount=5000,
	)

	response = perform_ach_credit(
		"internal_account_id",
		"external_account_id",
		5000,
		"idempotency_key",
	)

	assert response.status == PaymentStatus.PENDING

@patch("jawnt.api.jawnt_client.external_call")
def test_perform_book_payment(mock_external_call):
	mock_external_call.return_value = PaymentResponse(
		payment_id=str(uuid.uuid4()),
		status=PaymentStatus.PENDING,
		amount=5000,
	)

	response = perform_book_payment(
		"internal_account_id",
		"external_account_id",
		5000,
		"idempotency_key",
	)

	assert response.status == PaymentStatus.PENDING
