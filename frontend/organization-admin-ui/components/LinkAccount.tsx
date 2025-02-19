export function LinkAccountLarge() {
	return (
		<div className="flex flex-col w-1/4 gap-5">
			<div className="text-lg">
				Jawnt uses Plaid to connect to your organization&apos;s bank account to
				automatically fund your members&apos; passes each month
			</div>

			<PlaidLink />
		</div>
	);
}

export default function LinkAccount() {
	return <PlaidLink />;
}

function PlaidLink() {
	return (
		<button className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
			Add Account
		</button>
	);
}
