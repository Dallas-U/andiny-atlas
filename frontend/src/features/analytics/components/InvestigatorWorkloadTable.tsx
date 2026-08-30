import Card from "../../../shared/components/Card";
import EmptyState from "../../../shared/components/EmptyState";

import type {
    InvestigatorWorkloadItem,
} from "../types/analytics.types";

interface InvestigatorWorkloadTableProps {
    investigators: InvestigatorWorkloadItem[];
}

function InvestigatorWorkloadTable({
    investigators,
}: InvestigatorWorkloadTableProps) {
    if (investigators.length === 0) {
        return (
            <EmptyState
                title="No investigator activity"
                description="No investigations were created during the selected period."
            />
        );
    }

    return (
        <Card>
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Investigator Workload
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Number of investigations created by each investigator.
                </p>
            </div>

            <div className="mt-6 overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-800">
                    <thead className="bg-slate-950/60">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                                Investigator
                            </th>

                            <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wide text-slate-500">
                                Investigations
                            </th>
                        </tr>
                    </thead>

                    <tbody className="divide-y divide-slate-800">
                        {investigators.map((investigator) => (
                            <tr
                                key={investigator.investigator_id}
                                className="transition hover:bg-slate-800/40"
                            >
                                <td className="px-6 py-4">
                                    <div>
                                        <p className="font-medium text-white">
                                            {investigator.investigator_name}
                                        </p>

                                        <p className="mt-1 text-xs text-slate-500">
                                            {investigator.investigator_id}
                                        </p>
                                    </div>
                                </td>

                                <td className="px-6 py-4 text-right text-lg font-semibold text-white">
                                    {investigator.count}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Card>
    );
}

export default InvestigatorWorkloadTable;