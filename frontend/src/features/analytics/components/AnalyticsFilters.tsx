import { useState } from "react";

import type { InvestigationAnalyticsQuery } from "../api/analytics.api";

interface AnalyticsFiltersProps {
    onApply: (
        filters: InvestigationAnalyticsQuery,
    ) => void;
    isLoading?: boolean;
}

function today(): string {
    return new Date()
        .toISOString()
        .split("T")[0];
}

function thirtyDaysAgo(): string {
    const date = new Date();

    date.setDate(
        date.getDate() - 30,
    );

    return date
        .toISOString()
        .split("T")[0];
}

function AnalyticsFilters({
    onApply,
    isLoading = false,
}: AnalyticsFiltersProps) {
    const [filters, setFilters] =
        useState<InvestigationAnalyticsQuery>({
            start_date: thirtyDaysAgo(),
            end_date: today(),
            interval: "day",
        });

    function updateField(
        field: keyof InvestigationAnalyticsQuery,
        value: string,
    ): void {
        setFilters((current) => ({
            ...current,
            [field]: value,
        }));
    }

    function handleSubmit(
        event: React.FormEvent<HTMLFormElement>,
    ): void {
        event.preventDefault();
        onApply(filters);
    }

    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div>
                <h2 className="text-lg font-semibold text-white">
                    Analytics Filters
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Select the period and grouping interval
                    for investigation analytics.
                </p>
            </div>

            <form
                onSubmit={handleSubmit}
                className="mt-6 grid gap-5 md:grid-cols-4"
            >
                <div>
                    <label
                        htmlFor="analytics_start_date"
                        className="mb-2 block text-sm text-slate-400"
                    >
                        Start Date
                    </label>

                    <input
                        id="analytics_start_date"
                        type="date"
                        required
                        value={filters.start_date}
                        onChange={(event) => {
                            updateField(
                                "start_date",
                                event.target.value,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    />
                </div>

                <div>
                    <label
                        htmlFor="analytics_end_date"
                        className="mb-2 block text-sm text-slate-400"
                    >
                        End Date
                    </label>

                    <input
                        id="analytics_end_date"
                        type="date"
                        required
                        value={filters.end_date}
                        onChange={(event) => {
                            updateField(
                                "end_date",
                                event.target.value,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    />
                </div>

                <div>
                    <label
                        htmlFor="analytics_interval"
                        className="mb-2 block text-sm text-slate-400"
                    >
                        Interval
                    </label>

                    <select
                        id="analytics_interval"
                        value={filters.interval}
                        onChange={(event) => {
                            updateField(
                                "interval",
                                event.target.value,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    >
                        <option value="day">Daily</option>
                        <option value="week">Weekly</option>
                        <option value="month">Monthly</option>
                    </select>
                </div>

                <div className="flex items-end">
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {isLoading
                            ? "Loading analytics..."
                            : "Apply Filters"}
                    </button>
                </div>
            </form>
        </section>
    );
}

export default AnalyticsFilters;