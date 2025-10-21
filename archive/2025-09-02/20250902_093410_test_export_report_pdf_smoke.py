from pathlib import Path
def test_export_pdf_script_exists():
    assert Path("scripts/export_report_pdf.py").exists()