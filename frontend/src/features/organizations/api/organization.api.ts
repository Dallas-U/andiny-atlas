import { apiClient } from "../../../shared/api/client";

import type {
    Organization,
    OrganizationOverview,
    OnboardedOrganizationResponse,
    ProvisionCustomerOrganizationRequest,
} from "../types/organization.types";


export async function getOrganizationOverview(): Promise<
    OrganizationOverview[]
> {
    const response = await apiClient.get<
        OrganizationOverview[]
    >("/analytics/organizations/overview");

    return response.data;
}


export async function listOrganizations(): Promise<
    Organization[]
> {
    const response = await apiClient.get<
        Organization[]
    >("/organizations/");

    return response.data;
}


export async function getOrganization(
    organizationId: string,
): Promise<Organization> {
    const response = await apiClient.get<Organization>(
        `/organizations/${organizationId}`,
    );

    return response.data;
}


export async function provisionCustomerOrganization(
    request: ProvisionCustomerOrganizationRequest,
): Promise<OnboardedOrganizationResponse> {
    const response =
        await apiClient.post<OnboardedOrganizationResponse>(
            "/onboarding/organizations",
            request,
        );

    return response.data;
}