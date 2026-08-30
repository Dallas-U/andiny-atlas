import { apiClient } from "../../../shared/api/client";

import type {
    InvestigationReportQuery,
    InvestigationReportResponse,
} from "../types/report.types";

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