from __future__ import annotations

import csv
from io import BytesIO, StringIO

from openpyxl import Workbook
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from app.models.report import InvestigationReportResponse


class ExportGenerationService:
    """
    Backend export generation engine.

    This service is the single authoritative location for
    generating CSV, Excel, and PDF exports for Atlas.
    """

    @staticmethod
    def generate_csv(
        report: InvestigationReportResponse,
    ) -> bytes:
        buffer = StringIO()

        writer = csv.writer(buffer)

        writer.writerow(
            [
                "Customer",
                "Phone Number",
                "Status",
                "Created",
                "Investigator",
            ]
        )

        for item in report.items:
            writer.writerow(
                [
                    item.customer_name,
                    item.phone_number,
                    item.result.status,
                    item.timestamp,
                    item.created_by,
                ]
            )

        return buffer.getvalue().encode("utf-8")

    @staticmethod
    def generate_excel(
        report: InvestigationReportResponse,
    ) -> bytes:
        workbook = Workbook()

        worksheet = workbook.active

        worksheet.title = "Investigations"

        worksheet.append(
            [
                "Customer",
                "Phone Number",
                "Status",
                "Created",
                "Investigator",
            ]
        )

        for item in report.items:
            worksheet.append(
                [
                    item.customer_name,
                    item.phone_number,
                    item.result.status,
                    item.timestamp,
                    item.created_by,
                ]
            )

        output = BytesIO()

        workbook.save(output)

        return output.getvalue()

    @staticmethod
    def generate_pdf(
        report: InvestigationReportResponse,
    ) -> bytes:
        output = BytesIO()

        document = SimpleDocTemplate(output)

        styles = getSampleStyleSheet()

        elements = [
            Paragraph(
                "Andiny Atlas Investigation Report",
                styles["Title"],
            ),
            Paragraph(
                f"Reporting Period: {report.start_date} - {report.end_date}",
                styles["Normal"],
            ),
            Paragraph(
                f"Records: {len(report.items)}",
                styles["Normal"],
            ),
            Paragraph(" ", styles["Normal"]),
        ]

        for item in report.items:
            elements.append(
                Paragraph(
                    (
                        f"<b>Customer:</b> {item.customer_name}<br/>"
                        f"<b>Phone:</b> {item.phone_number}<br/>"
                        f"<b>Status:</b> {item.result.status}<br/>"
                        f"<b>Investigator:</b> {item.created_by}<br/>"
                        f"<b>Created:</b> {item.timestamp}"
                    ),
                    styles["BodyText"],
                )
            )

            elements.append(
                Paragraph(" ", styles["Normal"]),
            )

        document.build(elements)

        return output.getvalue()