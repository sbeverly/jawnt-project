from enum import Enum
from pydantic import BaseModel

class Account(BaseModel):
	account_id: str
	name: str

class InternalAccount(Account):
	pass

class ExternalAccount(Account):
	organization_id: str

class PaymentStatus(str, Enum):
	PENDING = "PENDING"
	SUCCESS = "SUCCESS"
	FAILURE = "FAILURE"

class Payment(BaseModel):
	internal_account_id: str
	external_account_id: str
	amount: str
	status: PaymentStatus = PaymentStatus.PENDING
