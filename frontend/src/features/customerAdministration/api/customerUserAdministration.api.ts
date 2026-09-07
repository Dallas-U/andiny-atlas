import { apiClient } from "../../../shared/api/client";

import type {
    CreateCustomerUserRequest,
    CustomerUser,
    UpdateCustomerUserStatusRequest,
} from "../types/customerUserAdministration.types";


export async function listCustomerUsers(
    organizationId: string,
): Promise<CustomerUser[]> {
    const response = await apiClient.get<CustomerUser[]>(
        `/admin/users/organization/${organizationId}`,
    );

    return response.data;
}


export async function createCustomerUser(
    request: CreateCustomerUserRequest,
): Promise<CustomerUser> {
    const response = await apiClient.post<CustomerUser>(
        "/admin/users/",
        request,
    );

    return response.data;
}


export async function updateCustomerUserStatus(
    userId: string,
    request: UpdateCustomerUserStatusRequest,
): Promise<CustomerUser> {
    const response = await apiClient.patch<CustomerUser>(
        `/admin/users/${userId}/status`,
        request,
    );

    return response.data;
}