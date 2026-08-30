import BackButton from "../shared/components/BackButton";

import MyInvestigations from "../features/investigation/components/MyInvestigations";

function InvestigationsPage() {
    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">

                <div className="mb-6">
                    <BackButton />
                </div>

                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white">
                        My Investigations
                    </h1>

                    <p className="mt-2 text-slate-400">
                        Review investigation cases created by your account.
                    </p>
                </div>

                <MyInvestigations />

            </div>
        </main>
    );
}

export default InvestigationsPage;