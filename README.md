# Домашнє завдання #12

У цьому домашньому завданні ми продовжуємо допрацьовувати наш REST API застосунок із домашнього завдання 11.
Завдання:

- реалізуйте механізм аутентифікації в застосунку;
- реалізуйте механізм авторизації за допомогою JWT токенів, щоб усі операції з контактами проводились лише зареєстрованими користувачами;
- користувач має доступ лише до своїх операцій з контактами;

Загальні вимоги

- При реєстрації, якщо користувач вже існує з таким email, сервер поверне помилку HTTP 409 Conflict;
- Сервер хешує пароль і не зберігає його у відкритому вигляді в базі даних;
- У разі успішної реєстрації користувача сервер повинен повернути HTTP статус відповіді 201 Created та дані нового користувача;
- Для всіх операцій POST створення нового ресурсу, сервер повертає статус 201 Created;

# Домашнє завдання #11

Мета цього домашнього завдання — створити REST API для зберігання та управління контактами. API повинен бути побудований з використанням інфраструктури FastAPI та використовувати SQLAlchemy для управління базою даних.

Контакти повинні зберігатися в базі даних та містити в собі наступну інформацію:

- Ім'я
- Прізвище
- Електронна адреса
- Номер телефону
- День народження
- Додаткові дані (необов'язково)

API повинен мати можливість виконувати наступні дії:

- Створити новий контакт
- Отримати список всіх контактів
- Отримати один контакт за ідентифікатором
- Оновити існуючий контакт
- Видалити контакт

На придачу до базового функціоналу CRUD API також повинен мати наступні функції:

- Контакти повинні бути доступні для пошуку за іменем, прізвищем чи адресою електронної пошти (Query).


## Реалізація проекту

Встановлення додаткових модулів:

```
poetry add fastapi[all]
poetry add sqlalchemy
poetry add pytest
poetry add alembic
poetry add psycopg-binary
```

Створення Docker-контейнера для Postgres:
```
docker run --name pyweb-hw-11 -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
docker exec -it <id_container> bash
psql -U postgres
CREATE DATABASE contacts;
```

Налаштування міграцій
```
alembic init migrations
alembic revision --autogenerate -m 'init'
alembic upgrade head
```
