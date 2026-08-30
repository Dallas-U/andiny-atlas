import { apiClient } from "../../../shared/api/client";

export interface EnterpriseKpis {
    total_cases: number;
    resolved_cases: number;
    waiting_cases: number;
    technical_investigation_cases: number;
    escalated_cases: number;
    resolution_rate: number;
    escalation_rate: number;
}

export interface EnterpriseAnalyticsResponse {
    organization_id: string;
    kpis: EnterpriseKpis;
}

export interface BranchAnalytics {
    branch_id: string;
    branch_name: string;
    total_cases: number;
    resolved_cases: number;
    escalation_rate: number;
}

export interface BranchAnalyticsResponse {
    organization_id: string;
    branches: BranchAnalytics[];
}

export interface DepartmentAnalytics {
    department_id: string;
    department_name: string;
    total_cases: number;
    resolved_cases: number;
    escalation_rate: number;
}

export interface DepartmentAnalyticsResponse {
    branch_id: string;
    departments: DepartmentAnalytics[];
}

/**
 * Get executive-level analytics for an organization.
 */
export async function getEnterpriseAnalytics(
    organizationId: string,
): Promise<EnterpriseAnalyticsResponse> {
    const response =
        await apiClient.get<EnterpriseAnalyticsResponse>(
            `/enterprise-analytics/organization/${organizationId}`,
        );

    return response.data;
}

/**
 * Get branch-level analytics for an organization.
 */
export async function getBranchAnalytics(
    organizationId: string,
): Promise<BranchAnalyticsResponse> {
    const response =
        await apiClient.get<BranchAnalyticsResponse>(
            `/enterprise-analytics/organization/${organizationId}/branches`,
        );

    return response.data;
}

/**
 * Get department-level analytics for a branch.
 */
export async function getDepartmentAnalytics(
    branchId: string,
): Promise<DepartmentAnalyticsResponse> {
    const response =
        await apiClient.get<DepartmentAnalyticsResponse>(
            `/enterprise-analytics/branch/${branchId}/departments`,
        );

    return response.data;
}