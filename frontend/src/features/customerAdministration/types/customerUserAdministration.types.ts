export type CustomerUserRole =
    | "AGENT"
    | "SUPERVISOR"
    | "ADMIN";


export interface CustomerUser {
    id: string;
    full_name: string;
    email: string;
    role: CustomerUserRole;
    organization_id: string | null;
    is_active: boolean;
    created_at: string;
}


export interface CreateCustomerUserRequest {
    organization_id: string;
    full_name: string;
    email: string;
    password: string;
    role: CustomerUserRole;
}


export interface UpdateCustomerUserStatusRequest {
    is_active: boolean;
}