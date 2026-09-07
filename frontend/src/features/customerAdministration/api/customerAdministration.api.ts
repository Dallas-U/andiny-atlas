import { apiClient } from "../../../shared/api/client";

import type {
    Branch,
    CreateBranchRequest,
    CreateDepartmentRequest,
    Department,
} from "../types/customerAdministration.types";


export async function listBranches(
    organizationId: string,
): Promise<Branch[]> {
    const response = await apiClient.get<Branch[]>(
        `/branches/organization/${organizationId}`,
    );

    return response.data;
}


export async function createBranch(
    request: CreateBranchRequest,
): Promise<Branch> {
    const response = await apiClient.post<Branch>(
        "/branches/",
        request,
    );

    return response.data;
}


export async function listDepartments(
    branchId: string,
): Promise<Department[]> {
    const response = await apiClient.get<Department[]>(
        `/departments/branch/${branchId}`,
    );

    return response.data;
}


export async function createDepartment(
    request: CreateDepartmentRequest,
): Promise<Department> {
    const response =
        await apiClient.post<Department>(
            "/departments/",
            request,
        );

    return response.data;
}