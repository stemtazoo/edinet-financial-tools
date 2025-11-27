"""Parsing utilities for financial statements."""
from __future__ import annotations

from typing import Dict


def parse_financials_from_file(file_path: str) -> Dict:
    """Parse financial information from a given file.

    TODO: Implement real parsing for XBRL/PDF documents.
    """
    # TODO: Replace with actual parsing logic reading XBRL or PDF files.
    return {
        "company_name": "サンプル株式会社",
        "fiscal_year": "2024年3月期",
        "net_sales": 100_000_000,
        "operating_income": 8_000_000,
        "ordinary_income": 7_500_000,
        "net_income": 5_000_000,
        "eps": 123.45,
        "notes": "サンプルデータ。TODO: 決算短信ファイルを解析して実データを抽出する。",
    }
