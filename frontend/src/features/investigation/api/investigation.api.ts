import { apiClient } from "../../../shared/api/client";

import type {
    CaseHistoryResponse,
    CaseQuery,
    CaseResponse,
    InvestigationReportQuery,
    InvestigationReportResponse,
    PaginatedCasesResponse,
    Statistics,
    SupportCase,
    UpdateCaseRequest,
} from "../types/investigation.types";

export async function investigate(
    supportCase: SupportCase,
): Promise<CaseResponse> {
    const response = await apiClient.post<CaseResponse>(
        "/support/investigate",
        supportCase,
    );

    return response.data;
}

export async function getMyCases(
    query: CaseQuery = {},
): Promise<PaginatedCasesResponse> {
    const response = await apiClient.get<PaginatedCasesResponse>(
        "/support/my-cases",
        {
            params: query,
        },
    );

    return response.data;
}

export async function getCases(
    query: CaseQuery = {},
): Promise<PaginatedCasesResponse> {
    const response = await apiClient.get<PaginatedCasesResponse>(
        "/support/cases",
        {
            params: query,
        },
    );

    return response.data;
}

export async function getCase(
    caseId: string,
): Promise<CaseResponse> {
    const response = await apiClient.get<CaseResponse>(
        `/support/cases/${caseId}`,
    );

    return response.data;
}

export async function getCaseHistory(
    caseId: string,
): Promise<CaseHistoryResponse[]> {
    const response = await apiClient.get<CaseHistoryResponse[]>(
        `/support/cases/${caseId}/history`,
    );

    return response.data;
}

export async function updateCase(
    caseId: string,
    request: UpdateCaseRequest,
): Promise<CaseResponse> {
    const response = await apiClient.patch<CaseResponse>(
        `/support/cases/${caseId}`,
        request,
    );

    return response.data;
}

export async function getStatistics(): Promise<Statistics> {
    const response = await apiClient.get<Statistics>(
        "/support/statistics",
    );

    return response.data;
}

export async function getInvestigationSummaryReport(
    query: InvestigationReportQuery,
): Promise<InvestigationReportResponse> {
    const response =
        await apiClient.get<InvestigationReportResponse>(
            "/reports/investigation-summary",
            {
                params: query,
            },
        );

    return response.data;
}