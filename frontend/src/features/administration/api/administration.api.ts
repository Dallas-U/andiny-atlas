import { apiClient } from "../../../shared/api/client";

import type {
    AdminUser,
    AdminUserListResponse,
    ChangeUserRoleRequest,
    CreateAdminUserRequest,
} from "../types/administration.types";


export async function getAdminUsers(
    page = 1,
    pageSize = 20,
): Promise<AdminUserListResponse> {
    const response =
        await apiClient.get<AdminUserListResponse>(
            "/admin/users",
            {
                params: {
                    page,
                    page_size: pageSize,
                },
            },
        );

    return response.data;
}


export async function getAdminUser(
    userId: string,
): Promise<AdminUser> {
    const response =
        await apiClient.get<AdminUser>(
            `/admin/users/${userId}`,
        );

    return response.data;
}


export async function createAdminUser(
    request: CreateAdminUserRequest,
): Promise<AdminUser> {
    const response =
        await apiClient.post<AdminUser>(
            "/admin/users",
            request,
        );

    return response.data;
}


export async function changeUserRole(
    userId: string,
    request: ChangeUserRoleRequest,
): Promise<AdminUser> {
    const response =
        await apiClient.patch<AdminUser>(
            `/admin/users/${userId}/role`,
            request,
        );

    return response.data;
}


export async function activateUser(
    userId: string,
): Promise<AdminUser> {
    const response =
        await apiClient.post<AdminUser>(
            `/admin/users/${userId}/activate`,
        );

    return response.data;
}


export async function deactivateUser(
    userId: string,
): Promise<AdminUser> {
    const response =
        await apiClient.post<AdminUser>(
            `/admin/users/${userId}/deactivate`,
        );

    return response.data;
}