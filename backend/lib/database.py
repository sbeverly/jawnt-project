from enum import Enum
from plaid.model_utils import uuid
from pydantic.main import BaseModel
from backend.lib.models import ExternalAccount, InternalAccount, Payment

class Record(BaseModel):
	record_id: str | None = None
	table_name: str | None = None
	organization_id: str | None = None
	data: InternalAccount | ExternalAccount | Payment

class Tables(str, Enum):
	EXTERNAL_ACCOUNT = "ExternalAccount"
	INTERNAL_ACCOUNT = "InternalAccount"
	PAYMENT = "Payment"
	ORGANIZATION = "Organization"

class Database():
	tables = {
		Tables.EXTERNAL_ACCOUNT: {},
		Tables.INTERNAL_ACCOUNT: {},
		Tables.PAYMENT: {}
	}

	def set(self, record: Record) -> str:
		table_name = Tables(type(record.data).__name__)
		record_id = record.record_id

		if not record_id:
			record_id = str(uuid.uuid4())

		self.tables[table_name][record_id] = record.data

		return record_id

	def delete(self, table_name: Tables, record_id: str):
		del self.tables[table_name][record_id]

	def get(self, table_name: Tables, record_id: str) -> Record | None:
		data = self.tables[table_name].get(record_id)

		if not data:
			return

		return Record(record_id=record_id, table_name=table_name, data=data)

	def get_by_condition(self, table_name, col, value):
		return [row for row in self.tables[table_name].values() if getattr(row, col) == value]

	def show(self, table_name: Tables | None = None):
		if table_name:
			return self.tables[table_name]

		return self.tables
