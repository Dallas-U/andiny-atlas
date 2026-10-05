import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { useAuth } from "../../../shared/auth/AuthContext";
import { investigate } from "../api/investigation.api";
import {
    investigationSchema,
    type InvestigationFormData,
} from "../schema/investigation.schema";
import type {
    CaseResponse,
    DemoScenarioKey,
} from "../types/investigation.types";
import InvestigationResultCard from "./InvestigationResultCard";

const DEMO_SCENARIOS: Record<
    DemoScenarioKey,
    {
        label: string;
        description: string;
        customerName: string;
        reference: string;
        checklist: Array<{
            name: keyof InvestigationFormData;
            label: string;
            description: string;
        }>;
        values: Omit<
            InvestigationFormData,
            "customer_name" | "phone_number" | "country"
        >;
    }
> = {
    payments: {
        label: "Payment / merchant exception",
        description:
            "Representative of payment, merchant and transaction-exception operations.",
        customerName: "Demo Merchant — TX-20492",
        reference: "Transaction TX-20492",
        checklist: [
            {
                name: "payment_verified",
                label: "Payment verified",
                description: "Confirm the transaction/payment record.",
            },
            {
                name: "extension_triggered",
                label: "Exception workflow triggered",
                description:
                    "Confirm whether the exception workflow was triggered.",
            },
            {
                name: "api_success",
                label: "Transaction service successful",
                description:
                    "Confirm the relevant transaction service completed successfully.",
            },
            {
                name: "skg_success",
                label: "Verification completed",
                description: "Confirm the required verification completed.",
            },
            {
                name: "device_online",
                label: "Channel available",
                description:
                    "Confirm the relevant service channel is available.",
            },
            {
                name: "sim_slot_one",
                label: "Account/channel identified",
                description:
                    "Confirm the account or channel is correctly identified.",
            },
            {
                name: "mobile_data_on",
                label: "Required service enabled",
                description: "Confirm the required service is enabled.",
            },
        ],
        values: {
            payment_verified: true,
            extension_triggered: true,
            api_success: false,
            skg_success: false,
            device_online: false,
            sim_slot_one: false,
            mobile_data_on: false,
        },
    },

    lending: {
        label: "Loan / repayment exception",
        description:
            "Representative of lending, repayment and borrower-service operations.",
        customerName: "Demo Borrower — LN-38117",
        reference: "Loan LN-38117",
        checklist: [
            {
                name: "payment_verified",
                label: "Repayment verified",
                description:
                    "Confirm the repayment record and amount.",
            },
            {
                name: "extension_triggered",
                label: "Repayment exception triggered",
                description:
                    "Confirm whether the exception workflow was triggered.",
            },
            {
                name: "api_success",
                label: "Account service successful",
                description:
                    "Confirm the relevant account service completed successfully.",
            },
            {
                name: "skg_success",
                label: "Verification completed",
                description:
                    "Confirm the required borrower verification completed.",
            },
            {
                name: "device_online",
                label: "Customer channel available",
                description:
                    "Confirm the relevant customer service channel is available.",
            },
            {
                name: "sim_slot_one",
                label: "Loan account identified",
                description:
                    "Confirm the correct loan/account record is identified.",
            },
            {
                name: "mobile_data_on",
                label: "Required service enabled",
                description:
                    "Confirm the required service is enabled.",
            },
        ],
        values: {
            payment_verified: false,
            extension_triggered: true,
            api_success: true,
            skg_success: false,
            device_online: true,
            sim_slot_one: true,
            mobile_data_on: true,
        },
    },

    recovery: {
        label: "Borrower / recovery case",
        description:
            "Representative of borrower recovery and complex account-resolution operations.",
        customerName: "Demo Borrower — RC-7814",
        reference: "Recovery RC-7814",
        checklist: [
            {
                name: "payment_verified",
                label: "Account/payment history verified",
                description: "Confirm the relevant payment history.",
            },
            {
                name: "extension_triggered",
                label: "Recovery workflow triggered",
                description:
                    "Confirm whether the recovery workflow was triggered.",
            },
            {
                name: "api_success",
                label: "Account service successful",
                description:
                    "Confirm the relevant account service completed successfully.",
            },
            {
                name: "skg_success",
                label: "Identity verification completed",
                description:
                    "Confirm the required verification completed.",
            },
            {
                name: "device_online",
                label: "Customer channel available",
                description:
                    "Confirm the relevant customer channel is available.",
            },
            {
                name: "sim_slot_one",
                label: "Account identified",
                description:
                    "Confirm the correct borrower/account record is identified.",
            },
            {
                name: "mobile_data_on",
                label: "Required service enabled",
                description:
                    "Confirm the required service is enabled.",
            },
        ],
        values: {
            payment_verified: true,
            extension_triggered: true,
            api_success: true,
            skg_success: true,
            device_online: true,
            sim_slot_one: true,
            mobile_data_on: false,
        },
    },

    claims: {
        label: "Insurance claims exception",
        description:
            "Representative of claims intake, validation and resolution operations.",
        customerName: "Demo Policyholder — CL-20418",
        reference: "Claim CL-20418",
        checklist: [
            {
                name: "payment_verified",
                label: "Claim/payment record verified",
                description:
                    "Confirm the relevant claim or payment record.",
            },
            {
                name: "extension_triggered",
                label: "Claims review triggered",
                description:
                    "Confirm whether additional review was triggered.",
            },
            {
                name: "api_success",
                label: "Policy service successful",
                description:
                    "Confirm the relevant policy service completed successfully.",
            },
            {
                name: "skg_success",
                label: "Claim verification completed",
                description:
                    "Confirm the required claim verification completed.",
            },
            {
                name: "device_online",
                label: "Service channel available",
                description:
                    "Confirm the relevant service channel is available.",
            },
            {
                name: "sim_slot_one",
                label: "Policy identified",
                description:
                    "Confirm the correct policy/claim record is identified.",
            },
            {
                name: "mobile_data_on",
                label: "Required service enabled",
                description:
                    "Confirm the required service is enabled.",
            },
        ],
        values: {
            payment_verified: true,
            extension_triggered: true,
            api_success: true,
            skg_success: false,
            device_online: true,
            sim_slot_one: true,
            mobile_data_on: true,
        },
    },

    delivery: {
        label: "Delivery exception",
        description:
            "Representative of failed, delayed or exception-based delivery operations.",
        customerName: "Demo Shipment — SH-58291",
        reference: "Shipment SH-58291",
        checklist: [
            {
                name: "payment_verified",
                label: "Order/payment verified",
                description:
                    "Confirm the relevant order or payment record.",
            },
            {
                name: "extension_triggered",
                label: "Delivery exception triggered",
                description:
                    "Confirm whether the delivery exception workflow was triggered.",
            },
            {
                name: "api_success",
                label: "Tracking service successful",
                description:
                    "Confirm the relevant tracking service completed successfully.",
            },
            {
                name: "skg_success",
                label: "Delivery verification completed",
                description:
                    "Confirm the required delivery verification completed.",
            },
            {
                name: "device_online",
                label: "Delivery channel available",
                description:
                    "Confirm the relevant operational channel is available.",
            },
            {
                name: "sim_slot_one",
                label: "Shipment identified",
                description:
                    "Confirm the correct shipment/order record is identified.",
            },
            {
                name: "mobile_data_on",
                label: "Required service enabled",
                description:
                    "Confirm the required service is enabled.",
            },
        ],
        values: {
            payment_verified: true,
            extension_triggered: true,
            api_success: false,
            skg_success: true,
            device_online: true,
            sim_slot_one: true,
            mobile_data_on: true,
        },
    },
};

const defaultValues: InvestigationFormData = {
    customer_name: "",
    phone_number: "",
    country: "",
    payment_verified: false,
    extension_triggered: false,
    api_success: false,
    skg_success: false,
    device_online: false,
    sim_slot_one: false,
    mobile_data_on: false,
};

function NewInvestigationForm() {
    const [completedInvestigation, setCompletedInvestigation] =
        useState<CaseResponse | null>(null);

    const [demoScenario, setDemoScenario] =
        useState<DemoScenarioKey>("payments");

    const { currentUser } = useAuth();

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<InvestigationFormData>({
        resolver: zodResolver(investigationSchema),
        defaultValues,
    });

    const onSubmit = async (
        data: InvestigationFormData,
    ): Promise<void> => {
        if (!currentUser?.organization_id) {
            console.error(
                "Investigation failed: authenticated user has no organization.",
            );
            return;
        }

        try {
            const investigation = await investigate({
                ...data,
                organization_id: currentUser.organization_id,
                demo_scenario: demoScenario,
            });

            setCompletedInvestigation(investigation);
        } catch (error) {
            console.error("Investigation failed:", error);
        }
    };

    function handleStartAnother(): void {
        setCompletedInvestigation(null);
        reset(defaultValues);
    }

    function loadDemoScenario(): void {
        const scenario = DEMO_SCENARIOS[demoScenario];

        reset({
            customer_name: scenario.customerName,
            phone_number: "08000000000",
            country: "Nigeria",
            ...scenario.values,
        });
    }

    if (completedInvestigation) {
        return (
            <InvestigationResultCard
                investigation={completedInvestigation}
                onStartAnother={handleStartAnother}
            />
        );
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-8 rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
            <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-4">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <p className="text-sm font-semibold text-amber-200">
                            Controlled prospect demonstration
                        </p>

                        <p className="mt-1 text-sm leading-6 text-amber-100/70">
                            Choose a synthetic scenario that is closest to the
                            prospect&apos;s operating environment. This controlled
                            demo uses the existing Atlas investigation structure
                            with neutral demonstration checks; customer-specific
                            rules and integrations are configured after discovery.
                        </p>
                    </div>

                    <div className="flex shrink-0 flex-col gap-2 sm:items-end">
                        <select
                            value={demoScenario}
                            onChange={(event) =>
                                setDemoScenario(
                                    event.target.value as DemoScenarioKey,
                                )
                            }
                            className="rounded-lg border border-amber-300/30 bg-slate-950 px-3 py-2 text-sm font-medium text-amber-100 outline-none"
                            aria-label="Prospect demonstration scenario"
                        >
                            {Object.entries(DEMO_SCENARIOS).map(
                                ([key, scenario]) => (
                                    <option key={key} value={key}>
                                        {scenario.label}
                                    </option>
                                ),
                            )}
                        </select>

                        <p className="text-xs text-amber-100/60">
                            {DEMO_SCENARIOS[demoScenario].reference}
                        </p>

                        <button
                            type="button"
                            onClick={loadDemoScenario}
                            className="rounded-lg border border-amber-300/30 bg-slate-950 px-4 py-2 text-sm font-semibold text-amber-200 transition hover:bg-slate-900"
                        >
                            Load selected scenario
                        </button>
                    </div>
                </div>
            </div>

            <section>
                <div>
                    <h2 className="text-lg font-semibold text-white">
                        Customer information
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        Enter the customer details associated with this support
                        case.
                    </p>
                </div>

                <div className="mt-5 space-y-5">
                    <div>
                        <label
                            htmlFor="customer_name"
                            className="mb-2 block text-sm font-medium text-slate-200"
                        >
                            Customer name
                        </label>

                        <input
                            id="customer_name"
                            type="text"
                            autoComplete="name"
                            placeholder="Enter the customer's full name"
                            {...register("customer_name")}
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                        />

                        {errors.customer_name && (
                            <p className="mt-2 text-sm text-red-400">
                                {errors.customer_name.message}
                            </p>
                        )}
                    </div>

                    <div>
                        <label
                            htmlFor="phone_number"
                            className="mb-2 block text-sm font-medium text-slate-200"
                        >
                            Phone number
                        </label>

                        <input
                            id="phone_number"
                            type="tel"
                            autoComplete="tel"
                            placeholder="Enter the customer's phone number"
                            {...register("phone_number")}
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                        />

                        {errors.phone_number && (
                            <p className="mt-2 text-sm text-red-400">
                                {errors.phone_number.message}
                            </p>
                        )}
                    </div>

                    <div>
                        <label
                            htmlFor="country"
                            className="mb-2 block text-sm font-medium text-slate-200"
                        >
                            Country
                        </label>

                        <input
                            id="country"
                            type="text"
                            autoComplete="country-name"
                            placeholder="Enter the customer's country"
                            {...register("country")}
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                        />

                        {errors.country && (
                            <p className="mt-2 text-sm text-red-400">
                                {errors.country.message}
                            </p>
                        )}
                    </div>
                </div>
            </section>

            <section className="border-t border-slate-800 pt-8">
                <div>
                    <h2 className="text-lg font-semibold text-white">
                        Investigation checklist
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        Record the synthetic investigation checks used by this
                        demonstration scenario.
                    </p>
                </div>

                <div className="mt-5 space-y-3">
                    {DEMO_SCENARIOS[demoScenario].checklist.map((item) => (
                        <label
                            key={item.name}
                            className="flex cursor-pointer items-start gap-4 rounded-lg border border-slate-800 bg-slate-950 p-4"
                        >
                            <input
                                type="checkbox"
                                {...register(item.name)}
                                className="mt-1 h-4 w-4 rounded border-slate-600"
                            />

                            <span>
                                <span className="block text-sm font-medium text-slate-200">
                                    {item.label}
                                </span>

                                <span className="mt-1 block text-sm text-slate-500">
                                    {item.description}
                                </span>
                            </span>
                        </label>
                    ))}
                </div>
            </section>

            <button
                type="submit"
                disabled={
                    isSubmitting ||
                    !currentUser?.organization_id
                }
                className="w-full rounded-lg bg-white px-4 py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting
                    ? "Investigating..."
                    : "Start investigation"}
            </button>
        </form>
    );
}

export default NewInvestigationForm;