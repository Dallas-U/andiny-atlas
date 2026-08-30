import StatusBadge from "../../../shared/components/StatusBadge";
import type { CaseResponse } from "../types/investigation.types";

import {
    formatExactDate,
    formatRelativeDate,
} from "../../../shared/utils/date";

interface InvestigationDetailsProps {
    investigation: CaseResponse;
}

function InvestigationDetails({
    investigation,
}: InvestigationDetailsProps) {
    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div className="flex flex-col gap-3 border-b border-slate-800 pb-6 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
                        Investigation
                    </p>

                    <h2 className="mt-2 text-2xl font-semibold text-white">
                        {investigation.customer_name}
                    </h2>

                    <p className="mt-2 text-sm text-slate-400">
                        {investigation.case_id}
                    </p>
                </div>

                <StatusBadge
                    status={investigation.result.status}
                />
            </div>

            <dl className="mt-6 grid gap-5 sm:grid-cols-2">
                <div>
                    <dt className="text-sm text-slate-500">
                        Phone number
                    </dt>

                    <dd className="mt-1 text-slate-200">
                        {investigation.phone_number}
                    </dd>
                </div>

                <div>
                    <dt className="text-sm text-slate-500">
                        Created
                    </dt>

                    <dd className="mt-1 text-slate-200">
                        <time
                            dateTime={investigation.timestamp}
                            title={formatExactDate(investigation.timestamp)}
                        >
                            {formatRelativeDate(investigation.timestamp)}
                        </time>
                    </dd>
                </div>

                <div>
                    <dt className="text-sm text-slate-500">
                        Created by
                    </dt>

                    <dd className="mt-1 break-all text-slate-200">
                        {investigation.created_by}
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
        </section>
    );
}

export default InvestigationDetails;