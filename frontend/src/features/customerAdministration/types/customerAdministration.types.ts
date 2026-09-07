export interface Branch {
    branch_id: string;
    organization_id: string;
    name: string;
    code: string;
    city: string;
    state: string;
    is_active: boolean;
}

export interface CreateBranchRequest {
    organization_id: string;
    name: string;
    code: string;
    city: string;
    state: string;
}

export interface Department {
    department_id: string;
    organization_id: string;
    branch_id: string;
    name: string;
    code: string;
    is_active: boolean;
}

export interface CreateDepartmentRequest {
    organization_id: string;
    branch_id: string;
    name: string;
    code: string;
}