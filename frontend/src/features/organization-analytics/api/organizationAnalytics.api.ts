import type {
    OrganizationAnalytics,
} from "../types/organizationAnalytics.types";


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


const API_BASE = "http://127.0.0.1:8000";


export async function getEnterpriseAnalytics(
    organizationId: string,
): Promise<EnterpriseAnalyticsResponse> {
    const response = await fetch(
        `${API_BASE}/enterprise-analytics/organization/${organizationId}`,
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load enterprise analytics",
        );
    }

    return response.json();
}


export async function getBranchAnalytics(
    organizationId: string,
): Promise<BranchAnalyticsResponse> {
    const response = await fetch(
        `${API_BASE}/enterprise-analytics/organization/${organizationId}/branches`,
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load branch analytics",
        );
    }

    return response.json();
}


export async function getDepartmentAnalytics(
    branchId: string,
): Promise<DepartmentAnalyticsResponse> {
    const response = await fetch(
        `${API_BASE}/enterprise-analytics/branch/${branchId}/departments`,
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load department analytics",
        );
    }

    return response.json();
}


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