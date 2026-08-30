import { z } from "zod";

export const investigationSchema = z.object({
    customer_name: z
        .string()
        .min(2, "Customer name must contain at least 2 characters.")
        .max(100, "Customer name must not exceed 100 characters."),

    phone_number: z
        .string()
        .min(7, "Phone number is too short.")
        .max(20, "Phone number is too long."),

    country: z
        .string()
        .min(2, "Country is required.")
        .max(50, "Country must not exceed 50 characters."),

    payment_verified: z.boolean(),
    extension_triggered: z.boolean(),
    api_success: z.boolean(),
    skg_success: z.boolean(),
    device_online: z.boolean(),
    sim_slot_one: z.boolean(),
    mobile_data_on: z.boolean(),
});

export type InvestigationFormData =
    z.infer<typeof investigationSchema>;