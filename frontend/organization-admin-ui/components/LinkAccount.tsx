"use client";

import { useEffect, useState } from "react";

import { usePlaidLink } from "react-plaid-link";
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
	const [linkToken, setLinkToken] = useState<string | null>(null);

	useEffect(function () {
		async function fetchLinkToken() {
			const req = await fetch(
				"http://localhost:8000/api/plaid/create_link_token",
				{
					method: "POST",
				},
			);

			const data = await req.json();
			setLinkToken(data["link_token"]);
		}

		fetchLinkToken();
	}, []);

	const { open, ready } = usePlaidLink({
		token: linkToken || "",
		onSuccess: async (publicToken, metadata) => {
			console.log("Plaid Link success:", publicToken, metadata);
			const req = await fetch(`http://localhost:8000/accounts/external`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ publicToken }),
			});
			const data: { linkToken: string } = await req.json();
			setLinkToken(data.linkToken);
		},
		onExit: (error, metadata) => {
			console.log("Plaid Link exited:", error, metadata);
		},
		onEvent: (eventName, metadata) => {
			console.log("Plaid Link event:", eventName, metadata);
		},
	});

	return (
		<button
			onClick={() => open()}
			disabled={!ready}
			className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
		>
			Connect a bank account
		</button>
	);
}
