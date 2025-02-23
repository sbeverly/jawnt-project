from enum import Enum
from pydantic import BaseModel

class Record(BaseModel):
	record_id: str | None = None

class Account(Record):
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

class PaymentType(Enum):
	DEBIT = "debit"
	CREDIT = "credit"

class Payment(Record):
	internal_account_record_id: str
	external_account_record_id: str
	amount: int
	status: PaymentStatus = PaymentStatus.PENDING
	type: PaymentType

class Organization(Record):
	name: str
