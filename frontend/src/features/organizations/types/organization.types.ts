export interface OrganizationOverview {
    organization: string;
    total_cases: number;
    resolved_cases: number;
    escalated_cases: number;
    resolution_rate: number;
}