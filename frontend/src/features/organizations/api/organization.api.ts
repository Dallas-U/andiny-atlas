import { apiClient } from "../../../shared/api/client";
import type { OrganizationOverview } from "../types/organization.types";

export async function getOrganizationOverview(): Promise<
    OrganizationOverview[]
> {
    const response = await apiClient.get<
        OrganizationOverview[]
    >("/analytics/organizations/overview");

    return response.data;
}