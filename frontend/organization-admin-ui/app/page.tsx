"use client";

import AccountView, { Account } from "@/components/AccountView";
import { LinkAccountLarge } from "@/components/LinkAccount";
import { useEffect, useState } from "react";

export default function Home() {
	const [accounts, setAccounts] = useState<Account[]>();

	const getAccounts = async () => {
		const data = await fetch(
			"http://localhost:8000/accounts/external/tester-1",
		);
		const response = await data.json();
		setAccounts(response);
	};

	useEffect(() => {
		getAccounts();
	}, []);

	if (!accounts) {
		return <div>loading</div>;
	}

	if (accounts && accounts.length) {
		return <AccountView />;
	}

	return (
		<div className="flex justify-center items-center h-screen">
			<LinkAccountLarge onComplete={getAccounts} />
		</div>
	);
}
