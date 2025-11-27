"""Markdown generation helpers for financial summaries."""
from __future__ import annotations

from typing import Dict


def generate_markdown_from_financials(financials: Dict) -> str:
    """Generate markdown content from financial data."""
    company = financials.get("company_name", "不明な会社")
    fiscal_year = financials.get("fiscal_year", "年度未設定")
    net_sales = financials.get("net_sales", "-")
    operating_income = financials.get("operating_income", "-")
    ordinary_income = financials.get("ordinary_income", "-")
    net_income = financials.get("net_income", "-")
    eps = financials.get("eps", "-")
    notes = financials.get("notes", "")

    lines = [
        f"# {company} 決算概要 ({fiscal_year})",
        "",
        "## ハイライト",
        f"- 売上高: {net_sales:,} 円" if isinstance(net_sales, (int, float)) else f"- 売上高: {net_sales}",
        f"- 営業利益: {operating_income:,} 円" if isinstance(operating_income, (int, float)) else f"- 営業利益: {operating_income}",
        f"- 経常利益: {ordinary_income:,} 円" if isinstance(ordinary_income, (int, float)) else f"- 経常利益: {ordinary_income}",
        f"- 当期純利益: {net_income:,} 円" if isinstance(net_income, (int, float)) else f"- 当期純利益: {net_income}",
        f"- EPS: {eps}",
        "",
        "## コメント",
        notes or "詳細は後日更新予定です。",
    ]
    return "\n".join(lines)
