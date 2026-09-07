import UserStatusBadge from "./UserStatusBadge";

import type {
    AdminUser,
} from "../types/userAdministration.types";

import type {
    Organization,
} from "../../organizations/types/organization.types";

interface UserTableProps {
    users: AdminUser[];
    organizations: Organization[];
    currentUserId?: string;
    isSuperAdmin: boolean;
    onActivate: (userId: string) => void;
    onDeactivate: (userId: string) => void;
    onChangeRole: (
        userId: string,
        role: AdminUser["role"],
    ) => void;
}

function UserTable({
    users,
    organizations,
    currentUserId,
    isSuperAdmin,
    onActivate,
    onDeactivate,
    onChangeRole,
}: UserTableProps) {
    function formatRole(
        role: AdminUser["role"],
    ): string {
        switch (role) {
            case "super_admin":
                return "Super Admin";

            case "admin":
                return "Admin";

            case "supervisor":
                return "Supervisor";

            case "agent":
                return "Agent";

            default:
                return role;
        }
    }

    function getOrganizationName(
        organizationId: string | null | undefined,
    ): string {
        if (!organizationId) {
            return "Platform";
        }

        const organization = organizations.find(
            (item) =>
                item.organization_id === organizationId,
        );

        return (
            organization?.name ??
            organizationId
        );
    }

    return (
        <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-800">
                <thead className="bg-slate-900">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                            User
                        </th>

                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                            Role
                        </th>

                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                            Organization
                        </th>

                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                            Status
                        </th>

                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                            Created
                        </th>

                        <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wide text-slate-400">
                            Actions
                        </th>
                    </tr>
                </thead>

                <tbody className="divide-y divide-slate-800 bg-slate-950">
                    {users.map((user) => {
                        const isSelf =
                            user.id === currentUserId;

                        const canChangeRole =
                            isSuperAdmin &&
                            !isSelf &&
                            user.role !== "super_admin";

                        const canChangeStatus =
                            !isSelf;

                        return (
                            <tr
                                key={user.id}
                                className="transition hover:bg-slate-900/60"
                            >
                                <td className="px-6 py-4">
                                    <div className="font-medium text-white">
                                        {user.full_name}
                                    </div>

                                    <div className="mt-1 text-sm text-slate-500">
                                        {user.email}
                                    </div>

                                    {isSelf && (
                                        <div className="mt-1 text-xs text-slate-600">
                                            Current user
                                        </div>
                                    )}
                                </td>

                                <td className="px-6 py-4">
                                    {canChangeRole ? (
                                        <select
                                            value={user.role}
                                            onChange={(event) => {
                                                onChangeRole(
                                                    user.id,
                                                    event.target
                                                        .value as AdminUser["role"],
                                                );
                                            }}
                                            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none transition focus:border-slate-500"
                                        >
                                            <option value="agent">
                                                Agent
                                            </option>

                                            <option value="supervisor">
                                                Supervisor
                                            </option>

                                            <option value="admin">
                                                Admin
                                            </option>
                                        </select>
                                    ) : (
                                        <span className="text-sm text-slate-300">
                                            {formatRole(user.role)}
                                        </span>
                                    )}
                                </td>

                                <td className="px-6 py-4 text-sm text-slate-400">
                                    {getOrganizationName(
                                        user.organization_id,
                                    )}
                                </td>

                                <td className="px-6 py-4">
                                    <UserStatusBadge
                                        isActive={
                                            user.is_active
                                        }
                                    />
                                </td>

                                <td className="px-6 py-4 text-sm text-slate-400">
                                    {new Date(
                                        user.created_at,
                                    ).toLocaleDateString()}
                                </td>

                                <td className="px-6 py-4 text-right">
                                    {canChangeStatus && (
                                        <button
                                            type="button"
                                            onClick={() => {
                                                if (
                                                    user.is_active
                                                ) {
                                                    onDeactivate(
                                                        user.id,
                                                    );
                                                } else {
                                                    onActivate(
                                                        user.id,
                                                    );
                                                }
                                            }}
                                            className="rounded-lg border border-slate-700 px-3 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500 hover:bg-slate-800"
                                        >
                                            {user.is_active
                                                ? "Deactivate"
                                                : "Activate"}
                                        </button>
                                    )}

                                    {isSelf && (
                                        <span className="text-xs text-slate-600">
                                            No self-management
                                        </span>
                                    )}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>

            {users.length === 0 && (
                <div className="px-6 py-12 text-center text-sm text-slate-500">
                    No users found.
                </div>
            )}
        </div>
    );
}

export default UserTable;