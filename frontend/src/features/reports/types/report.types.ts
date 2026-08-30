import type {
    CaseResponse,
    InvestigationStatus,
} from "../../investigation/types/investigation.types";

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