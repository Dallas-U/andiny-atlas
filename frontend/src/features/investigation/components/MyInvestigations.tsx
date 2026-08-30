import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import StatusBadge from "../../../shared/components/StatusBadge";

import { getMyCases } from "../api/investigation.api";
import { FolderSearch2 } from "lucide-react";
import EmptyState from "../../../shared/components/EmptyState";
import {
    formatExactDate,
    formatRelativeDate,
} from "../../../shared/utils/date";
import type {
    CaseResponse,
    PaginationMetadata,
} from "../types/investigation.types";

function MyInvestigations() {
    const navigate = useNavigate();

    const [cases, setCases] = useState<CaseResponse[]>([]);
    const [metadata, setMetadata] =
        useState<PaginationMetadata | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        async function loadCases(): Promise<void> {
            try {
                const response = await getMyCases();

                setCases(response.items);
                setMetadata(response.metadata);
            } catch (error) {
                console.error("Failed to load investigations:", error);
                setErrorMessage("Unable to load your investigations.");
            } finally {
                setIsLoading(false);
            }
        }

        void loadCases();
    }, []);

    function openInvestigation(caseId: string): void {
        void navigate({
            to: "/dashboard/investigations/$caseId",
            params: {
                caseId,
            },
        });
    }

    if (isLoading) {
        return (
            <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-slate-400">
                    Loading your investigations...
                </p>
            </section>
        );
    }

    if (errorMessage) {
        return (
            <section className="rounded-xl border border-red-900 bg-slate-900 p-6">
                <p className="text-red-400">{errorMessage}</p>
            </section>
        );
    }

    if (cases.length === 0) {
        return (
            <EmptyState
                title="No investigations found"
                description="Investigations you create will appear here."
                icon={<FolderSearch2 className="h-10 w-10" />}
            />
        );
    }

    return (
        <section className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            <div className="flex items-center justify-between border-b border-slate-800 px-6 py-4">
                <div>
                    <h2 className="text-lg font-semibold text-white">
                        My investigations
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        Cases created by your account.
                    </p>
                </div>

                <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-medium text-slate-300">
                    {metadata?.total_records ?? cases.length} records
                </span>
            </div>

            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-800">
                    <thead className="bg-slate-950/50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Customer
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Phone number
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Status
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Created
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Case ID
                            </th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-800">
                        {cases.map((investigation) => (
                            <tr
                                key={investigation.case_id}
                                onClick={() => {
                                    openInvestigation(investigation.case_id);
                                }}
                                onKeyDown={(event) => {
                                    if (event.key === "Enter" || event.key === " ") {
                                        event.preventDefault();
                                        openInvestigation(investigation.case_id);
                                    }
                                }}
                                tabIndex={0}
                                role="link"
                                className="cursor-pointer transition hover:bg-slate-800/60 focus:bg-slate-800/60 focus:outline-none"
                            >
                                <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-white">
                                    {investigation.customer_name}
                                </td>

                                <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300">
                                    {investigation.phone_number}
                                </td>

                                <td className="whitespace-nowrap px-6 py-4">
                                    <StatusBadge status={investigation.result.status} />
                                </td>

                                <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300">
                                    <time
                                        dateTime={investigation.timestamp}
                                        title={formatExactDate(investigation.timestamp)}
                                    >
                                        {formatRelativeDate(investigation.timestamp)}
                                    </time>
                                </td>

                                <td className="max-w-xs truncate px-6 py-4 text-sm text-slate-400">
                                    {investigation.case_id}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </section>
    );
}

export default MyInvestigations;