## index.html を apche コンテナで表示する。

1. docker run で Apche コンテナを作成
2. http://localhost:8089/で確認
3. cp コマンドで apache コンテナ内に index.html をコピー
   - docker cp index.html apa000ex19:usr/local/apache2/htdocs
4. http://localhost:8089/で確認
5. ファイルの削除 or ファイル名の変更
6. cp コマンドで apache コンテナ内からホストへ index.html をコピー
   - docker cp apa000ex19:usr/local/apache2/htdocs/index.html dockerFileCopy
7. コンテナを停止、削除
