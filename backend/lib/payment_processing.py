from uuid import UUID
import uuid
from backend.lib.database import Tables
from backend.lib.models import Payment, PaymentType
from backend.lib.payment_processing_client import PaymentResponse
from backend.api.routes import db
from backend.lib.payment_processing import perform_ach_debit

# NOTE: This is mostly pseudocode
def process_payment(item: Payment) -> PaymentResponse:
	internal_account_id = db.get(Tables.INTERNAL_ACCOUNT, item.internal_account_record_id).account_id
	external_account_id = db.get(Tables.EXTERNAL_ACCOUNT, item.internal_account_record_id).account_id

	if item.type == PaymentType.DEBIT:
		return perform_ach_debit(internal_account_id, external_account_id, item.amount, uuid.uuid4())
	if item.type == PaymentType.CREDIT:
		return perform_ach_credit(internal_account_id, external_account_id, item.amount, )
