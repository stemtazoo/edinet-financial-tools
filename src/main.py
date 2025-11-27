"""Streamlit application entrypoint for EDINET決算短信ビューア."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import streamlit as st

from modules import edinet_client, instagram_data, markdown_generator, settings, tanshin_parser


def render_search_page() -> None:
    """Render the document search page."""
    st.header("書類検索")
    st.write("EDINET から決算短信を検索します。条件を入力してください。")

    default_start_date = st.session_state.get("submission_date_from") or date.today() - timedelta(days=30)
    default_end_date = st.session_state.get("submission_date_to") or date.today()

    with st.form("search_form"):
        company_code = st.text_input("企業コード / 銘柄コード / EDINET コード")
        submission_date_range = st.date_input(
            "提出日",
            value=(default_start_date, default_end_date),
        )
        document_type = st.selectbox("書類種別", ["決算短信", "四半期報告書", "有価証券報告書"])
        submitted = st.form_submit_button("検索")

    if submitted:
        start_date, end_date = (
            submission_date_range if isinstance(submission_date_range, tuple) else (None, None)
        )

        if start_date and end_date and start_date > end_date:
            st.error("提出日の開始日は終了日より前の日付を指定してください。")
            return

        st.session_state["submission_date_from"] = start_date
        st.session_state["submission_date_to"] = end_date

        target_date = start_date or end_date or date.today()

        edinet_params = {
            "date": target_date.isoformat(),
            "type": 2,
        }

        status_placeholder = st.empty()
        download_placeholder = st.empty()

        try:
            status_placeholder.info("検索中です。しばらくお待ちください。")
            results = edinet_client.search_documents(edinet_params)
        except Exception as exc:  # pragma: no cover - UI feedback path
            status_placeholder.error(f"検索中にエラーが発生しました: {exc}")
            return

        if results:
            status_placeholder.success("検索結果を表示します。")

            header_cols = st.columns([2, 3, 2, 2, 2])
            header_cols[0].markdown("**書類ID**")
            header_cols[1].markdown("**企業名**")
            header_cols[2].markdown("**提出日**")
            header_cols[3].markdown("**書類種別**")
            header_cols[4].markdown("**操作**")

            for result in results:
                doc_id = result.get("doc_id", "")
                company = result.get("company_name", "")
                submitted_at = result.get("submission_date", "")
                doc_type = result.get("document_type", "")

                row_cols = st.columns([2, 3, 2, 2, 2])
                row_cols[0].write(doc_id)
                row_cols[1].write(company)
                row_cols[2].write(submitted_at)
                row_cols[3].write(doc_type)

                if row_cols[4].button("ダウンロード", key=f"download_{doc_id}"):
                    try:
                        download_placeholder.info(f"{doc_id} をダウンロード中です...")
                        save_dir = Path("downloads")
                        save_dir.mkdir(parents=True, exist_ok=True)
                        edinet_client.download_document(doc_id, str(save_dir))
                        download_placeholder.success(f"{doc_id} を {save_dir} に保存しました。")
                    except Exception as exc:  # pragma: no cover - UI feedback path
                        download_placeholder.error(f"ダウンロードに失敗しました: {exc}")
        else:
            date_range_label = "指定期間"
            if start_date and end_date:
                date_range_label = f"{start_date} 〜 {end_date}"
            elif start_date:
                date_range_label = f"{start_date} 以降"
            elif end_date:
                date_range_label = f"{end_date} 以前"

            status_placeholder.warning(f"{date_range_label}に該当する検索結果はありません。")


def render_financials_page() -> None:
    """Render the financial details page."""
    st.header("決算表示")
    st.write("決算短信ファイルをアップロードして主要指標を表示します。")
    uploaded_file = st.file_uploader("PDF/XBRL ファイルを選択", type=["pdf", "xbrl", "zip"])

    if uploaded_file:
        st.info("ダミー解析を実行します。TODO: 実際の解析ロジックに置き換えます。")
        # Placeholder: In a real app, save the file and pass the path.
        financials = tanshin_parser.parse_financials_from_file(uploaded_file.name)
        st.subheader(f"{financials.get('company_name')} ({financials.get('fiscal_year')})")
        col1, col2, col3 = st.columns(3)
        col1.metric("売上高", f"{financials.get('net_sales'):,} 円")
        col2.metric("営業利益", f"{financials.get('operating_income'):,} 円")
        col3.metric("当期純利益", f"{financials.get('net_income'):,} 円")
        st.write("EPS", financials.get("eps"))
        st.write("コメント", financials.get("notes"))
    else:
        st.info("ファイルをアップロードすると解析結果を表示します。")


def render_markdown_page() -> None:
    """Render the markdown generation page."""
    st.header("Markdown 生成")
    st.write("決算データからブログ用の Markdown を生成します。")
    st.caption("TODO: 実際の決算データを入力できるフォームを追加")

    if st.button("サンプルデータで生成"):
        financials = tanshin_parser.parse_financials_from_file("sample")
        markdown = markdown_generator.generate_markdown_from_financials(financials)
        st.success("Markdown を生成しました。")
        st.text_area("生成結果", markdown, height=200)


def render_instagram_page() -> None:
    """Render the Instagram data generation page."""
    st.header("Instagram 用データ生成")
    st.write("決算データから Instagram 投稿用データセットを作成します。")
    st.caption("TODO: 複数社データの入力とグラフテンプレート設定を追加")

    if st.button("サンプルデータセットを作成"):
        sample_financials = [
            tanshin_parser.parse_financials_from_file("sample1"),
            tanshin_parser.parse_financials_from_file("sample2"),
        ]
        dataset = instagram_data.create_instagram_dataset(sample_financials)
        st.success("データセットを生成しました。")
        st.json(dataset)


def render_settings_page() -> None:
    """Render the settings page for API configuration."""
    st.header("設定")
    st.write("EDINET API キーを設定します。")

    current_key = settings.get_edinet_api_key()
    status_text = "EDINET API キー：設定済み" if current_key else "EDINET API キー：未設定"
    st.info(status_text)

    api_key = st.text_input("API キー", type="password")
    if st.button("保存"):
        if api_key:
            try:
                settings.save_edinet_api_key(api_key)
                st.success("API キーを保存しました。アプリを再起動して反映してください。")
            except Exception as exc:  # pragma: no cover - UI feedback path
                st.error(f"保存に失敗しました: {exc}")
        else:
            st.error("API キーを入力してください。")


def main() -> None:
    """Application entrypoint defining navigation and page rendering."""
    st.set_page_config(page_title="EDINET 決算短信ビューア", layout="wide")
    st.title("EDINET 決算短信ビューア")
    st.caption("EDINET から取得した決算短信を閲覧・加工するツール")

    page = st.sidebar.selectbox(
        "ページを選択", ["書類検索", "決算表示", "Markdown 生成", "Instagram 用データ生成", "設定"]
    )

    if page == "書類検索":
        render_search_page()
    elif page == "決算表示":
        render_financials_page()
    elif page == "Markdown 生成":
        render_markdown_page()
    elif page == "Instagram 用データ生成":
        render_instagram_page()
    elif page == "設定":
        render_settings_page()


if __name__ == "__main__":
    main()
