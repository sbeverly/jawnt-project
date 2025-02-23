from backend.lib.models import Payment


def perform_ach_debit(internal_account_id: str, external_account_id: str, amount: int, indepodency_key: str) -> Payment:
	pass

def perform_ach_credit(internal_account_id: str, external_account_id: str, amount: int, indepodency_key: str) -> Payment:
	pass
