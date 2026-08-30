export interface AnalyticsKpis {
    total_cases: number;
    resolved_cases: number;
    waiting_cases: number;
    technical_investigation_cases: number;
    escalated_cases: number;

    resolution_rate: number;
    escalation_rate: number;
}

export interface StatusDistributionItem {
    status: string;
    count: number;
    percentage: number;
}

export interface InvestigationTrendItem {
    period: string;
    count: number;
}

export interface InvestigatorWorkloadItem {
    investigator_id: string;
    investigator_name: string;
    count: number;
}

export interface InvestigationAnalyticsResponse {
    start_date: string;
    end_date: string;
    interval: string;

    kpis: AnalyticsKpis;

    status_distribution: StatusDistributionItem[];

    trend: InvestigationTrendItem[];

    investigator_workload: InvestigatorWorkloadItem[];
}