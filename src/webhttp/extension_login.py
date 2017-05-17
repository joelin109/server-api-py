from flask import render_template, Blueprint, redirect, url_for, flash, g
from flask_login import LoginManager, login_user, logout_user
from flask_principal import Principal, Permission, RoleNeed
from src.service.model.model_account import User
from src.service.logic.user_logic import UserLogic

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

_login_endpoint = "login"
login_manager = LoginManager()
login_manager.login_view = _login_endpoint
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

_principal = Principal()
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False
        else:
            # Does our the exist
            _logic = UserLogic()
            _user = _logic.get_detail_by_auth(self.username.data)

            if not _user:
                self.username.errors.append('Invalid username or password')
                return False
            else:
                return True
                # Do the passwords match
                if not _user.check_password(self.password.data):
                    self.username.errors.append('Invalid username or password')
                    return False
                else:
                    return True


@login_manager.user_loader
def load_user(user_id):
    _logic = UserLogic()
    _user = _logic.get_detail(user_id)
    print("extension_login: load_user")
    return _user


# @auth_blueprint.route('/login', methods=['GET', 'POST'])
def login(page=1):
    _form = LoginForm()

    if _form.validate_on_submit():
        _logic = UserLogic()
        _user = _logic.get_detail_by_auth(_form.username.data)

        login_user(_user, remember=_form.remember.data)

        flash("You have been logged in.", category="success")
        return redirect(url_for('home.admin'))

    return render_template('user/login.html', form=_form)


def logout():
    logout_user()
    return redirect(url_for('content.deutsch'))


def register_login(app):
    app.add_url_rule('/login', _login_endpoint, login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])

    login_manager.init_app(app)
    _principal.init_app(app)
    # app.register_blueprint(auth_blueprint, url_prefix='')
