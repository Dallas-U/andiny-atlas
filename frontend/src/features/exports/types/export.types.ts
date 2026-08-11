export type ExportFormat =
    | "csv"
    | "excel"
    | "pdf";

export type ExportSource =
    | "reports"
    | "analytics";

export interface ExportRequest {
    source: ExportSource;
    format: ExportFormat;
}

export interface ExportHistoryItem {
    audit_id: string;
    export_id: string;
    user_id: string;
    user_name: string;
    role: string;
    timestamp_utc: string;
    source: ExportSource;
    export_format: ExportFormat;
    file_name: string;
    record_count: number;
    processing_duration_ms: number;
    status: "Success" | "Failed";
    checksum: string | null;
    failure_reason: string | null;
}