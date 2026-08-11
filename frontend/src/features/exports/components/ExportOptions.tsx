import Card from "../../../shared/components/Card";

import type {
    InvestigationStatus,
} from "../../investigation/types/investigation.types";

import type {
    ExportFormat,
    ExportSource,
} from "../types/export.types";

type AnalyticsInterval =
    | "day"
    | "week"
    | "month";

interface ExportOptionsProps {
    source: ExportSource;
    format: ExportFormat;
    startDate: string;
    endDate: string;
    status: InvestigationStatus | "";
    interval: AnalyticsInterval;
    isLoading: boolean;

    onSourceChange: (
        source: ExportSource,
    ) => void;

    onFormatChange: (
        format: ExportFormat,
    ) => void;

    onStartDateChange: (
        value: string,
    ) => void;

    onEndDateChange: (
        value: string,
    ) => void;

    onStatusChange: (
        value: InvestigationStatus | "",
    ) => void;

    onIntervalChange: (
        value: AnalyticsInterval,
    ) => void;

    onGeneratePreview: () => void;
}

function ExportOptions({
    source,
    format,
    startDate,
    endDate,
    status,
    interval,
    isLoading,
    onSourceChange,
    onFormatChange,
    onStartDateChange,
    onEndDateChange,
    onStatusChange,
    onIntervalChange,
    onGeneratePreview,
}: ExportOptionsProps) {
    return (
        <Card>
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Export Options
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Select the information you want to export,
                    configure the period, and choose an export
                    format.
                </p>
            </div>

            <div className="mt-6 grid gap-5 md:grid-cols-2">
                <div>
                    <label
                        htmlFor="export_source"
                        className="mb-2 block text-sm font-medium text-slate-300"
                    >
                        Export source
                    </label>

                    <select
                        id="export_source"
                        value={source}
                        onChange={(event) => {
                            onSourceChange(
                                event.target.value as ExportSource,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    >
                        <option value="reports">
                            Investigation Reports
                        </option>

                        <option value="analytics">
                            Investigation Analytics
                        </option>
                    </select>
                </div>

                <div>
                    <label
                        htmlFor="export_format"
                        className="mb-2 block text-sm font-medium text-slate-300"
                    >
                        Export format
                    </label>

                    <select
                        id="export_format"
                        value={format}
                        onChange={(event) => {
                            onFormatChange(
                                event.target.value as ExportFormat,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    >
                        <option value="csv">
                            CSV
                        </option>

                        <option value="excel">
                            Excel (.xlsx)
                        </option>

                        <option value="pdf">
                            PDF
                        </option>
                    </select>
                </div>
            </div>

            <div className="mt-5 grid gap-5 md:grid-cols-3">
                <div>
                    <label
                        htmlFor="export_start_date"
                        className="mb-2 block text-sm font-medium text-slate-300"
                    >
                        Start Date
                    </label>

                    <input
                        id="export_start_date"
                        type="date"
                        required
                        value={startDate}
                        onChange={(event) => {
                            onStartDateChange(
                                event.target.value,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    />
                </div>

                <div>
                    <label
                        htmlFor="export_end_date"
                        className="mb-2 block text-sm font-medium text-slate-300"
                    >
                        End Date
                    </label>

                    <input
                        id="export_end_date"
                        type="date"
                        required
                        value={endDate}
                        onChange={(event) => {
                            onEndDateChange(
                                event.target.value,
                            );
                        }}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                    />
                </div>

                {source === "reports" && (
                    <div>
                        <label
                            htmlFor="export_status"
                            className="mb-2 block text-sm font-medium text-slate-300"
                        >
                            Status
                        </label>

                        <select
                            id="export_status"
                            value={status}
                            onChange={(event) => {
                                onStatusChange(
                                    event.target.value as
                                    | InvestigationStatus
                                    | "",
                                );
                            }}
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                        >
                            <option value="">
                                All statuses
                            </option>

                            <option value="Resolved">
                                Resolved
                            </option>

                            <option value="Waiting">
                                Waiting
                            </option>

                            <option value="Technical Investigation">
                                Technical Investigation
                            </option>

                            <option value="Escalated">
                                Escalated
                            </option>
                        </select>
                    </div>
                )}

                {source === "analytics" && (
                    <div>
                        <label
                            htmlFor="export_interval"
                            className="mb-2 block text-sm font-medium text-slate-300"
                        >
                            Interval
                        </label>

                        <select
                            id="export_interval"
                            value={interval}
                            onChange={(event) => {
                                onIntervalChange(
                                    event.target.value as AnalyticsInterval,
                                );
                            }}
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-white outline-none focus:border-slate-500"
                        >
                            <option value="day">
                                Daily
                            </option>

                            <option value="week">
                                Weekly
                            </option>

                            <option value="month">
                                Monthly
                            </option>
                        </select>
                    </div>
                )}
            </div>

            <div className="mt-6 flex justify-end">
                <button
                    type="button"
                    onClick={onGeneratePreview}
                    disabled={
                        isLoading ||
                        !startDate ||
                        !endDate
                    }
                    className="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {isLoading
                        ? "Generating preview..."
                        : "Generate Preview"}
                </button>
            </div>
        </Card>
    );
}

export default ExportOptions;