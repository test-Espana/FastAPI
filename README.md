# FastAPI-tamplates
## Dockerコンテナ起動
`docker-compose up`
or
`docker-compose up -d`

## Dockerコンテナ停止
- docker-compose upの場合 → `control^+c`
- docker-compose up -dの場合 → `docker-compose down`

## fastAPI操作
.envファイル個別で渡します

### プレビュー表示
> http://localhost:8080/
<!-- ここにアクセスすると表示される -->

fastapiコンテナの中に入りたい時は
`docker exec -it fastapi /bin/bash`

## 注意事項
__pycache__ ファイルはgitにあげないように！

なんかあったらペンギンまで