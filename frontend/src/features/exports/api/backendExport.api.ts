import { apiClient } from "../../../shared/api/client";

import type { InvestigationReportResponse } from "../../reports/types/report.types";
import type { ExportFormat } from "../types/export.types";

function extensionForFormat(
    format: ExportFormat,
): string {
    switch (format) {
        case "csv":
            return "csv";

        case "excel":
            return "xlsx";

        case "pdf":
            return "pdf";

        default:
            return "bin";
    }
}

export async function exportReportViaBackend(
    report: InvestigationReportResponse,
    format: ExportFormat,
): Promise<void> {
    const endpoint =
        format === "csv"
            ? "/exports/report/csv"
            : format === "excel"
                ? "/exports/report/excel"
                : "/exports/report/pdf";

    const response = await apiClient.post(
        endpoint,
        report,
        {
            responseType: "blob",
        },
    );

    const blob = new Blob(
        [response.data],
        {
            type:
                response.headers["content-type"] ??
                "application/octet-stream",
        },
    );

    const url =
        window.URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    const disposition =
        response.headers[
        "content-disposition"
        ];

    const fileName =
        disposition
            ?.match(/filename="(.+)"/)?.[1] ??
        `investigation-report.${extensionForFormat(format)}`;

    link.href = url;
    link.download = fileName;

    document.body.appendChild(link);

    link.click();

    link.remove();

    window.URL.revokeObjectURL(url);
}