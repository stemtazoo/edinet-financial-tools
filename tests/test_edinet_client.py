import io
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.modules.edinet_client import BASE_URL, download_document, search_documents


class TestEdinetClient(TestCase):
    def test_search_documents_success(self) -> None:
        params: Dict[str, Any] = {"date": "2024-01-01", "type": 2, "code": "S12345"}
        expected_results = [{"docID": "S1001234"}]

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"results": expected_results}

        with patch("src.modules.edinet_client.requests.get", return_value=mock_response) as mock_get:
            results = search_documents(params)

        mock_get.assert_called_once_with(
            f"{BASE_URL}/documents.json",
            params={"date": "2024-01-01", "type": 2, "code": "S12345"},
            headers={},
            timeout=30,
        )
        self.assertEqual(results, expected_results)

    def test_search_documents_failure(self) -> None:
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch("src.modules.edinet_client.requests.get", return_value=mock_response):
            with self.assertRaises(RuntimeError) as ctx:
                search_documents({"date": "2024-01-01"})

        self.assertIn("Failed to search documents", str(ctx.exception))

    def test_download_document_saves_and_extracts(self) -> None:
        doc_id = "S1000001"
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("sample.txt", "content")
        zip_buffer.seek(0)

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.iter_content.return_value = [zip_buffer.getvalue()]

        with TemporaryDirectory() as tmp_dir:
            with patch("src.modules.edinet_client.requests.get", return_value=mock_response) as mock_get:
                extracted_path = download_document(doc_id, tmp_dir)

            mock_get.assert_called_once_with(
                f"{BASE_URL}/documents/{doc_id}",
                params={"type": 1},
                headers={},
                stream=True,
                timeout=60,
            )

            extracted_file = Path(extracted_path) / "sample.txt"
            self.assertTrue(extracted_file.exists())
            self.assertEqual(extracted_file.read_text(), "content")

    def test_download_document_http_error(self) -> None:
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        with TemporaryDirectory() as tmp_dir:
            with patch("src.modules.edinet_client.requests.get", return_value=mock_response):
                with self.assertRaises(RuntimeError) as ctx:
                    download_document("missing", tmp_dir)

        self.assertIn("Failed to download document", str(ctx.exception))
