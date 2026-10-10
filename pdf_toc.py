# 必要なライブラリのインストール（Claude Codeやターミナルで実行する場合）
#
# brew install uv
# uv venv
# source .venv/bin/activate
# brew install pyenv
# pyenv install 3.12
# pyenv global 3.12
# python --version
# pip install pymupdf
# python -m ensurepip --default-pip
# python -m pip install pymupdf
#
# python py_toc.py
#

import fitz
import json
import os

# ==========================================
# 設定エリア（ここを変更するだけ）
# ==========================================
input_pdf = "input_book.pdf"
output_pdf = "output_book_with_toc.pdf"
toc_json_file = "toc_data.json"  # 目次データファイルのパス

# 本文の「1ページ目」が、実際のPDFで「何ページ目」にあるかのズレを指定
# 例: PDFの1〜16ページ目が表紙や前書きで、17ページ目から本文が始まる場合は「16」
page_offset = 16
# ==========================================

# 1. 外部のJSONファイルが存在するか確認して読み込む
if not os.path.exists(toc_json_file):
    print(f"エラー: 目次ファイル '{toc_json_file}' が見つかりません。")
    exit(1)

with open(toc_json_file, "r", encoding="utf-8") as f:
    toc_data = json.load(f)

# 2. PDFを開く
if not os.path.exists(input_pdf):
    print(f"エラー: 元のPDFファイル '{input_pdf}' が見つかりません。")
    exit(1)

doc = fitz.open(input_pdf)
toc = []

# 3. 読み込んだデータにオフセットを適用してPyMuPDFのフォーマットに変換
for level, title, page in toc_data:
    # JSONに記載されたページ番号に、指定されたオフセット値を加算
    actual_page = page + page_offset
    toc.append([level, title, actual_page])

# 4. 目次（しおり）をPDFにセットして保存
doc.set_toc(toc)
doc.save(output_pdf)
doc.close()

print(f"PDFへの目次追加が完了しました！（オフセット: +{page_offset}ページ）")
print(f"出力ファイル: {output_pdf}")
