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
    createBranch,
    createDepartment,
    listBranches,
    listDepartments,
} from "../api/customerAdministration.api";

import {
    createCustomerUser,
    listCustomerUsers,
    updateCustomerUserStatus,
} from "../api/customerUserAdministration.api";

import type {
    Branch,
    Department,
} from "../types/customerAdministration.types";

import type {
    CustomerUser,
    CustomerUserRole,
} from "../types/customerUserAdministration.types";

import { useAuth } from "../../../shared/auth/AuthContext";


function CustomerAdministrationPage() {
    const { currentUser } = useAuth();

    const organizationId =
        currentUser?.organization_id ?? null;

    const [branches, setBranches] =
        useState<Branch[]>([]);

    const [departments, setDepartments] =
        useState<Department[]>([]);

    const [customerUsers, setCustomerUsers] =
        useState<CustomerUser[]>([]);

    const [selectedBranchId, setSelectedBranchId] =
        useState<string | null>(null);

    const [isLoadingBranches, setIsLoadingBranches] =
        useState(false);

    const [isLoadingDepartments, setIsLoadingDepartments] =
        useState(false);

    const [isLoadingUsers, setIsLoadingUsers] =
        useState(false);

    const [isCreatingBranch, setIsCreatingBranch] =
        useState(false);

    const [isCreatingDepartment, setIsCreatingDepartment] =
        useState(false);

    const [isCreatingUser, setIsCreatingUser] =
        useState(false);

    const [updatingUserId, setUpdatingUserId] =
        useState<string | null>(null);

    const [branchName, setBranchName] =
        useState("");

    const [branchCode, setBranchCode] =
        useState("");

    const [branchCity, setBranchCity] =
        useState("");

    const [branchState, setBranchState] =
        useState("");

    const [departmentName, setDepartmentName] =
        useState("");

    const [departmentCode, setDepartmentCode] =
        useState("");

    const [userFullName, setUserFullName] =
        useState("");

    const [userEmail, setUserEmail] =
        useState("");

    const [userPassword, setUserPassword] =
        useState("");

    const [userRole, setUserRole] =
        useState<CustomerUserRole>("AGENT");

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    const [successMessage, setSuccessMessage] =
        useState<string | null>(null);


    function clearMessages(): void {
        setErrorMessage(null);
        setSuccessMessage(null);
    }


    async function loadBranches(): Promise<void> {
        if (!organizationId) {
            setBranches([]);
            return;
        }

        try {
            setIsLoadingBranches(true);
            setErrorMessage(null);

            const result =
                await listBranches(
                    organizationId,
                );

            setBranches(result);

            if (
                selectedBranchId &&
                !result.some(
                    (branch) =>
                        branch.branch_id ===
                        selectedBranchId,
                )
            ) {
                setSelectedBranchId(null);
                setDepartments([]);
            }
        } catch (error) {
            console.error(
                "Failed to load branches:",
                error,
            );

            setErrorMessage(
                "Unable to load organization branches.",
            );
        } finally {
            setIsLoadingBranches(false);
        }
    }


    async function loadDepartments(
        branchId: string,
    ): Promise<void> {
        try {
            setIsLoadingDepartments(true);
            setErrorMessage(null);

            const result =
                await listDepartments(
                    branchId,
                );

            setDepartments(result);
        } catch (error) {
            console.error(
                "Failed to load departments:",
                error,
            );

            setDepartments([]);

            setErrorMessage(
                "Unable to load branch departments.",
            );
        } finally {
            setIsLoadingDepartments(false);
        }
    }


    async function loadCustomerUsers(): Promise<void> {
        if (!organizationId) {
            setCustomerUsers([]);
            return;
        }

        try {
            setIsLoadingUsers(true);
            setErrorMessage(null);

            const result =
                await listCustomerUsers(
                    organizationId,
                );

            setCustomerUsers(result);
        } catch (error) {
            console.error(
                "Failed to load customer users:",
                error,
            );

            setErrorMessage(
                "Unable to load customer users.",
            );
        } finally {
            setIsLoadingUsers(false);
        }
    }


    useEffect(() => {
        void loadBranches();
    }, [organizationId]);


    useEffect(() => {
        void loadCustomerUsers();
    }, [organizationId]);


    useEffect(() => {
        if (!selectedBranchId) {
            setDepartments([]);
            return;
        }

        void loadDepartments(
            selectedBranchId,
        );
    }, [selectedBranchId]);


    async function handleCreateBranch(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        if (!organizationId) {
            setErrorMessage(
                "No organization is associated with the current user.",
            );

            return;
        }

        try {
            setIsCreatingBranch(true);
            clearMessages();

            await createBranch({
                organization_id:
                    organizationId,
                name: branchName.trim(),
                code: branchCode.trim(),
                city: branchCity.trim(),
                state: branchState.trim(),
            });

            setBranchName("");
            setBranchCode("");
            setBranchCity("");
            setBranchState("");

            setSuccessMessage(
                "Branch created successfully.",
            );

            await loadBranches();
        } catch (error) {
            console.error(
                "Failed to create branch:",
                error,
            );

            setErrorMessage(
                "Unable to create branch.",
            );
        } finally {
            setIsCreatingBranch(false);
        }
    }


    async function handleCreateDepartment(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        if (
            !organizationId ||
            !selectedBranchId
        ) {
            setErrorMessage(
                "Select a branch before creating a department.",
            );

            return;
        }

        try {
            setIsCreatingDepartment(true);
            clearMessages();

            await createDepartment({
                organization_id:
                    organizationId,
                branch_id:
                    selectedBranchId,
                name: departmentName.trim(),
                code: departmentCode.trim(),
            });

            setDepartmentName("");
            setDepartmentCode("");

            setSuccessMessage(
                "Department created successfully.",
            );

            await loadDepartments(
                selectedBranchId,
            );
        } catch (error) {
            console.error(
                "Failed to create department:",
                error,
            );

            setErrorMessage(
                "Unable to create department.",
            );
        } finally {
            setIsCreatingDepartment(false);
        }
    }


    async function handleCreateCustomerUser(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        if (!organizationId) {
            setErrorMessage(
                "No organization is associated with the current user.",
            );

            return;
        }

        try {
            setIsCreatingUser(true);
            clearMessages();

            await createCustomerUser({
                organization_id:
                    organizationId,
                full_name:
                    userFullName.trim(),
                email:
                    userEmail.trim(),
                password:
                    userPassword,
                role:
                    userRole,
            });

            setUserFullName("");
            setUserEmail("");
            setUserPassword("");
            setUserRole("AGENT");

            setSuccessMessage(
                "Customer user created successfully.",
            );

            await loadCustomerUsers();
        } catch (error) {
            console.error(
                "Failed to create customer user:",
                error,
            );

            setErrorMessage(
                "Unable to create customer user.",
            );
        } finally {
            setIsCreatingUser(false);
        }
    }


    async function handleUserStatusChange(
        user: CustomerUser,
    ): Promise<void> {
        try {
            setUpdatingUserId(user.id);
            clearMessages();

            await updateCustomerUserStatus(
                user.id,
                {
                    is_active:
                        !user.is_active,
                },
            );

            setSuccessMessage(
                `User ${user.full_name} was successfully ${user.is_active
                    ? "deactivated"
                    : "activated"
                }.`,
            );

            await loadCustomerUsers();
        } catch (error) {
            console.error(
                "Failed to update customer user status:",
                error,
            );

            setErrorMessage(
                "Unable to update customer user status.",
            );
        } finally {
            setUpdatingUserId(null);
        }
    }


    if (!organizationId) {
        return (
            <main className="min-h-screen bg-slate-950 px-10 py-8">
                <div className="mx-auto max-w-7xl">
                    <div className="mb-6">
                        <BackButton />
                    </div>

                    <PageHeader
                        title="Customer Administration"
                        description="Manage the operational structure and users of a customer organization."
                    />

                    <Card className="mt-8 border-red-900">
                        <p className="text-red-400">
                            Organization information is not available for
                            the current user.
                        </p>
                    </Card>
                </div>
            </main>
        );
    }


    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">

                <div className="mb-6">
                    <BackButton />
                </div>


                <PageHeader
                    title="Customer Administration"
                    description="Manage your organization's branches, departments, and authorized users."
                />


                {errorMessage && (
                    <div className="mt-6 rounded-xl border border-red-900 bg-red-950/40 px-5 py-4 text-red-300">
                        {errorMessage}
                    </div>
                )}


                {successMessage && (
                    <div className="mt-6 rounded-xl border border-emerald-900 bg-emerald-950/40 px-5 py-4 text-emerald-300">
                        {successMessage}
                    </div>
                )}


                <section className="mt-8">
                    <Card>
                        <div className="mb-6">
                            <h2 className="text-xl font-semibold text-white">
                                Branch Administration
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                Create and manage branches within your
                                organization.
                            </p>
                        </div>


                        <div className="grid gap-8 lg:grid-cols-2">

                            <div>
                                <h3 className="mb-4 text-lg font-semibold text-white">
                                    Organization Branches
                                </h3>

                                {isLoadingBranches ? (
                                    <LoadingSkeleton />
                                ) : branches.length === 0 ? (
                                    <div className="rounded-xl border border-dashed border-slate-800 p-6 text-sm text-slate-500">
                                        No branches have been created yet.
                                    </div>
                                ) : (
                                    <div className="space-y-3">
                                        {branches.map(
                                            (branch) => (
                                                <button
                                                    key={
                                                        branch.branch_id
                                                    }
                                                    type="button"
                                                    onClick={() =>
                                                        setSelectedBranchId(
                                                            branch.branch_id,
                                                        )
                                                    }
                                                    className={`w-full rounded-xl border p-4 text-left transition ${selectedBranchId ===
                                                            branch.branch_id
                                                            ? "border-blue-500 bg-slate-900"
                                                            : "border-slate-800 bg-slate-950 hover:border-slate-700"
                                                        }`}
                                                >
                                                    <div className="flex items-start justify-between gap-4">
                                                        <div>
                                                            <h4 className="font-semibold text-white">
                                                                {
                                                                    branch.name
                                                                }
                                                            </h4>

                                                            <p className="mt-1 text-sm text-slate-400">
                                                                {
                                                                    branch.code
                                                                }
                                                            </p>

                                                            <p className="mt-1 text-sm text-slate-500">
                                                                {
                                                                    branch.city
                                                                }
                                                                ,{" "}
                                                                {
                                                                    branch.state
                                                                }
                                                            </p>
                                                        </div>

                                                        <StatusBadge
                                                            isActive={
                                                                branch.is_active
                                                            }
                                                        />
                                                    </div>
                                                </button>
                                            ),
                                        )}
                                    </div>
                                )}
                            </div>


                            <div>
                                <h3 className="mb-4 text-lg font-semibold text-white">
                                    Create Branch
                                </h3>

                                <form
                                    onSubmit={
                                        handleCreateBranch
                                    }
                                    className="space-y-4"
                                >
                                    <TextInput
                                        value={branchName}
                                        onChange={
                                            setBranchName
                                        }
                                        placeholder="Branch name"
                                    />

                                    <TextInput
                                        value={branchCode}
                                        onChange={
                                            setBranchCode
                                        }
                                        placeholder="Branch code"
                                    />

                                    <TextInput
                                        value={branchCity}
                                        onChange={
                                            setBranchCity
                                        }
                                        placeholder="City"
                                    />

                                    <TextInput
                                        value={branchState}
                                        onChange={
                                            setBranchState
                                        }
                                        placeholder="State"
                                    />

                                    <PrimaryButton
                                        type="submit"
                                        disabled={
                                            isCreatingBranch
                                        }
                                    >
                                        {isCreatingBranch
                                            ? "Creating branch..."
                                            : "Create branch"}
                                    </PrimaryButton>
                                </form>
                            </div>

                        </div>
                    </Card>
                </section>


                <section className="mt-8">
                    <Card>
                        <div className="mb-6">
                            <h2 className="text-xl font-semibold text-white">
                                Department Administration
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                Manage departments within the selected branch.
                            </p>
                        </div>


                        {!selectedBranchId ? (
                            <div className="rounded-xl border border-dashed border-slate-800 p-6 text-sm text-slate-500">
                                Select a branch to manage its departments.
                            </div>
                        ) : (
                            <div className="grid gap-8 lg:grid-cols-2">

                                <div>
                                    <h3 className="mb-4 text-lg font-semibold text-white">
                                        Branch Departments
                                    </h3>

                                    {isLoadingDepartments ? (
                                        <LoadingSkeleton />
                                    ) : departments.length === 0 ? (
                                        <div className="rounded-xl border border-dashed border-slate-800 p-6 text-sm text-slate-500">
                                            No departments have been created
                                            for this branch.
                                        </div>
                                    ) : (
                                        <div className="space-y-3">
                                            {departments.map(
                                                (department) => (
                                                    <div
                                                        key={
                                                            department.department_id
                                                        }
                                                        className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                                                    >
                                                        <div className="flex items-start justify-between gap-4">
                                                            <div>
                                                                <h4 className="font-semibold text-white">
                                                                    {
                                                                        department.name
                                                                    }
                                                                </h4>

                                                                <p className="mt-1 text-sm text-slate-400">
                                                                    {
                                                                        department.code
                                                                    }
                                                                </p>
                                                            </div>

                                                            <StatusBadge
                                                                isActive={
                                                                    department.is_active
                                                                }
                                                            />
                                                        </div>
                                                    </div>
                                                ),
                                            )}
                                        </div>
                                    )}
                                </div>


                                <div>
                                    <h3 className="mb-4 text-lg font-semibold text-white">
                                        Create Department
                                    </h3>

                                    <form
                                        onSubmit={
                                            handleCreateDepartment
                                        }
                                        className="space-y-4"
                                    >
                                        <TextInput
                                            value={
                                                departmentName
                                            }
                                            onChange={
                                                setDepartmentName
                                            }
                                            placeholder="Department name"
                                        />

                                        <TextInput
                                            value={
                                                departmentCode
                                            }
                                            onChange={
                                                setDepartmentCode
                                            }
                                            placeholder="Department code"
                                        />

                                        <PrimaryButton
                                            type="submit"
                                            disabled={
                                                isCreatingDepartment
                                            }
                                        >
                                            {isCreatingDepartment
                                                ? "Creating department..."
                                                : "Create department"}
                                        </PrimaryButton>
                                    </form>
                                </div>

                            </div>
                        )}
                    </Card>
                </section>


                <section className="mt-8">
                    <Card>
                        <div className="mb-6">
                            <h2 className="text-xl font-semibold text-white">
                                Tenant User Administration
                            </h2>

                            <p className="mt-1 text-sm text-slate-400">
                                Create and manage authorized users within
                                your organization.
                            </p>
                        </div>


                        <div className="grid gap-8 lg:grid-cols-2">

                            <div>
                                <h3 className="mb-4 text-lg font-semibold text-white">
                                    Customer Users
                                </h3>

                                {isLoadingUsers ? (
                                    <LoadingSkeleton />
                                ) : customerUsers.length === 0 ? (
                                    <div className="rounded-xl border border-dashed border-slate-800 p-6 text-sm text-slate-500">
                                        No customer users have been created
                                        yet.
                                    </div>
                                ) : (
                                    <div className="space-y-3">
                                        {customerUsers.map(
                                            (user) => (
                                                <div
                                                    key={user.id}
                                                    className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                                                >
                                                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                                                        <div>
                                                            <h4 className="font-semibold text-white">
                                                                {
                                                                    user.full_name
                                                                }
                                                            </h4>

                                                            <p className="mt-1 text-sm text-slate-400">
                                                                {
                                                                    user.email
                                                                }
                                                            </p>

                                                            <p className="mt-2 text-xs font-medium uppercase tracking-wide text-slate-500">
                                                                {
                                                                    user.role
                                                                }
                                                            </p>

                                                            <div className="mt-3">
                                                                <StatusBadge
                                                                    isActive={
                                                                        user.is_active
                                                                    }
                                                                />
                                                            </div>
                                                        </div>


                                                        <button
                                                            type="button"
                                                            disabled={
                                                                updatingUserId ===
                                                                user.id
                                                            }
                                                            onClick={() =>
                                                                void handleUserStatusChange(
                                                                    user,
                                                                )
                                                            }
                                                            className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                                                        >
                                                            {updatingUserId ===
                                                                user.id
                                                                ? "Updating..."
                                                                : user.is_active
                                                                    ? "Deactivate"
                                                                    : "Activate"}
                                                        </button>
                                                    </div>
                                                </div>
                                            ),
                                        )}
                                    </div>
                                )}
                            </div>


                            <div>
                                <h3 className="mb-4 text-lg font-semibold text-white">
                                    Create Customer User
                                </h3>

                                <form
                                    onSubmit={
                                        handleCreateCustomerUser
                                    }
                                    className="space-y-4"
                                >
                                    <TextInput
                                        value={userFullName}
                                        onChange={
                                            setUserFullName
                                        }
                                        placeholder="Full name"
                                    />

                                    <TextInput
                                        value={userEmail}
                                        onChange={
                                            setUserEmail
                                        }
                                        placeholder="Email address"
                                        type="email"
                                    />

                                    <TextInput
                                        value={userPassword}
                                        onChange={
                                            setUserPassword
                                        }
                                        placeholder="Temporary password"
                                        type="password"
                                    />

                                    <select
                                        value={userRole}
                                        onChange={(event) =>
                                            setUserRole(
                                                event.target.value as CustomerUserRole,
                                            )
                                        }
                                        className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                                    >
                                        <option value="AGENT">
                                            Agent
                                        </option>

                                        <option value="SUPERVISOR">
                                            Supervisor
                                        </option>

                                        <option value="ADMIN">
                                            Administrator
                                        </option>
                                    </select>

                                    <p className="text-xs text-slate-500">
                                        Super Admin is a platform-level role
                                        and cannot be created within a
                                        customer organization.
                                    </p>

                                    <PrimaryButton
                                        type="submit"
                                        disabled={
                                            isCreatingUser
                                        }
                                    >
                                        {isCreatingUser
                                            ? "Creating user..."
                                            : "Create customer user"}
                                    </PrimaryButton>
                                </form>
                            </div>

                        </div>
                    </Card>
                </section>

            </div>
        </main>
    );
}


interface TextInputProps {
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    type?: string;
}


function TextInput({
    value,
    onChange,
    placeholder,
    type = "text",
}: TextInputProps) {
    return (
        <input
            type={type}
            value={value}
            onChange={(event) =>
                onChange(event.target.value)
            }
            placeholder={placeholder}
            required
            className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-blue-500"
        />
    );
}


interface PrimaryButtonProps {
    children: string;
    type: "submit";
    disabled: boolean;
}


function PrimaryButton({
    children,
    type,
    disabled,
}: PrimaryButtonProps) {
    return (
        <button
            type={type}
            disabled={disabled}
            className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
            {children}
        </button>
    );
}


function StatusBadge({
    isActive,
}: {
    isActive: boolean;
}) {
    return (
        <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${isActive
                    ? "bg-emerald-950 text-emerald-400"
                    : "bg-slate-800 text-slate-400"
                }`}
        >
            {isActive
                ? "Active"
                : "Inactive"}
        </span>
    );
}


export default CustomerAdministrationPage;