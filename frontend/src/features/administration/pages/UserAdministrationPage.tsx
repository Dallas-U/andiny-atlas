import {
    useEffect,
    useState,
    type FormEvent,
} from "react";

import BackButton from "../../../shared/components/BackButton";
import Card from "../../../shared/components/Card";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import PageHeader from "../../../shared/components/PageHeader";

import {
    activateUser,
    changeUserRole,
    createUser,
    deactivateUser,
    listUsers,
} from "../api/userAdministration.api";

import UserTable from "../components/UserTable";

import type {
    AdminUser,
    CreateAdminUserRequest,
} from "../types/userAdministration.types";

import { useAuth } from "../../../shared/auth/AuthContext";

function UserAdministrationPage() {
    const {
        currentUser,
    } = useAuth();

    const [
        users,
        setUsers,
    ] = useState<AdminUser[]>([]);

    const [
        page,
        setPage,
    ] = useState(1);

    const [
        totalPages,
        setTotalPages,
    ] = useState(0);

    const [
        totalUsers,
        setTotalUsers,
    ] = useState(0);

    const [
        isLoading,
        setIsLoading,
    ] = useState(true);

    const [
        isCreating,
        setIsCreating,
    ] = useState(false);

    const [
        showCreateForm,
        setShowCreateForm,
    ] = useState(false);

    const [
        error,
        setError,
    ] = useState<string | null>(null);

    const [
        success,
        setSuccess,
    ] = useState<string | null>(null);

    const [
        form,
        setForm,
    ] = useState<CreateAdminUserRequest>({
        full_name: "",
        email: "",
        password: "",
        role: "agent",
        organization_id: "",
    });

    const isSuperAdmin =
        currentUser?.role === "super_admin";

    async function loadUsers(
        requestedPage = page,
    ): Promise<void> {
        setIsLoading(true);
        setError(null);

        try {
            const response =
                await listUsers(
                    requestedPage,
                    20,
                );

            setUsers(response.users);
            setPage(response.page);
            setTotalPages(response.total_pages);
            setTotalUsers(response.total);
        } catch (loadError) {
            console.error(
                "Failed to load users:",
                loadError,
            );

            setError(
                "Unable to load users. Please try again.",
            );
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        void loadUsers(1);
    }, []);

    function updateForm(
        field: keyof CreateAdminUserRequest,
        value: string,
    ): void {
        setForm((previous) => ({
            ...previous,
            [field]: value,
        }));
    }

    async function handleCreateUser(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        setIsCreating(true);
        setError(null);
        setSuccess(null);

        try {
            const request: CreateAdminUserRequest = {
                full_name: form.full_name.trim(),
                email: form.email.trim(),
                password: form.password,
                role: form.role,
            };

            if (
                isSuperAdmin &&
                form.role !== "super_admin"
            ) {
                request.organization_id =
                    form.organization_id?.trim();
            }

            await createUser(request);

            setForm({
                full_name: "",
                email: "",
                password: "",
                role: "agent",
                organization_id: "",
            });

            setShowCreateForm(false);
            setSuccess(
                "User provisioned successfully.",
            );

            await loadUsers(1);
        } catch (createError) {
            console.error(
                "Failed to create user:",
                createError,
            );

            setError(
                "Unable to provision the user. Please verify the information and try again.",
            );
        } finally {
            setIsCreating(false);
        }
    }

    async function handleActivate(
        userId: string,
    ): Promise<void> {
        setError(null);
        setSuccess(null);

        try {
            await activateUser(userId);

            setSuccess(
                "User activated successfully.",
            );

            await loadUsers(page);
        } catch (activationError) {
            console.error(
                "Failed to activate user:",
                activationError,
            );

            setError(
                "Unable to activate the user.",
            );
        }
    }

    async function handleDeactivate(
        userId: string,
    ): Promise<void> {
        setError(null);
        setSuccess(null);

        try {
            await deactivateUser(userId);

            setSuccess(
                "User deactivated successfully.",
            );

            await loadUsers(page);
        } catch (deactivationError) {
            console.error(
                "Failed to deactivate user:",
                deactivationError,
            );

            setError(
                "Unable to deactivate the user.",
            );
        }
    }

    async function handleChangeRole(
        userId: string,
        role: AdminUser["role"],
    ): Promise<void> {
        setError(null);
        setSuccess(null);

        try {
            await changeUserRole(
                userId,
                { role },
            );

            setSuccess(
                "User role updated successfully.",
            );

            await loadUsers(page);
        } catch (roleError) {
            console.error(
                "Failed to change user role:",
                roleError,
            );

            setError(
                "Unable to change the user's role.",
            );
        }
    }

    function goToPreviousPage(): void {
        if (page <= 1) {
            return;
        }

        void loadUsers(page - 1);
    }

    function goToNextPage(): void {
        if (page >= totalPages) {
            return;
        }

        void loadUsers(page + 1);
    }

    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="User Administration"
                    description="Manage users and authorization within the enterprise."
                />

                <div className="mt-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                    <div>
                        <p className="text-sm text-slate-400">
                            {isSuperAdmin
                                ? "Platform-wide user administration."
                                : "Users belonging to your organization."}
                        </p>

                        <p className="mt-1 text-xs text-slate-600">
                            {totalUsers} total user
                            {totalUsers === 1
                                ? ""
                                : "s"}
                        </p>
                    </div>

                    <button
                        type="button"
                        onClick={() => {
                            setShowCreateForm(
                                (visible) => !visible,
                            );
                            setError(null);
                            setSuccess(null);
                        }}
                        className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-slate-200"
                    >
                        {showCreateForm
                            ? "Cancel"
                            : "Provision User"}
                    </button>
                </div>

                {success && (
                    <div className="mt-6 rounded-xl border border-emerald-900/50 bg-emerald-950/30 px-5 py-4 text-sm text-emerald-300">
                        {success}
                    </div>
                )}

                {error && (
                    <div className="mt-6 rounded-xl border border-red-900/50 bg-red-950/30 px-5 py-4 text-sm text-red-300">
                        {error}
                    </div>
                )}

                {showCreateForm && (
                    <Card className="mt-6">
                        <div className="mb-6">
                            <h2 className="text-lg font-semibold text-white">
                                Provision User
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                Create a new Atlas application user.
                            </p>
                        </div>

                        <form
                            onSubmit={(event) => {
                                void handleCreateUser(
                                    event,
                                );
                            }}
                            className="grid gap-5 md:grid-cols-2"
                        >
                            <label className="block">
                                <span className="text-sm font-medium text-slate-300">
                                    Full name
                                </span>

                                <input
                                    required
                                    minLength={2}
                                    maxLength={150}
                                    value={
                                        form.full_name
                                    }
                                    onChange={(event) => {
                                        updateForm(
                                            "full_name",
                                            event.target.value,
                                        );
                                    }}
                                    className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-slate-500"
                                />
                            </label>

                            <label className="block">
                                <span className="text-sm font-medium text-slate-300">
                                    Email
                                </span>

                                <input
                                    required
                                    type="email"
                                    value={form.email}
                                    onChange={(event) => {
                                        updateForm(
                                            "email",
                                            event.target.value,
                                        );
                                    }}
                                    className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-slate-500"
                                />
                            </label>

                            <label className="block">
                                <span className="text-sm font-medium text-slate-300">
                                    Temporary password
                                </span>

                                <input
                                    required
                                    type="password"
                                    minLength={8}
                                    maxLength={128}
                                    value={
                                        form.password
                                    }
                                    onChange={(event) => {
                                        updateForm(
                                            "password",
                                            event.target.value,
                                        );
                                    }}
                                    className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-slate-500"
                                />
                            </label>

                            <label className="block">
                                <span className="text-sm font-medium text-slate-300">
                                    Role
                                </span>

                                <select
                                    value={
                                        form.role
                                    }
                                    onChange={(event) => {
                                        updateForm(
                                            "role",
                                            event.target.value,
                                        );
                                    }}
                                    className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-slate-500"
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

                                    {isSuperAdmin && (
                                        <option value="super_admin">
                                            Super Admin
                                        </option>
                                    )}
                                </select>
                            </label>

                            {isSuperAdmin &&
                                form.role !==
                                "super_admin" && (
                                    <label className="block md:col-span-2">
                                        <span className="text-sm font-medium text-slate-300">
                                            Organization ID
                                        </span>

                                        <input
                                            required
                                            value={
                                                form.organization_id ??
                                                ""
                                            }
                                            onChange={(event) => {
                                                updateForm(
                                                    "organization_id",
                                                    event.target.value,
                                                );
                                            }}
                                            placeholder="Enter customer organization ID"
                                            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-slate-500"
                                        />

                                        <p className="mt-2 text-xs text-slate-600">
                                            Required when a Super Admin provisions a customer user.
                                        </p>
                                    </label>
                                )}

                            <div className="flex justify-end md:col-span-2">
                                <button
                                    type="submit"
                                    disabled={isCreating}
                                    className="rounded-lg bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
                                >
                                    {isCreating
                                        ? "Provisioning..."
                                        : "Provision User"}
                                </button>
                            </div>
                        </form>
                    </Card>
                )}

                <Card className="mt-8 overflow-hidden">
                    <div className="border-b border-slate-800 px-6 py-5">
                        <div>
                            <h2 className="text-lg font-semibold text-white">
                                Users
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                Authorization and account status.
                            </p>
                        </div>
                    </div>

                    {isLoading ? (
                        <div className="p-6">
                            <LoadingSkeleton />
                        </div>
                    ) : (
                        <>
                            <UserTable
                                users={users}
                                currentUserId={
                                    currentUser?.id
                                }
                                isSuperAdmin={
                                    isSuperAdmin
                                }
                                onActivate={(
                                    userId,
                                ) => {
                                    void handleActivate(
                                        userId,
                                    );
                                }}
                                onDeactivate={(
                                    userId,
                                ) => {
                                    void handleDeactivate(
                                        userId,
                                    );
                                }}
                                onChangeRole={(
                                    userId,
                                    role,
                                ) => {
                                    void handleChangeRole(
                                        userId,
                                        role,
                                    );
                                }}
                            />

                            {totalPages > 1 && (
                                <div className="flex items-center justify-between border-t border-slate-800 px-6 py-4">
                                    <p className="text-sm text-slate-500">
                                        Page {page} of{" "}
                                        {totalPages}
                                    </p>

                                    <div className="flex gap-2">
                                        <button
                                            type="button"
                                            disabled={
                                                page <=
                                                1
                                            }
                                            onClick={
                                                goToPreviousPage
                                            }
                                            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                                        >
                                            Previous
                                        </button>

                                        <button
                                            type="button"
                                            disabled={
                                                page >=
                                                totalPages
                                            }
                                            onClick={
                                                goToNextPage
                                            }
                                            className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                                        >
                                            Next
                                        </button>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </Card>
            </div>
        </main>
    );
}

export default UserAdministrationPage;