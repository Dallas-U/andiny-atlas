export interface ExportAuditPayload {
    user_id: string;
    user_name: string;
    role: string;
    source: "reports" | "analytics" | "investigations";
    export_format: "csv" | "excel" | "pdf";
    file_name: string;
    record_count: number;
    processing_duration_ms: number;
    status?: "Success" | "Failed";
}

const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ??
    "http://127.0.0.1:8000";

export async function recordExportAudit(
    payload: ExportAuditPayload,
) {
    const response = await fetch(
        `${API_BASE_URL}/exports/audit`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Failed to record export audit",
        );
    }

    return response.json();
}

export async function getExportHistory() {
    const response = await fetch(
        `${API_BASE_URL}/exports/history`,
    );

    if (!response.ok) {
        throw new Error(
            "Failed to retrieve export history",
        );
    }

    return response.json();
}