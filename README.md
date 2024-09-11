# FastAPI-tamplates
## Dockerコンテナ起動
`docker-compose up`
or
`docker-compose up -d`

## fastAPI操作
.envファイル個別で渡します

http://localhost:8080/
<!-- ここにアクセスすると表示される -->

fastapiコンテナの中に入りたい時は
`docker exec -it fastapi /bin/bash`

## 注意事項
__pycache__ ファイルはgitにあげないように！

なんかあったらペンギンまで
