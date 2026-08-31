interface UserStatusBadgeProps {
    isActive: boolean;
}

function UserStatusBadge({
    isActive,
}: UserStatusBadgeProps) {
    return (
        <span
            className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${isActive
                    ? "bg-emerald-500/10 text-emerald-400"
                    : "bg-slate-700 text-slate-400"
                }`}
        >
            {isActive ? "Active" : "Inactive"}
        </span>
    );
}

export default UserStatusBadge;