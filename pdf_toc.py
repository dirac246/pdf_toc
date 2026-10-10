# 必要なライブラリのインストール（Claude Codeやターミナルで実行する場合）
#
# brew install uv
# uv venv
#
# source .venv/bin/activate
# brew install pyenv
# pyenv install 3.12
# pyenv global 3.12
# python --version
# pip install pymupdf
# python -m ensurepip --default-pip
# python -m pip install pymupdf
#
# python pdf_toc.py input_book.pdf toc_data.json --offset 16
#

import argparse
import fitz
import json
import os


def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(
        description="PDFファイルにJSONから目次（しおり）を追加するスクリプト"
    )

    # 必須の引数
    parser.add_argument(
        "input_pdf", help="目次を追加したい元のPDFファイルのパス"
    )
    parser.add_argument("toc_json", help="目次データ（JSONファイル）のパス")

    # オプション引数（指定しない場合のデフォルト値を設定可能）
    parser.add_argument(
        "-o",
        "--output",
        help="出力するPDFファイルのパス（省略時は '入力ファイル名_with_toc.pdf'）",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="ページ番号のオフセット値（デフォルト: 0）",
    )

    args = parser.parse_args()

    # 出力ファイル名が省略された場合は自動生成
    if args.output:
        output_pdf = args.output
    else:
        base, ext = os.path.splitext(args.input_pdf)
        output_pdf = f"{base}_with_toc{ext}"

    # 1. 外部のJSONファイルが存在するか確認して読み込む
    if not os.path.exists(args.toc_json):
        print(f"エラー: 目次ファイル '{args.toc_json}' が見つかりません。")
        exit(1)

    with open(args.toc_json, "r", encoding="utf-8") as f:
        toc_data = json.load(f)

    # 2. 入力PDFを開く
    if not os.path.exists(args.input_pdf):
        print(f"エラー: 元のPDFファイル '{args.input_pdf}' が見つかりません。")
        exit(1)

    doc = fitz.open(args.input_pdf)
    toc = []

    # 3. 読み込んだデータにオフセットを適用してPyMuPDFのフォーマットに変換
    for level, title, page in toc_data:
        actual_page = page + args.offset
        toc.append([level, title, actual_page])

    # 4. 目次（しおり）をPDFにセットして保存
    doc.set_toc(toc)
    doc.save(output_pdf)
    doc.close()

    print(
        f"PDFへの目次追加が完了しました！（オフセット: +{args.offset}ページ）"
    )
    print(f"出力ファイル: {output_pdf}")


if __name__ == "__main__":
    main()
