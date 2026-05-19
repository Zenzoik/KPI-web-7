# Лабораторна робота 7

Розширення ЛР6: Flask-застосунок з аутентифікацією через Flask-Login, панеллю адміністратора, класовою конфігурацією та надсиланням email через Flask-Mail.

## Що додано до ЛР6

- Flask-Login: `login_user`, `logout_user`, `@login_required`, `current_user`. Модель `User` успадковує `UserMixin`.
- Класова конфігурація: `Config` → `DevelopmentConfig` у `app/config.py`. `create_app()` приймає клас конфігурації.
- `app/extensions.py` — екземпляри `LoginManager` та `Mail` винесено окремо.
- Панель адміністратора `/admin` зі статистикою та посиланнями на управління всіма сутностями.
- Надсилання email-звіту залишків ПММ через Flask-Mail на сторінці `/admin/send-report`.

## Структура

```
app/
├── __init__.py     — create_app()
├── config.py       — Config, DevelopmentConfig
├── extensions.py   — login_manager, mail
├── models.py       — User (UserMixin), FuelType, FuelItem, IssueRecord
├── auth.py         — hash_password, admin_required
├── forms.py        — всі форми + SendReportForm
├── routes.py       — всі маршрути
└── seed.py         — початкові дані
templates/
└── admin/          — dashboard.html, send_report.html
```

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

## Email-звіт

Для надсилання email потрібно задати змінні середовища:

```bash
set MAIL_USERNAME=your@gmail.com
set MAIL_PASSWORD=your-app-password
set MAIL_DEFAULT_SENDER=your@gmail.com
```

Або просто перейти на `/admin/send-report` — якщо SMTP не налаштовано, застосунок покаже повідомлення про помилку.
