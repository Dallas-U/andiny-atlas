import StatusBadge from "../../../shared/components/StatusBadge";
import Card from "../../../shared/components/Card";

import type { CaseResponse } from "../../investigation/types/investigation.types";

interface ReportResultsTableProps {
    investigations: CaseResponse[];
}

function ReportResultsTable({
    investigations,
}: ReportResultsTableProps) {
    if (investigations.length === 0) {
        return (
            <Card>
                <div className="py-12 text-center">
                    <h3 className="text-lg font-semibold text-white">
                        No investigations found
                    </h3>

                    <p className="mt-2 text-slate-400">
                        Try changing the report filters and generate the report
                        again.
                    </p>
                </div>
            </Card>
        );
    }

    return (
        <Card className="overflow-hidden p-0">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-800">
                    <thead className="bg-slate-950/60">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Customer
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Phone
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Status
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Created
                            </th>

                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Investigator
                            </th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-800">
                        {investigations.map((investigation) => (
                            <tr
                                key={investigation.case_id}
                                className="hover:bg-slate-800/40 transition"
                            >
                                <td className="px-6 py-4 font-medium text-white">
                                    {investigation.customer_name}
                                </td>

                                <td className="px-6 py-4 text-slate-300">
                                    {investigation.phone_number}
                                </td>

                                <td className="px-6 py-4">
                                    <StatusBadge
                                        status={
                                            investigation.result.status
                                        }
                                    />
                                </td>

                                <td className="px-6 py-4 text-slate-300">
                                    {new Date(
                                        investigation.timestamp,
                                    ).toLocaleString()}
                                </td>

                                <td className="px-6 py-4 text-slate-400">
                                    {investigation.created_by}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Card>
    );
}

export default ReportResultsTable;