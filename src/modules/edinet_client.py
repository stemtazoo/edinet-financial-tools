"""Client utilities for interacting with the EDINET API."""
from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .settings import get_edinet_api_key


BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/v2"


def _build_headers() -> Dict[str, str]:
    """Build request headers, adding API key when available."""

    api_key = get_edinet_api_key()
    headers: Dict[str, str] = {}
    if api_key:
        headers["X-API-KEY"] = api_key
    return headers


def search_documents(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Search documents from EDINET based on parameters.

    Args:
        params: Dictionary containing search parameters such as ``date``,
            ``type``, ``code`` or other code-based filters.

    Returns:
        List of search results as dictionaries.

    Raises:
        RuntimeError: If the API request fails or returns an unexpected format.
    """

    allowed_params = (
        "date",
        "type",
        "code",
        "edinetCode",
        "fundCode",
        "securitiesCode",
    )
    query: Dict[str, Any] = {
        key: value for key, value in params.items() if key in allowed_params and value
    }

    try:
        response = requests.get(
            f"{BASE_URL}/documents.json",
            params=query,
            headers=_build_headers(),
            timeout=30,
        )
    except requests.RequestException as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Failed to search documents: {exc}") from exc

    if not response.ok:
        raise RuntimeError(
            f"Failed to search documents: {response.status_code} {response.text}"
        )

    data: Dict[str, Any] = response.json()
    results: Optional[List[Dict[str, Any]]] = data.get("results")  # type: ignore[assignment]
    if not isinstance(results, list):
        raise RuntimeError("Unexpected response format from EDINET API.")

    return results


def download_document(doc_id: str, save_path: str) -> Path:
    """Download a specified document from EDINET and extract it.

    Args:
        doc_id: Document ID to download.
        save_path: Directory to save the downloaded zip and extracted contents.

    Returns:
        Path to the directory containing extracted files.

    Raises:
        RuntimeError: If the download fails or the zip file cannot be processed.
    """

    target_dir = Path(save_path)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(
            f"{BASE_URL}/documents/{doc_id}",
            params={"type": 1},
            headers=_build_headers(),
            stream=True,
            timeout=60,
        )
    except requests.RequestException as exc:  # pragma: no cover - network errors
        raise RuntimeError(f"Failed to download document {doc_id}: {exc}") from exc

    if not response.ok:
        raise RuntimeError(
            f"Failed to download document {doc_id}: {response.status_code} {response.text}"
        )

    zip_path = target_dir / f"{doc_id}.zip"
    with zip_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    extract_dir = target_dir / doc_id
    extract_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"Downloaded file for {doc_id} is not a valid zip archive.") from exc

    return extract_dir
