# QRKot
### О проекте.
Приложение для Благотворительного фонда поддержки котиков QRKot.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции. 
___
### Возможности
- Создавать и редактировать благотворительные проекты может создавать только пользователь с правами superuser. Нельзя редактировать уже полностью инвестированный проект, а так же уменьшать необходимую сумму ниже уже внесенных средств. Нельзя удалять проект, если в него уже поступили средства.
- Зарегистрированный пользователь может создавать пожертвования. Однако не может указывать куда пойдут средства - все решается автоматически, по принципу очереди.
- Никто не может редактировать или удалять пожертвования.
___
### При создании проекта использовалось:
- язык программирования [Python 3](https://www.python.org/);
- фреймворк [FastAPI](https://github.com/fastapi/fastapi/blob/master/docs/ru/docs/index.md),
- библиотека [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) для работы с базой данных,
- библиотека [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/) для создания отчетов в виде [Google-таблиц](https://developers.google.com/sheets).
___
Чтобы развернуть проект необходимо следующие:
- Клонировать репозиторий со своего GitHub и перейти в него в командной строке:

```
git clone git@github.com:levisserena/cat_charity_fund.git
```
>*Активная ссылка на репозиторий под этой кнопкой* -> [КНОПКА](https://github.com/levisserena/cat_charity_fund)
- Перейдите в папку с проектом:
```
cd cat_charity_fund
```
- Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/bin/activate
```
- Установить зависимости:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- Создать и заполнить файл `.env`. Пример можно посмотреть в файле `.env.example`.
Для подключения сервисов Google-таблиц необходимо на сайте [Google cloud](https://console.cloud.google.com/projectselector2/home/dashboard) подключить API сервис. Подробнее смотрите на сайте.
```
touch .env
```
- Создать базу данных.
```
alembic upgrade head
```
- Запустите сервер:

```
uvicorn app.main:app
```
___
### API проекта.
В папке `postman_collection` есть коллекция запросов, с которой можно ознакомится, например, в программе [Postman](https://www.postman.com/).<br>
В корне проекта есть файл `openapi.yml` или `openapi.json`- Подробное описание работы API проекта. Ознакомится можно, загрузив файл, например, на сайте [Swagger Editor](https://editor.swagger.io/).<br>

После запуска проекта в браузере можно будет открыть подобную документацию по адресу:
```
http://127.0.0.1:8000/docs
```
Так же есть документация в формате ReDoc, она доступна по адресу
```
http://127.0.0.1:8000/redoc:
```
___
Примеры запросов:<br>
___
Эндпоинт:
регистрация пользователя.
```
http://127.0.0.1:8000/auth/register
```
POST-запрос (JSON):
```
{
  "email": "user@example.com",
  "password": "string",
}
```
Ответ (JSON):
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
___
Эндпоинт:
получение токен для пользователя.
```
http://127.0.0.1:8000/auth/jwt/login
```
POST-запрос (application/x-www-form-urlencoded):
```
username: name@email.com
password: secret
```
Ответ (JSON):
```
{
  "access_token": "there_are_many_incomprehensible_signs_following_each_other",
  "token_type": "bearer"
}
```
___
Эндпоинт:
создание пожертвования.
```
http://127.0.0.1:8000//donation/
```
POST-запрос (JSON):
```
{
  "full_amount": 0,
  "comment": "string"
}
```
Ответ (JSON):
```
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2024-11-11T12:36:27.038Z"
}
```
___
### Информация об авторах.
Акчурин Лев Ливатович.<br>Студент курса Яндекс Практикума Python-разработчик плюс.<br>
[Страничка GitHub](https://github.com/levisserena)
___
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
