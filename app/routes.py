from flask import flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import admin_required, hash_password, verify_password
from app.database import db
from app.forms import (
    FuelItemForm,
    FuelTypeForm,
    IssueCreateForm,
    IssueRecordForm,
    LoginForm,
    UserCreateForm,
    UserEditForm,
)
from app.models import FuelItem, FuelType, IssueRecord, User


def fill_fuel_choices(form):
    form.fuel_type_id.choices = [(item.id, item.name) for item in FuelType.query.order_by(FuelType.name).all()]


def fill_issue_choices(form):
    form.fuel_item_id.choices = [(item.id, item.name) for item in FuelItem.query.order_by(FuelItem.name).all()]
    form.user_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()]


def register_routes(app):

    @app.route("/")
    def index():
        fuels = FuelItem.query.order_by(FuelItem.name).limit(6).all()
        last_page = request.cookies.get("last_page", "немає")
        response = make_response(render_template("index.html", fuels=fuels, last_page=last_page))
        response.set_cookie("last_page", "home", max_age=60 * 60 * 24 * 30)
        return response

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and verify_password(form.password.data, user.password_hash):
                login_user(user)
                flash(f"Вхід виконано: {user.full_name}.")
                return redirect(url_for("index"))
            flash("Невірний логін або пароль.")
        return render_template("login.html", form=form)

    @app.post("/logout")
    def logout():
        logout_user()
        flash("Ви вийшли із системи.")
        return redirect(url_for("index"))

    @app.route("/fuels")
    def fuels():
        fuel_items = FuelItem.query.order_by(FuelItem.name).all()
        return render_template("fuels/list.html", fuels=fuel_items)

    @app.route("/fuels/<int:fuel_id>")
    def fuel_detail(fuel_id):
        fuel = db.get_or_404(FuelItem, fuel_id)
        form = IssueCreateForm()
        return render_template("fuels/detail.html", fuel=fuel, form=form)

    @app.route("/admin/fuels/new", methods=["GET", "POST"])
    @admin_required
    def fuel_create():
        form = FuelItemForm()
        fill_fuel_choices(form)
        if form.validate_on_submit():
            fuel = FuelItem(
                name=form.name.data,
                supplier=form.supplier.data,
                quantity_liters=form.quantity_liters.data,
                unit_price=form.unit_price.data,
                fuel_type_id=form.fuel_type_id.data,
                description=form.description.data or "",
            )
            db.session.add(fuel)
            db.session.commit()
            flash("Позицію ПММ створено.")
            return redirect(url_for("fuels"))
        return render_template("fuels/form.html", form=form, title="Нова позиція ПММ")

    @app.route("/admin/fuels/<int:fuel_id>/edit", methods=["GET", "POST"])
    @admin_required
    def fuel_edit(fuel_id):
        fuel = db.get_or_404(FuelItem, fuel_id)
        form = FuelItemForm(obj=fuel)
        fill_fuel_choices(form)
        if form.validate_on_submit():
            fuel.name = form.name.data
            fuel.supplier = form.supplier.data
            fuel.quantity_liters = form.quantity_liters.data
            fuel.unit_price = form.unit_price.data
            fuel.fuel_type_id = form.fuel_type_id.data
            fuel.description = form.description.data or ""
            db.session.commit()
            flash("Позицію ПММ оновлено.")
            return redirect(url_for("fuel_detail", fuel_id=fuel.id))
        return render_template("fuels/form.html", form=form, title="Редагування ПММ")

    @app.post("/admin/fuels/<int:fuel_id>/delete")
    @admin_required
    def fuel_delete(fuel_id):
        fuel = db.get_or_404(FuelItem, fuel_id)
        if fuel.issue_records:
            flash("Неможливо видалити ПММ, бо для нього вже є операції видачі.")
            return redirect(url_for("fuels"))
        db.session.delete(fuel)
        db.session.commit()
        flash("Позицію ПММ видалено.")
        return redirect(url_for("fuels"))

    @app.route("/fuel-types")
    def fuel_types():
        types = FuelType.query.order_by(FuelType.name).all()
        return render_template("fuel_types/list.html", fuel_types=types)

    @app.route("/admin/fuel-types/new", methods=["GET", "POST"])
    @admin_required
    def fuel_type_create():
        form = FuelTypeForm()
        if form.validate_on_submit():
            db.session.add(FuelType(name=form.name.data, description=form.description.data or ""))
            db.session.commit()
            flash("Тип ПММ створено.")
            return redirect(url_for("fuel_types"))
        return render_template("fuel_types/form.html", form=form, title="Новий тип ПММ")

    @app.route("/admin/fuel-types/<int:type_id>/edit", methods=["GET", "POST"])
    @admin_required
    def fuel_type_edit(type_id):
        fuel_type = db.get_or_404(FuelType, type_id)
        form = FuelTypeForm(obj=fuel_type)
        if form.validate_on_submit():
            fuel_type.name = form.name.data
            fuel_type.description = form.description.data or ""
            db.session.commit()
            flash("Тип ПММ оновлено.")
            return redirect(url_for("fuel_types"))
        return render_template("fuel_types/form.html", form=form, title="Редагування типу ПММ")

    @app.post("/admin/fuel-types/<int:type_id>/delete")
    @admin_required
    def fuel_type_delete(type_id):
        fuel_type = db.get_or_404(FuelType, type_id)
        if fuel_type.fuels:
            flash("Неможливо видалити тип, бо до нього прив'язані позиції ПММ.")
            return redirect(url_for("fuel_types"))
        db.session.delete(fuel_type)
        db.session.commit()
        flash("Тип ПММ видалено.")
        return redirect(url_for("fuel_types"))

    @app.route("/issues")
    @login_required
    def issues():
        if current_user.role == "admin":
            all_issues = IssueRecord.query.order_by(IssueRecord.issued_at.desc()).all()
        else:
            all_issues = (
                IssueRecord.query.filter_by(user_id=current_user.id)
                .order_by(IssueRecord.issued_at.desc())
                .all()
            )
        return render_template("issues/list.html", issues=all_issues)

    @app.post("/fuels/<int:fuel_id>/issue")
    @login_required
    def issue_create(fuel_id):
        fuel = db.get_or_404(FuelItem, fuel_id)
        form = IssueCreateForm()
        if form.validate_on_submit():
            if fuel.quantity_liters < form.amount_liters.data:
                flash("Недостатній залишок на складі.")
                return redirect(url_for("fuel_detail", fuel_id=fuel.id))
            fuel.quantity_liters -= form.amount_liters.data
            db.session.add(
                IssueRecord(
                    user_id=current_user.id,
                    fuel_item_id=fuel.id,
                    amount_liters=form.amount_liters.data,
                    destination=form.destination.data,
                )
            )
            db.session.commit()
            flash("Операцію видачі створено.")
            return redirect(url_for("issues"))
        flash("Форма заповнена неправильно.")
        return redirect(url_for("fuel_detail", fuel_id=fuel.id))

    @app.route("/admin/issues/<int:issue_id>/edit", methods=["GET", "POST"])
    @admin_required
    def issue_edit(issue_id):
        issue = db.get_or_404(IssueRecord, issue_id)
        form = IssueRecordForm(obj=issue)
        fill_issue_choices(form)
        if form.validate_on_submit():
            issue.fuel_item_id = form.fuel_item_id.data
            issue.user_id = form.user_id.data
            issue.amount_liters = form.amount_liters.data
            issue.destination = form.destination.data
            db.session.commit()
            flash("Операцію оновлено.")
            return redirect(url_for("issues"))
        return render_template("issues/form.html", form=form, title="Редагування операції")

    @app.post("/admin/issues/<int:issue_id>/delete")
    @admin_required
    def issue_delete(issue_id):
        issue = db.get_or_404(IssueRecord, issue_id)
        db.session.delete(issue)
        db.session.commit()
        flash("Операцію видалено.")
        return redirect(url_for("issues"))

    # ---- Адмін панель ----

    @app.route("/admin")
    @admin_required
    def admin_dashboard():
        stats = {
            "users": User.query.count(),
            "fuel_types": FuelType.query.count(),
            "fuels": FuelItem.query.count(),
            "issues": IssueRecord.query.count(),
        }
        return render_template("admin/dashboard.html", stats=stats)

    @app.route("/admin/users")
    @admin_required
    def users():
        all_users = User.query.order_by(User.username).all()
        return render_template("users/list.html", users=all_users)

    @app.route("/admin/users/new", methods=["GET", "POST"])
    @admin_required
    def user_create():
        form = UserCreateForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                full_name=form.full_name.data,
                password_hash=hash_password(form.password.data),
                role=form.role.data,
            )
            db.session.add(user)
            db.session.commit()
            flash("Користувача створено.")
            return redirect(url_for("users"))
        return render_template("users/form.html", form=form, title="Новий користувач")

    @app.route("/admin/users/<int:user_id>/edit", methods=["GET", "POST"])
    @admin_required
    def user_edit(user_id):
        user = db.get_or_404(User, user_id)
        form = UserEditForm(obj=user)
        if form.validate_on_submit():
            user.username = form.username.data
            user.full_name = form.full_name.data
            user.role = form.role.data
            if form.password.data:
                user.password_hash = hash_password(form.password.data)
            db.session.commit()
            flash("Користувача оновлено.")
            return redirect(url_for("users"))
        return render_template("users/form.html", form=form, title="Редагування користувача")

    @app.post("/admin/users/<int:user_id>/delete")
    @admin_required
    def user_delete(user_id):
        if current_user.id == user_id:
            flash("Не можна видалити власний обліковий запис.")
            return redirect(url_for("users"))
        user = db.get_or_404(User, user_id)
        if user.issue_records:
            flash("Неможливо видалити користувача, бо для нього є операції видачі.")
            return redirect(url_for("users"))
        db.session.delete(user)
        db.session.commit()
        flash("Користувача видалено.")
        return redirect(url_for("users"))

