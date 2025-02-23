export interface Account {
	record_id: string;
	account_id: string;
	name: string;
	organization_id: string;
}

export default function AccountView({ accounts }: { accounts: [Account] }) {
	return (
		<div>
			<select>
				{accounts.map((x) => {
					return (
						<option key={x.record_id}>
							{x.name} ({x.account_id}))
						</option>
					);
				})}
			</select>
		</div>
	);
}
