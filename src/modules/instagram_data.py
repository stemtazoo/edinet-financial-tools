"""Helpers for preparing Instagram-ready datasets."""
from __future__ import annotations

from typing import Dict, List


def create_instagram_dataset(financials_list: List[Dict]) -> List[Dict]:
    """Create a dataset for Instagram posts from financial data."""
    # TODO: Format data for graphing/visual templates specific to Instagram posts.
    shaped_data = []
    for item in financials_list:
        shaped_data.append(
            {
                "company_name": item.get("company_name", "不明な会社"),
                "fiscal_year": item.get("fiscal_year", "年度未設定"),
                "net_sales": item.get("net_sales"),
                "operating_income": item.get("operating_income"),
                "net_income": item.get("net_income"),
            }
        )
    return shaped_data
