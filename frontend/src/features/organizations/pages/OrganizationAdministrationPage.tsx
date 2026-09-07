import { useEffect, useState } from "react";

import BackButton from "../../../shared/components/BackButton";
import Card from "../../../shared/components/Card";
import LoadingSkeleton from "../../../shared/components/LoadingSkeleton";
import PageHeader from "../../../shared/components/PageHeader";

import OrganizationProvisioningForm from "../components/OrganizationProvisioningForm";
import { listOrganizations } from "../api/organization.api";

import type {
    Organization,
} from "../types/organization.types";


function OrganizationAdministrationPage() {
    const [
        organizations,
        setOrganizations,
    ] = useState<Organization[]>([]);

    const [
        isLoading,
        setIsLoading,
    ] = useState(true);

    async function loadOrganizations(): Promise<void> {
        setIsLoading(true);

        try {
            const response =
                await listOrganizations();

            setOrganizations(response);
        } catch (error) {
            console.error(
                "Failed to load organizations:",
                error,
            );
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        void loadOrganizations();
    }, []);


    return (
        <main className="min-h-screen bg-slate-950 px-10 py-8">
            <div className="mx-auto max-w-7xl">
                <div className="mb-6">
                    <BackButton />
                </div>

                <PageHeader
                    title="Organization Administration"
                    description="Platform-level customer organization provisioning and tenant management."
                />


                <div className="mt-8">
                    <OrganizationProvisioningForm
                        onSuccess={loadOrganizations}
                    />
                </div>


                <div className="mt-8">
                    {isLoading ? (
                        <LoadingSkeleton />
                    ) : (
                        <Card className="overflow-hidden">
                            <div className="border-b border-slate-800 px-6 py-4">
                                <h2 className="text-lg font-semibold text-white">
                                    Customer Organizations
                                </h2>

                                <p className="mt-1 text-sm text-slate-400">
                                    Organizations currently registered on the platform.
                                </p>
                            </div>


                            <div className="overflow-x-auto">
                                <table className="min-w-full divide-y divide-slate-800">
                                    <thead className="bg-slate-900">
                                        <tr>
                                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                Organization
                                            </th>

                                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                Code
                                            </th>

                                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                Industry
                                            </th>

                                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                Contact
                                            </th>

                                            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-400">
                                                Status
                                            </th>
                                        </tr>
                                    </thead>


                                    <tbody className="divide-y divide-slate-800 bg-slate-950">
                                        {organizations.map(
                                            (organization) => (
                                                <tr
                                                    key={
                                                        organization.organization_id
                                                    }
                                                >
                                                    <td className="px-6 py-4 text-sm font-medium text-white">
                                                        {
                                                            organization.name
                                                        }
                                                    </td>

                                                    <td className="px-6 py-4 text-sm text-slate-300">
                                                        {
                                                            organization.code
                                                        }
                                                    </td>

                                                    <td className="px-6 py-4 text-sm text-slate-300">
                                                        {
                                                            organization.industry
                                                        }
                                                    </td>

                                                    <td className="px-6 py-4 text-sm text-slate-300">
                                                        {
                                                            organization.contact_email
                                                        }
                                                    </td>

                                                    <td className="px-6 py-4 text-sm">
                                                        <span
                                                            className={
                                                                organization.is_active
                                                                    ? "text-emerald-400"
                                                                    : "text-red-400"
                                                            }
                                                        >
                                                            {organization.is_active
                                                                ? "Active"
                                                                : "Inactive"}
                                                        </span>
                                                    </td>
                                                </tr>
                                            ),
                                        )}

                                        {organizations.length === 0 && (
                                            <tr>
                                                <td
                                                    colSpan={5}
                                                    className="px-6 py-10 text-center text-sm text-slate-500"
                                                >
                                                    No customer organizations have been provisioned yet.
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </Card>
                    )}
                </div>
            </div>
        </main>
    );
}


export default OrganizationAdministrationPage;