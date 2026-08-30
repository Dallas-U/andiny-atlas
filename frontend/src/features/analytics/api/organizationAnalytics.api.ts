import type {
    OrganizationAnalytics,
} from "../../organization-analytics/types/organizationAnalytics.types";

const API_BASE = "http://127.0.0.1:8000";

export async function getOrganizationAnalytics(): Promise<
    OrganizationAnalytics[]
> {
    const response = await fetch(
        `${API_BASE}/analytics/organizations`,
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load organization analytics",
        );
    }

    return response.json();
}