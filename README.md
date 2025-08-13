# voronini.fun

### Запуск проекта через Docker.

1. Скачать и установить программу Docker на свой компьютер
2. Склонировать данный проект на свою машину
3. Перейти в директорию, где находятся файлы **Dockerfile** и **docker-compose.yaml**
4. ```shell
   docker compose build --no-cache
   docker compose up
   ```
5. В браузере зайти на [`http://127.0.0.1:8000/docs`](): автоматическая OpenAPI-документация


### Запуск проекта локально.


### Stack
- Python 3.12
- FastAPI
- Alembic
- SQLAlchemy 2.0 (async)
- Poetry
- Redis
- PostgreSQL