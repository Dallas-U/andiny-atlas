import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { useToast } from "../../../shared/feedback/ToastContext";
import { updateCase } from "../api/investigation.api";
import {
    updateCaseSchema,
    type UpdateCaseFormData,
} from "../schema/updateCase.schema";
import type { CaseResponse } from "../types/investigation.types";

interface EditInvestigationFormProps {
    investigation: CaseResponse;
    onUpdated: (investigation: CaseResponse) => void;
}

function EditInvestigationForm({
    investigation,
    onUpdated,
}: EditInvestigationFormProps) {
    const { showToast } = useToast();

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<UpdateCaseFormData>({
        resolver: zodResolver(updateCaseSchema),
        defaultValues: {
            status: investigation.result.status,
            reason: investigation.result.reason,
            next_action: investigation.result.next_action,
        },
    });

    useEffect(() => {
        reset({
            status: investigation.result.status,
            reason: investigation.result.reason,
            next_action: investigation.result.next_action,
        });
    }, [investigation, reset]);

    const onSubmit = async (
        data: UpdateCaseFormData,
    ): Promise<void> => {
        try {
            const updatedInvestigation = await updateCase(
                investigation.case_id,
                data,
            );

            onUpdated(updatedInvestigation);

            showToast({
                type: "success",
                message: "Investigation updated successfully.",
            });
        } catch (error) {
            console.error("Failed to update investigation:", error);

            showToast({
                type: "error",
                message: "Unable to update the investigation. Please try again.",
            });
        }
    };

    return (
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Update Investigation
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Change the current status, reason, and next action for this case.
                </p>
            </div>

            <form
                onSubmit={handleSubmit(onSubmit)}
                className="mt-6 space-y-6"
            >
                <div>
                    <label
                        htmlFor="status"
                        className="mb-2 block text-sm font-medium text-slate-200"
                    >
                        Status
                    </label>

                    <select
                        id="status"
                        {...register("status")}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-slate-500"
                    >
                        <option value="Resolved">Resolved</option>
                        <option value="Waiting">Waiting</option>
                        <option value="Technical Investigation">
                            Technical Investigation
                        </option>
                        <option value="Escalated">Escalated</option>
                    </select>

                    {errors.status && (
                        <p className="mt-2 text-sm text-red-400">
                            {errors.status.message}
                        </p>
                    )}
                </div>

                <div>
                    <label
                        htmlFor="reason"
                        className="mb-2 block text-sm font-medium text-slate-200"
                    >
                        Reason
                    </label>

                    <textarea
                        id="reason"
                        rows={5}
                        maxLength={500}
                        {...register("reason")}
                        className="w-full resize-y rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                    />

                    {errors.reason && (
                        <p className="mt-2 text-sm text-red-400">
                            {errors.reason.message}
                        </p>
                    )}
                </div>

                <div>
                    <label
                        htmlFor="next_action"
                        className="mb-2 block text-sm font-medium text-slate-200"
                    >
                        Next action
                    </label>

                    <textarea
                        id="next_action"
                        rows={5}
                        maxLength={500}
                        {...register("next_action")}
                        className="w-full resize-y rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                    />

                    {errors.next_action && (
                        <p className="mt-2 text-sm text-red-400">
                            {errors.next_action.message}
                        </p>
                    )}
                </div>

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full rounded-lg bg-white px-4 py-3 font-semibold text-slate-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {isSubmitting ? "Saving changes..." : "Save changes"}
                </button>
            </form>
        </section>
    );
}

export default EditInvestigationForm;