# 環境
flamework: Flask
DB: PostgreSQL

app下のファイルが仮想環境（docker）内のappにマウントされる

# 起動コマンド
/devで`docker-compose up`




# dockerコマンド
- 実行
`docker-compose up`

バックグラウンド
`docker-compose up`

- 停止
`docker-compose stop`

- コンテナ内に入る(flask)
`docker-compose exec flask bash`

- コンテナ内に入る(DB: postgres)
`docker-compose exec postgres bash`

- db初期化
`docker-compose down -v`

# PostgreSQL
- データベースへ接続
`psql -U postgres(ユーザー名)`

## データベース内でのコマンド
- テーブル一覧
`\dt`

- テーブル内のデータを一覧
`select * from テーブル名`