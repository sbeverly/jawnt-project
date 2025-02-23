from typing import List
import plaid
from plaid.api import plaid_api

from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products

from backend.lib.models import ExternalAccount

def get_plaid_client() -> plaid_api.PlaidApi:
	configuration = plaid.Configuration(
	    host=plaid.Environment.Sandbox,
	    api_key={
	        'clientId': '6758563294bbe4001b5c5279',
	        'secret': '386a94d4b632d57fe91b7b0f8506b3',
	    }
	)

	api_client = plaid.ApiClient(configuration)
	client = plaid_api.PlaidApi(api_client)

	return client

def get_link_token(client: plaid_api.PlaidApi, public_token: str) -> str:
	exchange_request = ItemPublicTokenExchangeRequest(
	    public_token=public_token
	)
	exchange_response = client.item_public_token_exchange(exchange_request)
	access_token = exchange_response['access_token']
	return access_token

def create_link_token(client: plaid_api.PlaidApi) -> str:
	req = LinkTokenCreateRequest(
  		user=LinkTokenCreateRequestUser(
		    client_user_id='user-abc',
		    email_address='user@example.com'
    	),
     products=[Products('transfer')],
		  client_name='Jawnt Test App',
		  language='en',
		  country_codes=[CountryCode('US')],
		)

	res = client.link_token_create(link_token_create_request=req)
	return res['link_token']

def exchange_public_token(client: plaid_api.PlaidApi, public_token: str) -> str:
	exchange_request = ItemPublicTokenExchangeRequest(
    	public_token=public_token
	)
	exchange_response = client.item_public_token_exchange(exchange_request)
	access_token = exchange_response['access_token']

	return access_token

def get_linked_accounts(client: plaid_api.PlaidApi, public_token: str):
	access_token = exchange_public_token(client, public_token)
	req = AccountsGetRequest(access_token=access_token)
	accounts = client.accounts_get(req)
	return accounts['accounts']

def extract_accounts(get_accounts_response, organization_id: str) -> List[ExternalAccount]:
	accounts = []

	for acc in get_accounts_response:
		acc = ExternalAccount(
			account_id = acc["account_id"],
			name = acc["name"],
			organization_id=organization_id
		)

		accounts.append(acc)
	return accounts
