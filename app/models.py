from datetime import datetime

from flask_login import UserMixin

from app.database import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    issue_records = db.relationship("IssueRecord", back_populates="user")


class FuelType(db.Model):
    __tablename__ = "fuel_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, default="")

    fuels = db.relationship("FuelItem", back_populates="fuel_type")


class FuelItem(db.Model):
    __tablename__ = "fuel_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    supplier = db.Column(db.String(120), nullable=False)
    quantity_liters = db.Column(db.Integer, default=0, nullable=False)
    unit_price = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.Text, default="")
    fuel_type_id = db.Column(db.Integer, db.ForeignKey("fuel_types.id"), nullable=False)

    fuel_type = db.relationship("FuelType", back_populates="fuels")
    issue_records = db.relationship("IssueRecord", back_populates="fuel_item")


class IssueRecord(db.Model):
    __tablename__ = "issue_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fuel_item_id = db.Column(db.Integer, db.ForeignKey("fuel_items.id"), nullable=False)
    amount_liters = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="issue_records")
    fuel_item = db.relationship("FuelItem", back_populates="issue_records")
