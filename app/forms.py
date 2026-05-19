from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Увійти")


class UserCreateForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=2, max=50)])
    full_name = StringField("ПІБ", validators=[DataRequired(), Length(min=2, max=120)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=100)])
    role = SelectField("Роль", choices=[("user", "user"), ("admin", "admin")])
    submit = SubmitField("Зберегти")


class UserEditForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=2, max=50)])
    full_name = StringField("ПІБ", validators=[DataRequired(), Length(min=2, max=120)])
    password = PasswordField("Новий пароль", validators=[Optional(), Length(min=4, max=100)])
    role = SelectField("Роль", choices=[("user", "user"), ("admin", "admin")])
    submit = SubmitField("Зберегти")


class FuelTypeForm(FlaskForm):
    name = StringField("Назва", validators=[DataRequired(), Length(min=2, max=80)])
    description = TextAreaField("Опис", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Зберегти")


class FuelItemForm(FlaskForm):
    name = StringField("Найменування", validators=[DataRequired(), Length(min=2, max=120)])
    supplier = StringField("Постачальник", validators=[DataRequired(), Length(min=2, max=120)])
    quantity_liters = IntegerField("Залишок, літри", validators=[DataRequired(), NumberRange(min=0)])
    unit_price = IntegerField("Ціна за літр, грн", validators=[DataRequired(), NumberRange(min=0)])
    fuel_type_id = SelectField("Тип ПММ", coerce=int, validators=[DataRequired()])
    description = TextAreaField("Опис", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Зберегти")


class IssueRecordForm(FlaskForm):
    fuel_item_id = SelectField("ПММ", coerce=int, validators=[DataRequired()])
    user_id = SelectField("Користувач", coerce=int, validators=[DataRequired()])
    amount_liters = IntegerField("Обсяг, літри", validators=[DataRequired(), NumberRange(min=1)])
    destination = StringField("Куди видано", validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField("Зберегти")


class IssueCreateForm(FlaskForm):
    amount_liters = IntegerField("Обсяг, літри", validators=[DataRequired(), NumberRange(min=1)])
    destination = StringField("Куди видано", validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField("Оформити видачу")


class SendReportForm(FlaskForm):
    email = StringField("Email адреса", validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField("Надіслати звіт")
