"""Download encoding prevents formulas while preserving international phone strings."""

import csv
import io

from openpyxl import load_workbook

from src.staff.exports import render_csv, render_xlsx


def test_downloads_never_treat_user_text_as_formulas():
    rows = [["name", "phone"], [' \t=HYPERLINK("evil")', "+919876543210"], ["നായർ\x00", "@command"]]
    parsed = list(csv.reader(io.StringIO(render_csv(rows).decode("utf-8-sig"))))
    assert parsed[1][0].startswith("'") and parsed[1][1] == "'+919876543210"
    assert parsed[2] == ["നായർ", "'@command"]
    workbook = load_workbook(io.BytesIO(render_xlsx(rows)))
    sheet = workbook.active
    assert sheet["A2"].data_type == "s" and sheet["A2"].value == rows[1][0]
    assert sheet["B2"].value == "+919876543210" and sheet["B2"].data_type == "s"
    assert sheet["A3"].value == "നായർ"
