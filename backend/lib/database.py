from enum import Enum
from plaid.model_utils import uuid
from backend.lib.models import ExternalAccount, InternalAccount, Organization, Payment, PaymentStatus, PaymentType, Record

# class Record(BaseModel):
# 	record_id: str | None = None
# 	table_name: str | None = None
# 	data: InternalAccount | ExternalAccount | Payment

class Tables(str, Enum):
	EXTERNAL_ACCOUNT = "ExternalAccount"
	INTERNAL_ACCOUNT = "InternalAccount"
	PAYMENT = "Payment"
	ORGANIZATION = "Organization"

TEST_DB = data = {
    "ExternalAccount": {
        "82e0989e-bff9-4162-938f-9ebdfeb6243f": ExternalAccount(
            account_id="6rA6a8JXEVCMNgoMNjBkTnN6qdjo6ACkbyv7e",
            name="Plaid Checking",
            organization_id="tester-1",
            record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f"
        )
    },
    "InternalAccount": {
        "3440ea80-61c2-43cb-b6bd-494ad0bd36f6": InternalAccount(
            account_id="33243sdfa",
            name="Super Checking",
            record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6"
        )
    },
    "Organization": {
        "tester-1": Organization(
            name="Test Organization",
            record_id="tester-1"
        )
    },
    "Payment": {
        "375b0237-5e8e-4076-a2fa-4aede23467dc": Payment(
            amount=4534,
            external_account_record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f",
            internal_account_record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6",
            record_id="375b0237-5e8e-4076-a2fa-4aede23467dc",
            status=PaymentStatus.PENDING,
            type=PaymentType.DEBIT
        ),
        "3b9a4e9d-9f3e-4a89-bbc2-289bdf21c92e": Payment(
                amount=2500,
                external_account_record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f",
                internal_account_record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6",
                record_id="3b9a4e9d-9f3e-4a89-bbc2-289bdf21c92e",
                status=PaymentStatus.SUCCESS,
                type=PaymentType.CREDIT
        ),
        "2c36b6e8-5a7d-4f3a-a9f8-c04b65e69c4f": Payment(
            amount=3800,
            external_account_record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f",
            internal_account_record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6",
            record_id="2c36b6e8-5a7d-4f3a-a9f8-c04b65e69c4f",
            status=PaymentStatus.FAILURE,
            type=PaymentType.DEBIT
        ),
        "8f46d3b7-6429-4f95-9ecf-85e66df0e9a2": Payment(
            amount=4100,
            external_account_record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f",
            internal_account_record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6",
            record_id="8f46d3b7-6429-4f95-9ecf-85e66df0e9a2",
            status=PaymentStatus.PENDING,
            type=PaymentType.CREDIT
        ),
        "bb1cd4a3-f46e-468f-b39a-cccf2e76fc92": Payment(
            amount=5675,
            external_account_record_id="82e0989e-bff9-4162-938f-9ebdfeb6243f",
            internal_account_record_id="3440ea80-61c2-43cb-b6bd-494ad0bd36f6",
            record_id="bb1cd4a3-f46e-468f-b39a-cccf2e76fc92",
            status=PaymentStatus.SUCCESS,
            type=PaymentType.DEBIT
        ),
    }
}

class Database():
	# tables = {
	# 	Tables.EXTERNAL_ACCOUNT: {},
	# 	Tables.INTERNAL_ACCOUNT: {},
	# 	Tables.PAYMENT: {},
	# 	Tables.ORGANIZATION: {
	# 		'tester-1': {
	# 			"record_id": "tester-1",
	# 			"name": "Test Organization"
	# 		}
	# 	}
	# }

	tables = TEST_DB

	def set(self, record: Record) -> str:
		table_name = Tables(type(record).__name__)
		record.record_id = str(uuid.uuid4())

		self.tables[table_name][record.record_id] = record

		return record.record_id

	def delete(self, table_name: Tables, record_id: str):
		del self.tables[table_name][record_id]

	def get(self, table_name: Tables, record_id: str):
		record = self.tables[table_name].get(record_id)
		return record

	def get_by_condition(self, table_name, col, value):
		return [row for row in self.tables[table_name].values() if getattr(row, col) == value]

	def show(self, table_name: Tables | None = None):
		if table_name:
			return self.tables[table_name]

		return self.tables
