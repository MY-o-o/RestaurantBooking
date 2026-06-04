# RestaurantBooking

RestaurantBooking is a Django restaurant booking MVP with reservations, menu browsing, an admin panel, REST API endpoints, GraphQL availability checks, WebSockets for live table updates, and bilingual UI support in English and Ukrainian.

## Features

- Django Admin for menu items, opening hours, halls, tables, and reservations
- REST API endpoints for menu, schedule, halls, tables, and reservations
- GraphQL endpoint with `availableTables(date, time, guests, zone)`
- WebSockets via Channels to update table status live on the booking page
- Authentication flows for register, login, logout, and password reset
- URL-based language support with `/en/` and `/uk/`
- Language switcher in the site header with persisted language choice

## Local Setup

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

## Main URLs

- `/` redirects to the user's preferred language
- `/en/` English home page
- `/uk/` Ukrainian home page
- `/en/menu/` or `/uk/menu/` menu page
- `/en/booking/` or `/uk/booking/` booking page
- `/en/admin/` or `/uk/admin/` admin panel
- `/en/api/` or `/uk/api/` REST API
- `/en/graphql/` or `/uk/graphql/` GraphQL endpoint

## Translation Workflow

The project uses Django's built-in internationalization framework.

- Template text is marked with `{% trans %}` and `{% blocktrans %}`
- Python strings use `gettext_lazy()`
- Ukrainian translations live in `locale/uk/LC_MESSAGES/django.po`
- Compiled translation files live in `locale/uk/LC_MESSAGES/django.mo`

If you change translatable text, regenerate translations with GNU gettext tools:

```powershell
python manage.py makemessages -l uk
python manage.py compilemessages
```

## GraphQL Example

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

## Notes

- `db.sqlite3` is intentionally ignored by git and should be created locally with `migrate`
- The current project has translated UI text, but dynamic database content still depends on the stored values
- For fully translated model content, consider `django-modeltranslation` or separate `*_en` / `*_uk` fields
