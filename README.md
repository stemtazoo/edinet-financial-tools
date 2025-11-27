# edinet-financial-tools

EDINET から企業の決算短信を取得し、以下を行う Python ツールセットです：

* Streamlit による **決算内容の閲覧**
* GitHub Pages 向けの **Markdown 記事生成**
* Instagram 投稿用グラフのための **元データ生成**

このリポジトリは、企業分析・投資研究・ブログ運営を効率化するための統合ツール群を提供します。

---

## 🚀 Features（機能一覧）

### 🔎 **1. EDINET API を利用した決算短信検索**

* 企業コード／銘柄コード／期間を指定して EDINET 書類を検索
* 検索結果を Streamlit 上で一覧表示

### 📥 **2. 決算短信（PDF / XBRL）のダウンロード**

* EDINET API からファイルを取得してローカル保存

### 📊 **3. 主要財務データの抽出（予定）**

* 売上高
* 営業利益
* 経常利益
* 当期純利益
* EPS など

### 📰 **4. Markdown 記事生成（GitHub Pages / ブログ用）**

* 決算内容を自動で Markdown に整形
* GitHub Pages に貼るだけで記事になる形式を出力

### 📷 **5. Instagram 投稿用データ生成**

* グラフ画像生成のための簡易データ作成ツール

---

## 📁 Project Structure（構成）

```
edinet-financial-tools/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ docs/
│   └─ SRS_EDINET_Viewer.md      # ソフトウェア要求仕様書（SRS）
└─ src/
    ├─ main.py                   # Streamlit アプリのエントリーポイント
    └─ modules/
        ├─ __init__.py
        ├─ edinet_client.py      # EDINET API 呼び出し
        ├─ tanshin_parser.py     # 決算短信から財務データ抽出
        ├─ markdown_generator.py # ブログ用 Markdown 生成
        ├─ instagram_data.py     # Instagram 用データ整形
        └─ settings.py           # 設定値管理
```

---

## 🛠 Setup（セットアップ）

### 1. Clone the repository

```
git clone https://github.com/your-account/edinet-financial-tools.git
cd edinet-financial-tools
```

### 2. Create a virtual environment（任意）

```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶ Usage（使い方）

### Streamlit アプリを起動

```
streamlit run src/main.py
```

ブラウザが自動で開かない場合は、URL（例: [http://localhost:8501）にアクセスしてください。](http://localhost:8501）にアクセスしてください。)

---

## 📚 Documents

* [ソフトウェア要求仕様書（SRS）](docs/SRS_EDINET_Viewer.md)

---

## 🗺 Roadmap（今後の計画）

* EDINET 検索フォームの実装
* XBRL/PDF 解析ロジックの実装
* Markdown テンプレートの拡張
* Instagram 用画像生成フローの整備
* 複数企業比較や期間比較のサポート

---

## 📜 License

MIT License

---

## 💬 Notes

Pull Request / Issue は大歓迎です！
