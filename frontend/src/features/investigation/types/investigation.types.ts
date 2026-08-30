export type InvestigationStatus =
    | "Resolved"
    | "Waiting"
    | "Technical Investigation"
    | "Escalated";

export interface SupportCase {
    customer_name: string;
    phone_number: string;
    country: string;
    payment_verified: boolean;
    extension_triggered: boolean;
    api_success: boolean;
    skg_success: boolean;
    device_online: boolean;
    sim_slot_one: boolean;
    mobile_data_on: boolean;
}

export interface InvestigationResult {
    status: InvestigationStatus;
    reason: string;
    next_action: string;
}

export interface CaseResponse {
    case_id: string;
    timestamp: string;
    customer_name: string;
    phone_number: string;
    created_by: string;

    organization_id?: string | null;
    branch_id?: string | null;
    department_id?: string | null;

    result: InvestigationResult;
}

export interface PaginationMetadata {
    page: number;
    page_size: number;
    total_records: number;
    total_pages: number;
    returned_records: number;
}

export interface PaginatedResponse<T> {
    metadata: PaginationMetadata;
    items: T[];
}

export type PaginatedCasesResponse =
    PaginatedResponse<CaseResponse>;

export type SortOrder = "asc" | "desc";

export type CaseSortField =
    | "timestamp"
    | "customer_name"
    | "phone_number"
    | "status"
    | "created_by";

export interface CaseQuery {
    page?: number;
    page_size?: number;
    customer_name?: string;
    phone_number?: string;
    created_by?: string;

    organization_id?: string;
    branch_id?: string;
    department_id?: string;

    status?: InvestigationStatus;
    sort_by?: CaseSortField;
    sort_order?: SortOrder;
}

export interface CaseHistoryResponse {
    id: string;
    case_id: string;
    status: InvestigationStatus;
    reason: string;
    next_action: string;
    changed_by: string;
    changed_at: string;
}

export interface UpdateCaseRequest {
    status: InvestigationStatus;
    reason: string;
    next_action: string;
}

export interface Statistics {
    total_cases: number;
    resolved_cases: number;
    pending_cases: number;
    escalated_cases: number;
}

export interface InvestigationReportSummary {
    total_cases: number;
    resolved_cases: number;
    waiting_cases: number;
    technical_investigation_cases: number;
    escalated_cases: number;
}

export interface InvestigationReportQuery {
    start_date: string;
    end_date: string;
    status?: InvestigationStatus;
}

export interface InvestigationReportResponse {
    start_date: string;
    end_date: string;
    applied_status: InvestigationStatus | null;
    summary: InvestigationReportSummary;
    items: CaseResponse[];
}