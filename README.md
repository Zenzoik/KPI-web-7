# Лабораторна робота 7

Розширення ЛР6: Flask-застосунок для "Обліку ПММ" з аутентифікацією через Flask-Login, панеллю адміністратора та класовою конфігурацією.

## Що додано до ЛР6

- Flask-Login: `login_user`, `logout_user`, `@login_required`, `current_user`. Модель `User` успадковує `UserMixin`.
- Класова конфігурація: `Config` → `DevelopmentConfig` у `app/config.py`. `create_app()` приймає клас конфігурації.
- `app/extensions.py` — `LoginManager` винесено окремо для уникнення циклічних імпортів.
- Панель адміністратора `/admin` зі статистикою та посиланнями на управління всіма сутностями.

## Запуск

```bash
cd lab7
python -m pip install -r requirements.txt
python -m flask --app main run --debug --port 8007
```

Після запуску:

- сайт: `http://127.0.0.1:8007/`
- адмін: `admin / admin123`
- користувач: `operator / user123`

## Міграції

У роботі вже є приклад початкової міграції в `migrations/versions/`.

Команди Flask-Migrate:

```bash
python -m flask --app main db upgrade
python -m flask --app main db migrate -m "Change models"
python -m flask --app main db upgrade
```
