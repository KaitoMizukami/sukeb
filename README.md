## はじめに 
スケートパーク共有webアプリを作成しました<br>
自分のお気に入りのスケートパークを共有できます、また他の人の投稿にコメントを残せます。　<br>
投稿詳細画面では、スケートパーク周辺の現在の天候を知ることができます<br>
レスポンシブ対応はできていません

## イメージ図
投稿一覧
<img width="1440" alt="スクリーンショット 2023-04-10 午前2 04 16" src="https://user-images.githubusercontent.com/108565894/235426427-0ead8f6f-2453-41f2-a08e-435e42b86fd6.png">
投稿詳細
<img width="1440" alt="スクリーンショット 2023-05-01 午後5 08 56" src="https://user-images.githubusercontent.com/108565894/235427119-4a7871eb-aeb2-4836-a0aa-fa245ef8ec4b.png">

## 使用技術
- Python 3.9
- Django 4.1
- Postgres
- psycopg2-binary
- python-dotenv
- Pillow
- requests
- Docker / docker-compose
- Github Action (CI)

## 機能一覧
- ログイン / ログアウト
- ユーザー登録
- 投稿一覧
- 投稿の都道府県名検索
- 投稿詳細
- 現在の天気情報取得(天気予報API)
- コメント機能
- 投稿作成
- 投稿削除

## データベースER図
<img width="801" alt="スクリーンショット 2023-04-05 午後4 31 58" src="https://user-images.githubusercontent.com/108565894/235427234-eae3f45d-4967-4528-ad79-ae9fcc45e4a8.png">
