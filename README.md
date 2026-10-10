# 書籍スキャンpdfファイルに目次を追加するpythonスクリプト

1. 目次情報はpdfファイル中の目次部分を取り出して、Google AIでjson形式にして出力してもらう。
2. pdf_toc.pyを実行してpdfファイルに目次を追加する。

$ python pdf_toc.py input_book.pdf toc_data.json --offset 16

