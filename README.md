# 環境
flamework: Flask  
DB: PostgreSQL  
server: Heroku

## 環境構築
ルートディレクトリで`docker-compose build`

## localでの起動コマンド
`docker-compose up`  
※`-d`をつけるとバックグラウンドで実行

## heroku
https://search-demo-1234.herokuapp.com/  
gitにpushした際、自動でherokuにデプロイされる

### databaseの操作
- 新しいモデルの追加
dockerのflaskコンテナ内で以下を実行
`flask db migrate`
`flask db upgrade`

`Target database is not up to date`のエラーが出る時
`flask db stamp head`

- 新しいデータを投入
`init.sql`を変更後、docker内のデータを初期化した上で再度立ち上げる

- SQLファイルからdataを挿入
`heroku pg:psql postgresql-contoured-15367 --app search-demo-1234 --file ./init_db/docker-entrypoint-initdb.d/init.sql`

※portが5432のため接続できない場合があり

### Heroku内でdockerのコンテナを立てるとき
dashboardからRestart all dynosする

### コマンドラインから実行する場合
- Build the Dockerfile in the current directory and push the Docker image.  
`heroku container:push web `

- Deploy the changes  
`heroku container:release web`

# dockerコマンド
- 実行
`docker-compose up`

- バックグラウンド
`docker-compose up`

- 停止
`docker-compose stop`

- コンテナ内に入る(flask)
`docker-compose exec flask bash`

- コンテナ内に入る(DB: postgres)
`docker-compose exec postgres bash`

- db初期化
`docker-compose down -v`

# Flask
デバッグ
app.logger.debug("デバッグメッセージ")

# PostgreSQL
- データベースへ接続
`psql -U postgres(ユーザー名)`

## データベース内でのコマンド
- テーブル一覧
`\dt`

- テーブル内のデータを一覧
`select * from テーブル名;`
