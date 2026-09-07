import {
    useState,
    type FormEvent,
} from "react";

import {
    provisionCustomerOrganization,
} from "../api/organization.api";

import type {
    ProvisionCustomerOrganizationRequest,
} from "../types/organization.types";


interface OrganizationProvisioningFormProps {
    onSuccess: () => Promise<void> | void;
}


const initialForm: ProvisionCustomerOrganizationRequest = {
    organization_name: "",
    organization_code: "",
    industry: "",
    contact_email: "",
    admin_full_name: "",
    admin_email: "",
    admin_password: "",
};


function OrganizationProvisioningForm({
    onSuccess,
}: OrganizationProvisioningFormProps) {
    const [form, setForm] = useState(initialForm);

    const [isSubmitting, setIsSubmitting] =
        useState(false);

    const [error, setError] =
        useState<string | null>(null);

    const [success, setSuccess] =
        useState<string | null>(null);


    function updateField(
        field: keyof ProvisionCustomerOrganizationRequest,
        value: string,
    ): void {
        setForm((current) => ({
            ...current,
            [field]: value,
        }));
    }


    async function handleSubmit(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        setError(null);
        setSuccess(null);
        setIsSubmitting(true);

        try {
            const response =
                await provisionCustomerOrganization(form);

            setSuccess(
                `Organization "${response.organization_name}" was successfully provisioned with administrator ${response.admin_email}.`,
            );

            setForm(initialForm);

            await onSuccess();
        } catch (requestError) {
            console.error(
                "Failed to provision customer organization:",
                requestError,
            );

            setError(
                "Unable to provision the organization. Please verify the information and try again.",
            );
        } finally {
            setIsSubmitting(false);
        }
    }


    return (
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-6">
                <h2 className="text-lg font-semibold text-white">
                    Provision Customer Organization
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Create a new customer tenant and its initial
                    Customer Administrator.
                </p>
            </div>


            {error && (
                <div className="mb-5 rounded-lg border border-red-900 bg-red-950/40 px-4 py-3 text-sm text-red-300">
                    {error}
                </div>
            )}


            {success && (
                <div className="mb-5 rounded-lg border border-emerald-900 bg-emerald-950/40 px-4 py-3 text-sm text-emerald-300">
                    {success}
                </div>
            )}


            <form
                onSubmit={handleSubmit}
                className="space-y-8"
            >
                <div>
                    <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
                        Organization
                    </h3>

                    <div className="mt-4 grid gap-5 md:grid-cols-2">
                        <Field
                            label="Organization name"
                            value={form.organization_name}
                            onChange={(value) =>
                                updateField(
                                    "organization_name",
                                    value,
                                )
                            }
                            required
                        />

                        <Field
                            label="Organization code"
                            value={form.organization_code}
                            onChange={(value) =>
                                updateField(
                                    "organization_code",
                                    value,
                                )
                            }
                            required
                        />

                        <Field
                            label="Industry"
                            value={form.industry}
                            onChange={(value) =>
                                updateField(
                                    "industry",
                                    value,
                                )
                            }
                            required
                        />

                        <Field
                            label="Contact email"
                            type="email"
                            value={form.contact_email}
                            onChange={(value) =>
                                updateField(
                                    "contact_email",
                                    value,
                                )
                            }
                            required
                        />
                    </div>
                </div>


                <div>
                    <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
                        Initial Customer Administrator
                    </h3>

                    <div className="mt-4 grid gap-5 md:grid-cols-2">
                        <Field
                            label="Full name"
                            value={form.admin_full_name}
                            onChange={(value) =>
                                updateField(
                                    "admin_full_name",
                                    value,
                                )
                            }
                            required
                        />

                        <Field
                            label="Email"
                            type="email"
                            value={form.admin_email}
                            onChange={(value) =>
                                updateField(
                                    "admin_email",
                                    value,
                                )
                            }
                            required
                        />

                        <Field
                            label="Initial password"
                            type="password"
                            value={form.admin_password}
                            onChange={(value) =>
                                updateField(
                                    "admin_password",
                                    value,
                                )
                            }
                            required
                        />
                    </div>
                </div>


                <div className="flex justify-end border-t border-slate-800 pt-6">
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        className="rounded-lg bg-white px-5 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {isSubmitting
                            ? "Provisioning..."
                            : "Provision Organization"}
                    </button>
                </div>
            </form>
        </section>
    );
}


interface FieldProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    type?: string;
    required?: boolean;
}


function Field({
    label,
    value,
    onChange,
    type = "text",
    required = false,
}: FieldProps) {
    return (
        <label className="block">
            <span className="text-sm font-medium text-slate-300">
                {label}
            </span>

            <input
                type={type}
                value={value}
                onChange={(event) =>
                    onChange(event.target.value)
                }
                required={required}
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-2.5 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-slate-500"
            />
        </label>
    );
}


export default OrganizationProvisioningForm;