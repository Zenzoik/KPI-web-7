from app.auth import hash_password
from app.database import db
from app.models import FuelItem, FuelType, User


def seed_database():
    if User.query.count() == 0:
        db.session.add_all(
            [
                User(
                    username="admin",
                    full_name="Адміністратор",
                    password_hash=hash_password("admin123"),
                    role="admin",
                ),
                User(
                    username="operator",
                    full_name="Оператор складу",
                    password_hash=hash_password("user123"),
                    role="user",
                ),
            ]
        )

    if FuelType.query.count() == 0:
        diesel = FuelType(name="Дизель", description="Пальне для вантажного транспорту.")
        gasoline = FuelType(name="Бензин А-95", description="Пальне для легкових авто.")
        oil = FuelType(name="Моторна олива", description="Мастильні матеріали для техніки.")
        db.session.add_all([diesel, gasoline, oil])
        db.session.flush()

        db.session.add_all(
            [
                FuelItem(
                    name="Дизель Euro 5",
                    supplier="OKKO",
                    quantity_liters=5200,
                    unit_price=56,
                    description="Основний запас дизельного пального.",
                    fuel_type_id=diesel.id,
                ),
                FuelItem(
                    name="Бензин А-95 резерв",
                    supplier="WOG",
                    quantity_liters=2800,
                    unit_price=59,
                    description="Резерв для службових авто.",
                    fuel_type_id=gasoline.id,
                ),
                FuelItem(
                    name="Олива 10W-40",
                    supplier="Shell",
                    quantity_liters=650,
                    unit_price=185,
                    description="Олива для планового обслуговування.",
                    fuel_type_id=oil.id,
                ),
            ]
        )

    db.session.commit()
