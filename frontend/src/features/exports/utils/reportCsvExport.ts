import type { CaseResponse } from "../../investigation/types/investigation.types";
import { recordExportAudit } from "../api/exportAudit.api";

function downloadFile(
    content: string,
    filename: string,
    mimeType: string,
) {
    const blob = new Blob([content], {
        type: mimeType,
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(url);
}

export async function exportReportToCsv(
    investigations: CaseResponse[],
) {
    const startedAt = performance.now();

    const headers = [
        "Customer",
        "Phone Number",
        "Status",
        "Created",
        "Investigator",
    ];

    const rows = investigations.map((item) => [
        item.customer_name,
        item.phone_number,
        item.status,
        item.created_at,
        item.created_by,
    ]);

    const csv = [
        headers.join(","),
        ...rows.map((row) =>
            row.map((value) => `"${value}"`).join(","),
        ),
    ].join("\n");

    const filename = `investigation-report-${new Date()
        .toISOString()
        .slice(0, 10)}.csv`;

    downloadFile(
        csv,
        filename,
        "text/csv;charset=utf-8;",
    );

    try {
        await recordExportAudit({
            user_id: "development-admin",
            user_name: "Development Super Administrator",
            role: "Administrator",
            source: "reports",
            export_format: "csv",
            file_name: filename,
            record_count: investigations.length,
            processing_duration_ms: Math.round(
                performance.now() - startedAt,
            ),
            status: "Success",
        });
    } catch (error) {
        console.error(
            "Failed to record export audit:",
            error,
        );
    }
}