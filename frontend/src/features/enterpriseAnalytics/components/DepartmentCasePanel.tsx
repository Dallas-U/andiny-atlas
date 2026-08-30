import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { FolderSearch2 } from "lucide-react";

import StatusBadge from "../../../shared/components/StatusBadge";
import EmptyState from "../../../shared/components/EmptyState";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";

import { getCases } from "../../investigation/api/investigation.api";

import type { CaseResponse } from "../../investigation/types/investigation.types";

interface DepartmentCasePanelProps {
    departmentId: string | null;
    departmentName: string | null;
}

function DepartmentCasePanel({
    departmentId,
    departmentName,
}: DepartmentCasePanelProps) {
    const navigate = useNavigate();

    const [
        cases,
        setCases,
    ] = useState<CaseResponse[]>([]);

    const [
        isLoading,
        setIsLoading,
    ] = useState(false);

    const [
        errorMessage,
        setErrorMessage,
    ] = useState<string | null>(null);

    useEffect(() => {
        if (!departmentId) {
            setCases([]);
            setErrorMessage(null);
            setIsLoading(false);
            return;
        }

        const selectedDepartmentId: string =
            departmentId;

        async function loadDepartmentCases(): Promise<void> {
            try {
                setIsLoading(true);
                setErrorMessage(null);

                const response = await getCases({
                    department_id:
                        selectedDepartmentId,
                });

                setCases(response.items);
            } catch (error) {
                console.error(
                    "Failed to load department cases:",
                    error,
                );

                setCases([]);

                setErrorMessage(
                    "Unable to load cases for this department.",
                );
            } finally {
                setIsLoading(false);
            }
        }

        void loadDepartmentCases();
    }, [departmentId]);

    function openCase(caseId: string): void {
        void navigate({
            to: "/dashboard/investigations/$caseId",
            params: {
                caseId,
            },
        });
    }

    if (!departmentId) {
        return (
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <div className="flex items-center gap-3">
                    <FolderSearch2 className="h-5 w-5 text-slate-500" />

                    <div>
                        <h2 className="text-lg font-semibold text-white">
                            Department Cases
                        </h2>

                        <p className="mt-1 text-sm text-slate-400">
                            Select a department to view its investigation cases.
                        </p>
                    </div>
                </div>
            </section>
        );
    }

    return (
        <section className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
            <div className="border-b border-slate-800 px-6 py-5">
                <h2 className="text-lg font-semibold text-white">
                    Department Cases
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Investigation cases belonging to{" "}
                    <span className="font-medium text-slate-300">
                        {departmentName ??
                            "the selected department"}
                    </span>
                    .
                </p>
            </div>

            {isLoading && (
                <div className="p-6">
                    <LoadingSkeleton className="h-32 w-full" />
                </div>
            )}

            {!isLoading && errorMessage && (
                <div className="p-6">
                    <p className="text-sm text-red-400">
                        {errorMessage}
                    </p>
                </div>
            )}

            {!isLoading &&
                !errorMessage &&
                cases.length === 0 && (
                    <div className="p-6">
                        <EmptyState
                            title="No cases found"
                            description="There are currently no investigation cases recorded for this department."
                            icon={
                                <FolderSearch2 className="h-10 w-10" />
                            }
                        />
                    </div>
                )}

            {!isLoading &&
                !errorMessage &&
                cases.length > 0 && (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-slate-800">
                            <thead className="bg-slate-950/50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                        Customer
                                    </th>

                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                        Phone Number
                                    </th>

                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                        Status
                                    </th>

                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                        Created By
                                    </th>

                                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                        Case ID
                                    </th>
                                </tr>
                            </thead>

                            <tbody className="divide-y divide-slate-800">
                                {cases.map(
                                    (investigation) => (
                                        <tr
                                            key={
                                                investigation.case_id
                                            }
                                            onClick={() =>
                                                openCase(
                                                    investigation.case_id,
                                                )
                                            }
                                            onKeyDown={(
                                                event,
                                            ) => {
                                                if (
                                                    event.key ===
                                                    "Enter" ||
                                                    event.key ===
                                                    " "
                                                ) {
                                                    event.preventDefault();

                                                    openCase(
                                                        investigation.case_id,
                                                    );
                                                }
                                            }}
                                            tabIndex={0}
                                            role="link"
                                            className="cursor-pointer transition hover:bg-slate-800/60 focus:bg-slate-800/60 focus:outline-none"
                                        >
                                            <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-white">
                                                {
                                                    investigation.customer_name
                                                }
                                            </td>

                                            <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300">
                                                {
                                                    investigation.phone_number
                                                }
                                            </td>

                                            <td className="whitespace-nowrap px-6 py-4">
                                                <StatusBadge
                                                    status={
                                                        investigation
                                                            .result
                                                            .status
                                                    }
                                                />
                                            </td>

                                            <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-300">
                                                {
                                                    investigation.created_by
                                                }
                                            </td>

                                            <td className="max-w-xs truncate px-6 py-4 text-sm text-slate-400">
                                                {
                                                    investigation.case_id
                                                }
                                            </td>
                                        </tr>
                                    ),
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
        </section>
    );
}

export default DepartmentCasePanel;