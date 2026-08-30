import BackButton from "../shared/components/BackButton";
import NewInvestigationForm from "../features/investigation/components/NewInvestigationForm";

function NewInvestigationPage() {
    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-3xl">

                <div className="mb-6">
                    <BackButton />
                </div>

                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white">
                        New Investigation
                    </h1>

                    <p className="mt-2 text-slate-400">
                        Create a new customer support investigation.
                    </p>
                </div>

                <NewInvestigationForm />

            </div>
        </main>
    );
}

export default NewInvestigationPage;