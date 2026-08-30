import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { investigate } from "../api/investigation.api";
import {
    investigationSchema,
    type InvestigationFormData,
} from "../schema/investigation.schema";
import type { CaseResponse } from "../types/investigation.types";
import InvestigationResultCard from "./InvestigationResultCard";

const checklistItems = [
    {
        name: "payment_verified",
        label: "Payment verified",
        description: "Confirm that the customer’s payment has been verified.",
    },
    {
        name: "extension_triggered",
        label: "Extension triggered",
        description: "Confirm whether the required extension was triggered.",
    },
    {
        name: "api_success",
        label: "API successful",
        description: "Confirm that the relevant API request completed successfully.",
    },
    {
        name: "skg_success",
        label: "SKG successful",
        description: "Confirm that the SKG verification completed successfully.",
    },
    {
        name: "device_online",
        label: "Device online",
        description: "Confirm that the customer’s device is currently online.",
    },
    {
        name: "sim_slot_one",
        label: "SIM in slot one",
        description: "Confirm that the SIM is installed in the first SIM slot.",
    },
    {
        name: "mobile_data_on",
        label: "Mobile data enabled",
        description: "Confirm that mobile data is enabled on the device.",
    },
] as const;

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
        try {
            const investigation = await investigate(data);

            setCompletedInvestigation(investigation);
        } catch (error) {
            console.error("Investigation failed:", error);
        }
    };

    function handleStartAnother(): void {
        setCompletedInvestigation(null);
        reset(defaultValues);
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
            <section>
                <div>
                    <h2 className="text-lg font-semibold text-white">
                        Customer information
                    </h2>

                    <p className="mt-1 text-sm text-slate-400">
                        Enter the customer details associated with this support case.
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
                        Record the diagnostic checks completed during the investigation.
                    </p>
                </div>

                <div className="mt-5 space-y-3">
                    {checklistItems.map((item) => (
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
                disabled={isSubmitting}
                className="w-full rounded-lg bg-white px-4 py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
                {isSubmitting ? "Investigating..." : "Start investigation"}
            </button>
        </form>
    );
}

export default NewInvestigationForm;