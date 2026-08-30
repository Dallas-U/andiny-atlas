import { z } from "zod";

export const reportFilterSchema = z
    .object({
        start_date: z
            .string()
            .min(1, "Start date is required."),

        end_date: z
            .string()
            .min(1, "End date is required."),

        status: z
            .enum([
                "Resolved",
                "Waiting",
                "Technical Investigation",
                "Escalated",
            ])
            .optional(),
    })
    .refine(
        (values) => values.end_date >= values.start_date,
        {
            message:
                "End date must be on or after the start date.",
            path: ["end_date"],
        },
    );

export type ReportFilterFormData =
    z.infer<typeof reportFilterSchema>;