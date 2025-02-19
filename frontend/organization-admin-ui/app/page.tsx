import { LinkAccountLarge } from "@/components/LinkAccount";
import { redirect } from "next/navigation";

export default function Home() {
	// TODO: fetch accounts for user
	// let data = await fetch("/accounts/payments/list/{organization_id}")
	// let accounts = data.json()

	const accounts = [{}];

	if (accounts.length > 0) {
		return redirect("/accounts");
	}

	return (
		<div className="flex justify-center items-center h-screen">
			<LinkAccountLarge />
		</div>
	);
}
