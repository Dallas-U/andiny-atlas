import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import type {
    InvestigationReportResponse,
} from "../../reports/types/report.types";

import { recordExportAudit } from "../api/exportAudit.api";

function formatDateTime(value: string): string {
    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    });
}

export async function exportReportToPdf(
    report: InvestigationReportResponse,
): Promise<void> {
    const startedAt = performance.now();

    const document = new jsPDF({
        orientation: "landscape",
        unit: "mm",
        format: "a4",
    });

    const generatedAt = new Date().toLocaleString(
        "en-GB",
        {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        },
    );

    document.setFontSize(18);
    document.text(
        "Andiny Atlas",
        14,
        16,
    );

    document.setFontSize(14);
    document.text(
        "Investigation Report",
        14,
        25,
    );

    document.setFontSize(9);

    document.text(
        `Reporting period: ${report.start_date} to ${report.end_date}`,
        14,
        33,
    );

    document.text(
        `Status filter: ${report.applied_status ?? "All statuses"}`,
        14,
        39,
    );

    document.text(
        `Generated: ${generatedAt}`,
        14,
        45,
    );

    document.setFontSize(11);

    document.text(
        "Report Summary",
        14,
        56,
    );

    autoTable(document, {
        startY: 60,

        head: [[
            "Total Cases",
            "Resolved",
            "Waiting",
            "Technical Investigation",
            "Escalated",
        ]],

        body: [[
            report.summary.total_cases,
            report.summary.resolved_cases,
            report.summary.waiting_cases,
            report.summary.technical_investigation_cases,
            report.summary.escalated_cases,
        ]],

        theme: "grid",

        styles: {
            fontSize: 9,
            cellPadding: 3,
        },

        headStyles: {
            fontStyle: "bold",
        },
    });

    const rows = report.items.map(
        (investigation) => [
            investigation.customer_name,
            investigation.phone_number,
            investigation.result.status,
            formatDateTime(
                investigation.timestamp,
            ),
            investigation.created_by,
        ],
    );

    autoTable(document, {
        startY: 88,

        head: [[
            "Customer",
            "Phone Number",
            "Status",
            "Created",
            "Investigator",
        ]],

        body: rows,

        theme: "striped",

        styles: {
            fontSize: 8,
            cellPadding: 3,
            overflow: "linebreak",
        },

        headStyles: {
            fontStyle: "bold",
        },

        columnStyles: {
            0: {
                cellWidth: 45,
            },
            1: {
                cellWidth: 35,
            },
            2: {
                cellWidth: 35,
            },
            3: {
                cellWidth: 45,
            },
            4: {
                cellWidth: 90,
            },
        },

        margin: {
            left: 14,
            right: 14,
        },

        didDrawPage: () => {
            const pageNumber =
                document.getNumberOfPages();

            document.setFontSize(8);

            document.text(
                `Andiny Atlas Investigation Report — Page ${pageNumber}`,
                14,
                200,
            );
        },
    });

    const filename =
        `investigation-report-${new Date()
            .toISOString()
            .slice(0, 10)}.pdf`;

    document.save(filename);

    try {
        await recordExportAudit({
            user_id: "development-admin",
            user_name: "Development Super Administrator",
            role: "Administrator",
            source: "reports",
            export_format: "pdf",
            file_name: filename,
            record_count: report.items.length,
            processing_duration_ms: Math.round(
                performance.now() - startedAt,
            ),
            status: "Success",
        });
    } catch (error) {
        console.error(
            "Failed to record PDF export audit:",
            error,
        );
    }
}