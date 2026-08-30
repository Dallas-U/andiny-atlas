export interface LoginRequest {
    email: string;
    password: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export type UserRole =
    | "super_admin"
    | "admin"
    | "supervisor"
    | "agent";

export interface CurrentUser {
    id: string;
    full_name: string;
    email: string;
    role: UserRole;
    organization_id: string | null;
    is_active: boolean;
    created_at: string;
}