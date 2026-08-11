import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import type {
    InvestigationAnalyticsResponse,
} from "../../analytics/types/analytics.types";

export function exportAnalyticsToPdf(
    analytics: InvestigationAnalyticsResponse,
): void {
    const document = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4",
    });

    document.setFontSize(18);
    document.text(
        "Andiny Atlas",
        14,
        16,
    );

    document.setFontSize(14);
    document.text(
        "Investigation Analytics",
        14,
        25,
    );

    document.setFontSize(9);

    document.text(
        `Reporting period: ${analytics.start_date} to ${analytics.end_date}`,
        14,
        33,
    );

    document.text(
        `Interval: ${analytics.interval}`,
        14,
        39,
    );

    document.text(
        `Generated: ${new Date().toLocaleString("en-GB")}`,
        14,
        45,
    );

    document.setFontSize(11);

    document.text(
        "Key Performance Indicators",
        14,
        56,
    );

    autoTable(document, {
        startY: 60,

        head: [[
            "Total",
            "Resolved",
            "Waiting",
            "Technical",
            "Escalated",
            "Resolution %",
            "Escalation %",
        ]],

        body: [[
            analytics.kpis.total_cases,
            analytics.kpis.resolved_cases,
            analytics.kpis.waiting_cases,
            analytics.kpis
                .technical_investigation_cases,
            analytics.kpis.escalated_cases,
            analytics.kpis.resolution_rate,
            analytics.kpis.escalation_rate,
        ]],

        theme: "grid",

        styles: {
            fontSize: 7,
            cellPadding: 2,
        },
    });

    document.text(
        "Investigation Trend",
        14,
        84,
    );

    autoTable(document, {
        startY: 88,

        head: [[
            "Period",
            "Count",
        ]],

        body: analytics.trend.map(
            (item) => [
                item.period,
                item.count,
            ],
        ),

        theme: "striped",

        styles: {
            fontSize: 8,
        },
    });

    const trendEndY =
        (
            document as jsPDF & {
                lastAutoTable?: {
                    finalY: number;
                };
            }
        ).lastAutoTable?.finalY ?? 100;

    document.text(
        "Status Distribution",
        14,
        trendEndY + 10,
    );

    autoTable(document, {
        startY: trendEndY + 14,

        head: [[
            "Status",
            "Count",
            "Percentage",
        ]],

        body:
            analytics.status_distribution.map(
                (item) => [
                    item.status,
                    item.count,
                    `${item.percentage}%`,
                ],
            ),

        theme: "striped",

        styles: {
            fontSize: 8,
        },
    });

    const statusEndY =
        (
            document as jsPDF & {
                lastAutoTable?: {
                    finalY: number;
                };
            }
        ).lastAutoTable?.finalY ?? 140;

    document.text(
        "Investigator Workload",
        14,
        statusEndY + 10,
    );

    autoTable(document, {
        startY: statusEndY + 14,

        head: [[
            "Investigator",
            "Investigations",
        ]],

        body:
            analytics.investigator_workload.map(
                (item) => [
                    item.investigator_name,
                    item.count,
                ],
            ),

        theme: "striped",

        styles: {
            fontSize: 8,
        },

        didDrawPage: () => {
            document.setFontSize(8);

            document.text(
                `Andiny Atlas Investigation Analytics — Page ${document.getNumberOfPages()}`,
                14,
                287,
            );
        },
    });

    const filename =
        `investigation-analytics-${analytics.start_date}-to-${analytics.end_date}.pdf`;

    document.save(
        filename,
    );
}