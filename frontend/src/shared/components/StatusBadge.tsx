import type { InvestigationStatus } from "../../features/investigation/types/investigation.types";

interface StatusBadgeProps {
    status: InvestigationStatus;
}

const statusStyles: Record<
    InvestigationStatus,
    string
> = {
    Resolved:
        "bg-green-500/15 text-green-300 border border-green-500/20",

    Waiting:
        "bg-amber-500/15 text-amber-300 border border-amber-500/20",

    "Technical Investigation":
        "bg-blue-500/15 text-blue-300 border border-blue-500/20",

    Escalated:
        "bg-red-500/15 text-red-300 border border-red-500/20",
};

function StatusBadge({
    status,
}: StatusBadgeProps) {
    return (
        <span
            className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${statusStyles[status]}`}
        >
            {status}
        </span>
    );
}

export default StatusBadge;