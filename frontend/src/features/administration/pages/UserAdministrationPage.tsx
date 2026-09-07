import {
    useEffect,
    useState,
    type FormEvent,
} from "react";

import axios from "axios";

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

import {
    listOrganizations,
} from "../../organizations/api/organization.api";

import UserTable from "../components/UserTable";

import type {
    AdminUser,
    CreateAdminUserRequest,
    UserRole,
} from "../types/userAdministration.types";

import type {
    Organization,
} from "../../organizations/types/organization.types";

import { useAuth } from "../../../shared/auth/AuthContext";


const initialForm: CreateAdminUserRequest = {
    full_name: "",
    email: "",
    password: "",
    role: "agent",
    organization_id: "",
};


function UserAdministrationPage() {
    const {
        currentUser,
    } = useAuth();

    const [
        users,
        setUsers,
    ] = useState<AdminUser[]>([]);

    const [
        organizations,
        setOrganizations,
    ] = useState<Organization[]>([]);

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
        isLoadingOrganizations,
        setIsLoadingOrganizations,
    ] = useState(false);

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
    ] = useState<CreateAdminUserRequest>(
        initialForm,
    );

    const isSuperAdmin =
        currentUser?.role === "super_admin";


    async function loadUsers(
        requestedPage = 1,
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
                getErrorMessage(
                    loadError,
                    "Unable to load users. Please try again.",
                ),
            );
        } finally {
            setIsLoading(false);
        }
    }


    async function loadOrganizations(): Promise<void> {
        if (!isSuperAdmin) {
            setOrganizations([]);
            return;
        }

        setIsLoadingOrganizations(true);

        try {
            const response =
                await listOrganizations();

            setOrganizations(response);
        } catch (loadError) {
            console.error(
                "Failed to load organizations:",
                loadError,
            );

            setError(
                getErrorMessage(
                    loadError,
                    "Unable to load customer organizations.",
                ),
            );
        } finally {
            setIsLoadingOrganizations(false);
        }
    }


    useEffect(() => {
        void loadUsers(1);
    }, []);


    useEffect(() => {
        if (isSuperAdmin) {
            void loadOrganizations();
        } else {
            setOrganizations([]);
        }
    }, [isSuperAdmin]);


    function updateForm(
        field: keyof CreateAdminUserRequest,
        value: string,
    ): void {
        setForm((previous) => ({
            ...previous,
            [field]: value,
        }));
    }


    function handleRoleChange(
        role: UserRole,
    ): void {
        setForm((previous) => ({
            ...previous,
            role,
            organization_id:
                role === "super_admin"
                    ? ""
                    : previous.organization_id,
        }));
    }


    function handleToggleCreateForm(): void {
        setShowCreateForm((visible) => !visible);

        setError(null);
        setSuccess(null);

        if (showCreateForm) {
            setForm(initialForm);
        }
    }


    async function handleCreateUser(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        setError(null);
        setSuccess(null);

        const fullName =
            form.full_name.trim();

        const email =
            form.email.trim();

        const organizationId =
            form.organization_id?.trim() ?? "";

        if (!fullName) {
            setError(
                "Full name is required.",
            );
            return;
        }

        if (!email) {
            setError(
                "Email is required.",
            );
            return;
        }

        if (!form.password) {
            setError(
                "Temporary password is required.",
            );
            return;
        }

        if (
            isSuperAdmin &&
            form.role !== "super_admin" &&
            !organizationId
        ) {
            setError(
                "Select a customer organization for this user.",
            );
            return;
        }

        setIsCreating(true);

        try {
            const request: CreateAdminUserRequest = {
                full_name: fullName,
                email,
                password: form.password,
                role: form.role,
            };

            /*
             * Super Admin provisioning:
             *
             * - Super Admin users are platform-scoped
             *   and do not have an organization.
             *
             * - Customer users must belong to an
             *   organization.
             *
             * Customer Admin provisioning:
             *
             * - The backend determines the organization
             *   from the authenticated user.
             */
            if (
                isSuperAdmin &&
                form.role !== "super_admin"
            ) {
                request.organization_id =
                    organizationId;
            }

            await createUser(request);

            setForm(initialForm);

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
                getErrorMessage(
                    createError,
                    "Unable to provision the user.",
                ),
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
                getErrorMessage(
                    activationError,
                    "Unable to activate the user.",
                ),
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
                getErrorMessage(
                    deactivationError,
                    "Unable to deactivate the user.",
                ),
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
                getErrorMessage(
                    roleError,
                    "Unable to change the user's role.",
                ),
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
        if (
            totalPages === 0 ||
            page >= totalPages
        ) {
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
                    description={
                        isSuperAdmin
                            ? "Manage users and authorization across the Andiny Atlas platform."
                            : "Manage users within your organization."
                    }
                />


                <Card className="mt-8">
                    <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">

                        <div>
                            <h2 className="text-lg font-semibold text-white">
                                Users
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                {isSuperAdmin
                                    ? "Platform-wide user administration."
                                    : "Users belonging to your organization."}
                            </p>

                            <p className="mt-2 text-sm text-slate-500">
                                {totalUsers} total user
                                {totalUsers === 1
                                    ? ""
                                    : "s"}
                            </p>
                        </div>


                        <button
                            type="button"
                            onClick={handleToggleCreateForm}
                            className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-slate-200"
                        >
                            {showCreateForm
                                ? "Cancel"
                                : "Provision User"}
                        </button>

                    </div>
                </Card>


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
                                Create a new Andiny Atlas
                                application user.
                            </p>
                        </div>


                        <form
                            onSubmit={(event) => {
                                void handleCreateUser(event);
                            }}
                            className="space-y-6"
                        >

                            <div className="grid gap-6 md:grid-cols-2">

                                <label className="block">
                                    <span className="text-sm font-medium text-slate-300">
                                        Full name
                                    </span>

                                    <input
                                        type="text"
                                        required
                                        value={form.full_name}
                                        onChange={(event) => {
                                            updateForm(
                                                "full_name",
                                                event.target.value,
                                            );
                                        }}
                                        className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-slate-500"
                                    />
                                </label>


                                <label className="block">
                                    <span className="text-sm font-medium text-slate-300">
                                        Email
                                    </span>

                                    <input
                                        type="email"
                                        required
                                        value={form.email}
                                        onChange={(event) => {
                                            updateForm(
                                                "email",
                                                event.target.value,
                                            );
                                        }}
                                        className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-slate-500"
                                    />
                                </label>


                                <label className="block">
                                    <span className="text-sm font-medium text-slate-300">
                                        Temporary password
                                    </span>

                                    <input
                                        type="password"
                                        required
                                        value={form.password}
                                        onChange={(event) => {
                                            updateForm(
                                                "password",
                                                event.target.value,
                                            );
                                        }}
                                        className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-slate-500"
                                    />
                                </label>


                                <label className="block">
                                    <span className="text-sm font-medium text-slate-300">
                                        Role
                                    </span>

                                    <select
                                        value={form.role}
                                        onChange={(event) => {
                                            handleRoleChange(
                                                event.target
                                                    .value as UserRole,
                                            );
                                        }}
                                        className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-slate-500"
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
                                    form.role !== "super_admin" && (
                                        <label className="block md:col-span-2">

                                            <span className="text-sm font-medium text-slate-300">
                                                Organization
                                            </span>

                                            <select
                                                required
                                                disabled={
                                                    isLoadingOrganizations
                                                }
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
                                                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-slate-500 disabled:cursor-not-allowed disabled:opacity-50"
                                            >
                                                <option value="">
                                                    {isLoadingOrganizations
                                                        ? "Loading organizations..."
                                                        : "Select customer organization"}
                                                </option>

                                                {organizations
                                                    .filter(
                                                        (organization) =>
                                                            organization.is_active,
                                                    )
                                                    .map(
                                                        (organization) => (
                                                            <option
                                                                key={
                                                                    organization.organization_id
                                                                }
                                                                value={
                                                                    organization.organization_id
                                                                }
                                                            >
                                                                {organization.name}{" "}
                                                                (
                                                                {organization.code}
                                                                )
                                                            </option>
                                                        ),
                                                    )}
                                            </select>

                                            <p className="mt-2 text-xs text-slate-500">
                                                Select the customer
                                                organization this user
                                                belongs to.
                                            </p>

                                        </label>
                                    )}

                            </div>


                            <div className="flex justify-end">
                                <button
                                    type="submit"
                                    disabled={
                                        isCreating ||
                                        isLoadingOrganizations
                                    }
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

                        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">

                            <div>
                                <h2 className="text-lg font-semibold text-white">
                                    User Directory
                                </h2>

                                <p className="mt-1 text-sm text-slate-400">
                                    {isSuperAdmin
                                        ? "All users across the platform."
                                        : "Users within your organization."}
                                </p>
                            </div>


                            <div className="text-sm text-slate-500">
                                Page {page}
                                {totalPages > 0
                                    ? ` of ${totalPages}`
                                    : ""}
                            </div>

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
                                organizations={organizations}
                                currentUserId={
                                    currentUser?.id
                                }
                                isSuperAdmin={
                                    isSuperAdmin
                                }
                                onActivate={(userId) => {
                                    void handleActivate(userId);
                                }}
                                onDeactivate={(userId) => {
                                    void handleDeactivate(userId);
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

                                    <button
                                        type="button"
                                        disabled={page <= 1}
                                        onClick={
                                            goToPreviousPage
                                        }
                                        className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                                    >
                                        Previous
                                    </button>


                                    <span className="text-sm text-slate-400">
                                        Page {page} of{" "}
                                        {totalPages}
                                    </span>


                                    <button
                                        type="button"
                                        disabled={
                                            page >= totalPages
                                        }
                                        onClick={goToNextPage}
                                        className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                                    >
                                        Next
                                    </button>

                                </div>
                            )}
                        </>
                    )}

                </Card>

            </div>
        </main>
    );
}


function getErrorMessage(
    error: unknown,
    fallback: string,
): string {
    if (axios.isAxiosError(error)) {
        const detail =
            error.response?.data?.detail;

        if (typeof detail === "string") {
            return detail;
        }

        if (Array.isArray(detail)) {
            const messages = detail
                .map((item) => {
                    if (
                        typeof item === "object" &&
                        item !== null &&
                        "msg" in item
                    ) {
                        const message =
                            item.msg;

                        if (
                            typeof message === "string"
                        ) {
                            return message;
                        }
                    }

                    return null;
                })
                .filter(
                    (
                        message,
                    ): message is string =>
                        message !== null,
                );

            if (messages.length > 0) {
                return messages.join(" ");
            }
        }

        if (error.message) {
            return error.message;
        }
    }

    if (error instanceof Error) {
        return error.message;
    }

    return fallback;
}


export default UserAdministrationPage;