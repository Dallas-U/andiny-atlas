import * as XLSX from "xlsx";

import type { CaseResponse } from "../../investigation/types/investigation.types";

import { recordExportAudit } from "../api/exportAudit.api";

export async function exportReportToExcel(
    investigations: CaseResponse[],
) {
    const startedAt = performance.now();

    const rows = investigations.map((item) => ({
        Customer: item.customer_name,
        "Phone Number": item.phone_number,
        Status: item.result.status,
        Created: item.timestamp,
        Investigator: item.created_by,
    }));

    const worksheet = XLSX.utils.json_to_sheet(rows);

    const workbook = XLSX.utils.book_new();

    XLSX.utils.book_append_sheet(
        workbook,
        worksheet,
        "Investigations",
    );

    const filename = `investigation-report-${new Date()
        .toISOString()
        .slice(0, 10)}.xlsx`;

    XLSX.writeFile(workbook, filename);

    try {
        await recordExportAudit({
            user_id: "development-admin",
            user_name: "Development Super Administrator",
            role: "Administrator",
            source: "reports",
            export_format: "excel",
            file_name: filename,
            record_count: investigations.length,
            processing_duration_ms: Math.round(
                performance.now() - startedAt,
            ),
            status: "Success",
        });
    } catch (error) {
        console.error(
            "Failed to record Excel export audit:",
            error,
        );
    }
}