export type UserRole =
    | "super_admin"
    | "admin"
    | "supervisor"
    | "agent";


export interface AdminUser {
    id: string;
    full_name: string;
    email: string;
    role: UserRole;
    organization_id: string | null;
    is_active: boolean;
    created_at: string;
}


export interface AdminUserListResponse {
    users: AdminUser[];
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
}


export interface CreateAdminUserRequest {
    full_name: string;
    email: string;
    password: string;
    role?: UserRole;
    organization_id?: string;
}


export interface ChangeUserRoleRequest {
    role: UserRole;
}