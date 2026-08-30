import { useState } from "react";

import type { InvestigationStatus } from "../../investigation/types/investigation.types";
import type { ReportFilterFormData } from "../schema/report.schema";

interface ReportFiltersProps {
    onGenerate: (filters: ReportFilterFormData) => void;
    isLoading?: boolean;
}

const statusOptions: InvestigationStatus[] = [
    "Resolved",
    "Waiting",
    "Technical Investigation",
    "Escalated",
];

function today(): string {
    return new Date().toISOString().split("T")[0];
}

function sevenDaysAgo(): string {
    const date = new Date();

    date.setDate(date.getDate() - 7);

    return date.toISOString().split("T")[0];
}

function ReportFilters({
    onGenerate,
    isLoading = false,
}: ReportFiltersProps) {
    const [filters, setFilters] =
        useState<ReportFilterFormData>({
            start_date: sevenDaysAgo(),
            end_date: today(),
            status: undefined,
        });

    function updateField(
        field: keyof ReportFilterFormData,
        value: string,
    ) {
        setFilters((current) => ({
            ...current,
            [field]:
                value === ""
                    ? undefined
                    : value,
        }));
    }

    function handleSubmit(
        event: React.FormEvent<HTMLFormElement>,
    ) {
        event.preventDefault();

        onGenerate(filters);
    }

    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div>
                <h2 className="text-lg font-semibold text-white">
                    Report Filters
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Select a reporting period and optional
                    investigation status.
                </p>
            </div>

            <form
                onSubmit={handleSubmit}
                className="mt-6 grid gap-5 md:grid-cols-4"
            >
                <div>
                    <label className="mb-2 block text-sm text-slate-400">
                        Start Date
                    </label>

                    <input
                        type="date"
                        value={filters.start_date}
                        onChange={(event) =>
                            updateField(
                                "start_date",
                                event.target.value,
                            )
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                    />
                </div>

                <div>
                    <label className="mb-2 block text-sm text-slate-400">
                        End Date
                    </label>

                    <input
                        type="date"
                        value={filters.end_date}
                        onChange={(event) =>
                            updateField(
                                "end_date",
                                event.target.value,
                            )
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                    />
                </div>

                <div>
                    <label className="mb-2 block text-sm text-slate-400">
                        Status
                    </label>

                    <select
                        value={filters.status ?? ""}
                        onChange={(event) =>
                            updateField(
                                "status",
                                event.target.value,
                            )
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                    >
                        <option value="">
                            All statuses
                        </option>

                        {statusOptions.map((status) => (
                            <option
                                key={status}
                                value={status}
                            >
                                {status}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="flex items-end">
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white transition hover:bg-indigo-500 disabled:opacity-50"
                    >
                        {isLoading
                            ? "Generating..."
                            : "Generate Report"}
                    </button>
                </div>
            </form>
        </section>
    );
}

export default ReportFilters;