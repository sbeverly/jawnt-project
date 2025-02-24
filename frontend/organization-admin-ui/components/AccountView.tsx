import { useState, useEffect } from "react";
import LinkAccount from "./LinkAccount";

export interface Account {
	record_id: string;
	account_id: string;
	name: string;
	organization_id: string;
}

export interface Payment {
	record_id: string;
	type: string;
	amount: string;
}

export default function AccountView() {
	const [accounts, setAccounts] = useState<Account[]>([]);
	const [selectedAccount, setSelectedAccount] = useState<string | null>(null);
	const [accountData, setAccountData] = useState<Payment[]>([]);

	const getAccounts = async () => {
		const data = await fetch(
			"http://localhost:8000/accounts/external/tester-1",
		);
		const response = await data.json();
		setAccounts(response);
		if (response.length == 1) {
			setSelectedAccount(response[0].record_id);
			fetchAccountData();
		}
	};

	const fetchAccountData = async () => {
		const data = await fetch(
			`http://localhost:8000/payments/account/${selectedAccount}`,
		);
		const payments = await data.json();
		setAccountData(payments);
	};

	useEffect(() => {
		getAccounts();
	}, []);

	useEffect(() => {
		if (!selectedAccount) return;

		fetchAccountData();
	}, [selectedAccount]);

	return (
		<div className="flex flex-col gap-10">
			<div className="flex flex-row gap-5 items-center bg-gray-800 p-4 rounded-lg shadow-md">
				<div className="max-w-fit">
					<LinkAccount onComplete={getAccounts} />
				</div>
				<div>
					<select
						className="bg-gray-900 text-gray-300 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
						value={selectedAccount ?? ""}
						onChange={(e) => {
							setSelectedAccount(e.target.value);
						}}
					>
						<option value="" disabled>
							Select an account
						</option>
						{accounts.map((x) => (
							<option key={x.record_id} value={x.record_id}>
								{x.name} ({x.record_id})
							</option>
						))}
					</select>
				</div>
			</div>

			{selectedAccount && accountData.length > 0 && (
				<table className="w-full border border-gray-700 rounded-lg shadow-sm bg-gray-900 text-gray-200">
					<thead>
						<tr className="bg-gray-800 text-gray-300 uppercase text-sm font-semibold">
							<th className="px-4 py-3 text-left">Type</th>
							<th className="px-4 py-3 text-left">Amount</th>
						</tr>
					</thead>
					<tbody>
						{accountData.map((item) => (
							<tr
								key={item.record_id}
								className="border-b border-gray-700 last:border-none hover:bg-gray-800"
							>
								<td className="px-4 py-3 text-gray-300">{item.type}</td>
								<td className="px-4 py-3 text-gray-300">{item.amount}</td>
							</tr>
						))}
					</tbody>
				</table>
			)}
		</div>
	);
}
