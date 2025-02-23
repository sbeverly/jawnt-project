from fastapi import FastAPI, HTTPException

from backend.lib.database import Database, Tables
from backend.lib.models import InternalAccount, Payment, PaymentStatus
from backend.lib.plaid import extract_accounts, get_linked_accounts, get_plaid_client, create_link_token
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
db = Database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateExternalAccountRequest(BaseModel):
	public_token: str | None

# For expediency, this route will simply persist the account details
# passed by the internal superuser.
class CreateInternalAccountRequest(BaseModel):
	account: InternalAccount

class CreatePaymentRequest(BaseModel):
	payment: Payment

@app.post("/api/plaid/create_link_token")
def create_token():
	client = get_plaid_client()
	response = create_link_token(client)

	return {
		"link_token": response
	}

@app.post("/accounts/external/{organization_id}")
async def create_external_account(organization_id: str, payload: CreateExternalAccountRequest):
	if not payload.public_token:
		raise HTTPException(status_code=400,)

	client = get_plaid_client()
	accounts = get_linked_accounts(client, payload.public_token)

	external_accounts = extract_accounts(accounts, organization_id)

	inserted = []
	for a in external_accounts:
		record = a
		inserted.append(db.set(record))
	if len(inserted) == 1:
		return inserted[0]

	return inserted

@app.post("/accounts/internal")
async def create_internal_account(payload: CreateInternalAccountRequest):
	return db.set(payload.account)

@app.delete("/accounts/internal/{record_id}")
def delete_internal_account(record_id):
	return db.delete(Tables.INTERNAL_ACCOUNT, record_id)

@app.put("/accounts/internal/{record_id}")
def update_internal_account(record_id, payload: CreateInternalAccountRequest):
	if not db.get(Tables.INTERNAL_ACCOUNT, record_id):
		raise HTTPException(status_code=404)
	return db.set(payload.account)

@app.get("/accounts/internal/{record_id}")
def get_internal_account(record_id):
	record = db.get(Tables.INTERNAL_ACCOUNT, record_id)
	if not record:
		raise HTTPException(status_code=404)
	return record

@app.post("/payment/debit")
def create_ach_debit(payload: CreatePaymentRequest):
	payment = payload.payment
	payment.status = PaymentStatus.PENDING

	return db.set(payment)

@app.post("/payment/credit")
def create_ach_credit(payload: CreatePaymentRequest):
	payment = payload.payment
	payment.status = PaymentStatus.PENDING

	return db.set(payment)

@app.get("/accounts/external/{organization_id}")
def get_account_list(organization_id: str):
	return db.get_by_condition(Tables.EXTERNAL_ACCOUNT, col="organization_id", value=organization_id)

@app.get("/payments/account/{account_record_id}")
def get_payments_list(account_record_id: str):
	return db.show(Tables.PAYMENT)
	return db.get_by_condition(Tables.PAYMENT, col="external_account_record_id", value=account_record_id)
