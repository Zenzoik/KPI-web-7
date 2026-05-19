from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Спочатку увійдіть у систему."

mail = Mail()
