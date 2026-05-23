# RestaurantBooking

Django MVP для модульного проєкту: система бронювання столиків у ресторані.

## Що реалізовано

- Django Admin для меню, графіку, залів, столиків і бронювань.
- REST API CRUD: `/api/menu/`, `/api/schedule/`, `/api/halls/`, `/api/tables/`, `/api/reservations/`.
- GraphQL endpoint: `/graphql/` із запитом `availableTables(date, time, guests, zone)`.
- WebSockets через Channels: `/ws/tables/` оновлює статус столика на сторінці бронювання.
- Frontend на Django Templates + CSS + Vanilla JS.
- Реєстрація, login/logout. Неавторизовані користувачі можуть дивитись меню і столики, але не можуть бронювати.

## Запуск локально

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Сторінки:

- `/` головна
- `/menu/` меню
- `/booking/` бронювання
- `/admin/` адмін-панель
- `/api/` REST API
- `/graphql/` GraphQL

## Приклад GraphQL

```graphql
query {
  availableTables(date: "2026-05-25", time: "18:00", guests: 4, zone: "VIP") {
    id
    number
    seats
    hall {
      name
      zone
    }
  }
}
```
