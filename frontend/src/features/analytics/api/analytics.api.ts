import { apiClient } from "../../../shared/api/client";

import type {
    InvestigationAnalyticsResponse,
} from "../types/analytics.types";

export interface InvestigationAnalyticsQuery {
    start_date: string;
    end_date: string;
    interval?: "day" | "week" | "month";
}

export async function getInvestigationAnalytics(
    query: InvestigationAnalyticsQuery,
): Promise<InvestigationAnalyticsResponse> {
    const response =
        await apiClient.get<InvestigationAnalyticsResponse>(
            "/analytics/investigation-overview",
            {
                params: query,
            },
        );

    return response.data;
}