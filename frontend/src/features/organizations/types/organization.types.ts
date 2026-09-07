export interface OrganizationOverview {
    organization: string;
    total_cases: number;
    resolved_cases: number;
    escalated_cases: number;
    resolution_rate: number;
}

export interface Organization {
    organization_id: string;
    name: string;
    code: string;
    industry: string;
    contact_email: string;
    is_active: boolean;
}

export interface CreateOrganizationRequest {
    name: string;
    code: string;
    industry: string;
    contact_email: string;
}

export interface ProvisionCustomerOrganizationRequest {
    organization_name: string;
    organization_code: string;
    industry: string;
    contact_email: string;
    admin_full_name: string;
    admin_email: string;
    admin_password: string;
}

export interface OnboardedOrganizationResponse {
    organization_id: string;
    organization_name: string;
    organization_code: string;
    industry: string;
    contact_email: string;
    organization_is_active: boolean;

    admin_user_id: string;
    admin_full_name: string;
    admin_email: string;
    admin_role: "admin";
    admin_organization_id: string;
    admin_is_active: boolean;
    admin_created_at: string;
}