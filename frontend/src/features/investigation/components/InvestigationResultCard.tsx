import { CheckCircle2 } from "lucide-react";
import { useNavigate } from "@tanstack/react-router";

import type { CaseResponse } from "../types/investigation.types";

interface InvestigationResultCardProps {
    investigation: CaseResponse;
    onStartAnother: () => void;
}

function InvestigationResultCard({
    investigation,
    onStartAnother,
}: InvestigationResultCardProps) {
    const navigate = useNavigate();

    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-green-900/40">
                    <CheckCircle2 className="h-6 w-6 text-green-300" />
                </div>

                <div>
                    <p className="text-sm font-medium uppercase tracking-wide text-green-300">
                        Investigation complete
                    </p>

                    <h2 className="mt-1 text-2xl font-semibold text-white">
                        {investigation.result.status}
                    </h2>

                    <p className="mt-2 text-slate-400">
                        The support case was investigated and recorded successfully.
                    </p>
                </div>
            </div>

            <dl className="mt-8 grid gap-5 sm:grid-cols-2">
                <div>
                    <dt className="text-sm text-slate-500">Case ID</dt>
                    <dd className="mt-1 break-all text-slate-200">
                        {investigation.case_id}
                    </dd>
                </div>

                <div>
                    <dt className="text-sm text-slate-500">Date and time</dt>
                    <dd className="mt-1 text-slate-200">
                        {new Date(investigation.timestamp).toLocaleString()}
                    </dd>
                </div>

                <div>
                    <dt className="text-sm text-slate-500">Customer</dt>
                    <dd className="mt-1 text-slate-200">
                        {investigation.customer_name}
                    </dd>
                </div>

                <div>
                    <dt className="text-sm text-slate-500">Phone number</dt>
                    <dd className="mt-1 text-slate-200">
                        {investigation.phone_number}
                    </dd>
                </div>
            </dl>

            <div className="mt-8 space-y-5 border-t border-slate-800 pt-6">
                <div>
                    <h3 className="text-sm font-medium text-slate-500">
                        Reason
                    </h3>

                    <p className="mt-2 leading-7 text-slate-200">
                        {investigation.result.reason}
                    </p>
                </div>

                <div>
                    <h3 className="text-sm font-medium text-slate-500">
                        Next action
                    </h3>

                    <p className="mt-2 leading-7 text-slate-200">
                        {investigation.result.next_action}
                    </p>
                </div>
            </div>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <button
                    type="button"
                    onClick={onStartAnother}
                    className="rounded-lg bg-white px-4 py-3 font-semibold text-slate-950 transition hover:bg-slate-200"
                >
                    Start another investigation
                </button>

                <button
                    type="button"
                    onClick={() => {
                        void navigate({
                            to: "/dashboard",
                            replace: true,
                        });
                    }}
                    className="rounded-lg border border-slate-700 px-4 py-3 font-semibold text-slate-200 transition hover:border-slate-500 hover:bg-slate-800"
                >
                    Back to dashboard
                </button>
            </div>
        </section>
    );
}

export default InvestigationResultCard;