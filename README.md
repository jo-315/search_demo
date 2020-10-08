# 環境
flamework: Flask

DB: PostgreSQL

server: Heroku

## localでの起動コマンド
`docker-compose up`

※`-d`をつけるとバックグラウンドで実行

## heroku
https://search-demo-1234.herokuapp.com/
gitにpushした際、自動でherokuにデプロイされる

### Heroku内でdockerのコンテナを立てるとき
- Build the Dockerfile in the current directory and push the Docker image.
`heroku container:push web `

- Deploy the changes
`heroku container:release web`

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
`select * from テーブル名;`