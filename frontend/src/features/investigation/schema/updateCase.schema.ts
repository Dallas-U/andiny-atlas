import { z } from "zod";

export const updateCaseSchema = z.object({
    status: z.enum([
        "Resolved",
        "Waiting",
        "Technical Investigation",
        "Escalated",
    ]),

    reason: z
        .string()
        .trim()
        .min(1, "Reason is required.")
        .max(500, "Reason cannot exceed 500 characters."),

    next_action: z
        .string()
        .trim()
        .min(1, "Next action is required.")
        .max(500, "Next action cannot exceed 500 characters."),
});

export type UpdateCaseFormData =
    z.infer<typeof updateCaseSchema>;