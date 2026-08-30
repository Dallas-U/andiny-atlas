import { useEffect, useState } from "react";
import StatusBadge from "../../../shared/components/StatusBadge";

import { getCaseHistory } from "../api/investigation.api";
import type { CaseHistoryResponse } from "../types/investigation.types";
import { History } from "lucide-react";
import EmptyState from "../../../shared/components/EmptyState";

import {
    formatExactDate,
    formatRelativeDate,
} from "../../../shared/utils/date";

interface InvestigationHistoryProps {
    caseId: string;
}

function InvestigationHistory({
    caseId,
}: InvestigationHistoryProps) {
    const [history, setHistory] = useState<CaseHistoryResponse[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadHistory(): Promise<void> {
            try {
                const response = await getCaseHistory(caseId);

                setHistory(response);
            } catch (error) {
                console.error("Failed to load investigation history:", error);
                setErrorMessage("Unable to load investigation history.");
            } finally {
                setIsLoading(false);
            }
        }

        void loadHistory();
    }, [caseId]);

    if (isLoading) {
        return (
            <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-slate-400">
                    Loading investigation history...
                </p>
            </section>
        );
    }

    if (errorMessage) {
        return (
            <section className="mt-8 rounded-xl border border-red-900 bg-slate-900 p-6">
                <p className="text-red-400">{errorMessage}</p>
            </section>
        );
    }

    if (history.length === 0) {
        return (
            <div className="mt-8">
                <EmptyState
                    title="No history entries"
                    description="Audit entries will appear here after this investigation is updated."
                    icon={<History className="h-10 w-10" />}
                />
            </div>
        );
    }

    return (
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Investigation History
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Immutable audit entries recorded for this case.
                </p>
            </div>

            <div className="mt-6 space-y-4">
                {history.map((entry) => (
                    <article
                        key={entry.id}
                        className="rounded-lg border border-slate-800 bg-slate-950 p-5"
                    >
                        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                            <div>
                                <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
                                    Previous status
                                </p>

                                <div className="mt-2">
                                    <StatusBadge status={entry.status} />
                                </div>
                            </div>

                            <time
                                dateTime={entry.changed_at}
                                title={formatExactDate(entry.changed_at)}
                                className="text-sm text-slate-400"
                            >
                                {formatRelativeDate(entry.changed_at)}
                            </time>
                        </div>

                        <div className="mt-5 grid gap-5 sm:grid-cols-2">
                            <div>
                                <h3 className="text-sm font-medium text-slate-500">
                                    Reason
                                </h3>

                                <p className="mt-2 leading-7 text-slate-200">
                                    {entry.reason}
                                </p>
                            </div>

                            <div>
                                <h3 className="text-sm font-medium text-slate-500">
                                    Next action
                                </h3>

                                <p className="mt-2 leading-7 text-slate-200">
                                    {entry.next_action}
                                </p>
                            </div>
                        </div>

                        <div className="mt-5 border-t border-slate-800 pt-4">
                            <p className="text-sm text-slate-500">
                                Changed by
                            </p>

                            <p className="mt-1 break-all text-sm text-slate-300">
                                {entry.changed_by}
                            </p>
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
}

export default InvestigationHistory;