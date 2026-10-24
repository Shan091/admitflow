"""Rebuild the committed, fictional digital-PDF fixture with reportlab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle


def build() -> None:
    target = Path(__file__).with_name("structured-prospectus.pdf")
    canvas = Canvas(str(target), pagesize=A4, invariant=1)
    canvas.setTitle("Synthetic institution reference - structure test")
    canvas.setAuthor("AdmitFlow")
    width, height = A4
    programmes = [
        (
            "Nursing Programme",
            "45000",
            "11000",
            [
                "Applicants must be at least 18 years old.",
                "School marks must be at least 60 percent.",
                "These are fictional eligibility examples.",
            ],
            [
                "Hostel accommodation is on campus.",
                "The library is open from 9 AM to 5 PM.",
                "Lab induction precedes practical sessions.",
            ],
        ),
        (
            "Commerce Programme",
            "35000",
            "9000",
            [
                "Applicants must have completed school.",
                "Accounting is part of the curriculum.",
                "These are fictional eligibility examples.",
            ],
            [
                "Business communication is taught weekly.",
                "The reading room opens at 10 AM.",
                "Computer access follows induction.",
            ],
        ),
    ]
    for page, (name, tuition, hostel, left, right) in enumerate(programmes, start=1):
        canvas.setFillColor(colors.HexColor("#173b2c"))
        canvas.setFont("Helvetica-Bold", 21)
        canvas.drawString(48, height - 58, "Synthetic Institute")
        canvas.setFillColor(colors.HexColor("#34433d"))
        canvas.setFont("Helvetica", 10)
        canvas.drawString(
            48, height - 80, "Fictional reference for automated tests. Not an admissions offer."
        )
        canvas.setFont("Helvetica-Bold", 17)
        canvas.drawString(48, height - 128, name)
        for x, heading, lines in [(48, "Eligibility", left), (315, "Facilities", right)]:
            canvas.setFont("Helvetica-Bold", 13)
            canvas.drawString(x, height - 168, heading)
            canvas.setFont("Helvetica", 10)
            for index, text in enumerate(lines):
                canvas.drawString(x, height - 193 - 19 * index, text)
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(48, height - 300, "Annual tuition reference")
        data = [
            ["Programme", "Charge", "Annual amount"],
            [name, "Tuition", f"INR {tuition}"],
            [name, "Hostel", f"INR {hostel}"],
            [name, "Library", "Included"],
        ]
        table = Table(data, colWidths=[210, 145, width - 451], rowHeights=32)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eee8")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#9eb5a7")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        table.wrapOn(canvas, width - 96, 200)
        table.drawOn(canvas, 48, height - 450)
        canvas.setFont("Helvetica", 10)
        canvas.drawString(
            48,
            height - 480,
            "Printed tuition examples do not set the application or registration fee.",
        )
        canvas.setFont("Helvetica", 9)
        canvas.drawString(48, 42, "Synthetic fixture only. No real institution or applicant data.")
        canvas.drawRightString(width - 48, 42, f"Page {page}")
        canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    build()
