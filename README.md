Для старта - запустить приложение из Docker:
docker-compose up --build

Приложение будет доступно по адресу:
http://localhost:8000

Документация Swagger UI:
http://localhost:8000/docs

Запуск тестов:
pytest

Запуск с покрытием:
pytest --cov=app tests/

