import type { ReactNode } from "react";

import Card from "../../../shared/components/Card";

import type {
    ExportHistoryItem,
} from "../types/export.types";

interface ExportHistoryProps {
    history: ExportHistoryItem[];
}

function ExportHistory({
    history,
}: ExportHistoryProps) {
    return (
        <Card>
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Trust Ledger
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Immutable export audit records stored by the
                    Andiny Trust Ledger.
                </p>
            </div>

            {history.length === 0 ? (
                <div className="mt-6 rounded-lg border border-dashed border-slate-700 p-6">
                    <p className="text-center text-sm text-slate-500">
                        No Trust Ledger export records are available.
                    </p>
                </div>
            ) : (
                <div className="mt-6 overflow-x-auto">
                    <table className="min-w-full divide-y divide-slate-800">
                        <thead className="bg-slate-950/60">
                            <tr>
                                <TableHeading>
                                    File
                                </TableHeading>

                                <TableHeading>
                                    Source
                                </TableHeading>

                                <TableHeading>
                                    Format
                                </TableHeading>

                                <TableHeading>
                                    Records
                                </TableHeading>

                                <TableHeading>
                                    Status
                                </TableHeading>

                                <TableHeading>
                                    Exported At
                                </TableHeading>
                            </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-800">
                            {history.map((item) => (
                                <tr
                                    key={item.audit_id}
                                    className="transition hover:bg-slate-800/30"
                                >
                                    <TableCell>
                                        {item.file_name}
                                    </TableCell>

                                    <TableCell>
                                        {item.source ===
                                            "reports"
                                            ? "Investigation Reports"
                                            : "Investigation Analytics"}
                                    </TableCell>

                                    <TableCell>
                                        {item.export_format ===
                                            "excel"
                                            ? "Excel (.xlsx)"
                                            : item.export_format.toUpperCase()}
                                    </TableCell>

                                    <TableCell>
                                        {item.record_count}
                                    </TableCell>

                                    <TableCell>
                                        <span
                                            className={
                                                item.status ===
                                                    "Success"
                                                    ? "text-green-400"
                                                    : "text-red-400"
                                            }
                                        >
                                            {item.status}
                                        </span>
                                    </TableCell>

                                    <TableCell>
                                        {new Date(
                                            item.timestamp_utc,
                                        ).toLocaleString(
                                            "en-GB",
                                        )}
                                    </TableCell>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </Card>
    );
}

interface TableHeadingProps {
    children: ReactNode;
}

function TableHeading({
    children,
}: TableHeadingProps) {
    return (
        <th className="px-5 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
            {children}
        </th>
    );
}

interface TableCellProps {
    children: ReactNode;
}

function TableCell({
    children,
}: TableCellProps) {
    return (
        <td className="px-5 py-4 text-sm text-slate-300">
            {children}
        </td>
    );
}

export default ExportHistory;