### Описание проекта
Сервис парсинга статей с портала Хабр.
Имеется возможность настраивать периодичность парсинга каждого хаба через REST API или административную панель Django.
Пользователи могут запрашивать статьи, авторов, хабы через REST API, также добавлять хаб в избранные.

### Установка
- Клонируйте репозиторий:
```commandline
git clone https://github.com/mihailkasev/habr_service.git
```
### Тесты
- Убедитесь, что у вас локально запущены redis и postgres
- Переименуйте файл .env.example в .env и замените содержимое файла необходимыми данными
- Перейдите в директорию habr_service/backend/ и запустите тесты бекэнда:
```commandline
cd backend
```
```commandline
python manage.py test
```
- Перейдите в директорию habr_service/parser/ и запустите тесты парсер сервиса:
```commandline
cd parser
```
```commandline
python -m unittest
```
### Запуск проекта
- Переименуйте директорию habr_service/infra/env-example/ в habr_service/infra/env/ и замените содержимое файлов необходимыми данными
- Запустите проект одной командой:
```commandline
docker-compose up -d --build
```
- Административная панель доступна по адресу:
localhost/admin/
- Swagger доступен по адресу:
localhost/swagger/
(Необходимо выполнить вход в качестве администратора для доступа к swagger)
- Готово!

### Автор:
- [Михаил Касев](https://github.com/mihailkasev/) - создание проекта, деплой.