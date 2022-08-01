
from werkzeug.urls import url_parse

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm

from app import db
from app.auth import bp

from app.models import User
from app.email import send_password_reset_email


@bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.main')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.main'))


@bp.route('/register_user', methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация, прошла успешно')
        return redirect(url_for('main.main'))
    return render_template('auth/register_form.html', title='Регистрация', form=form)


@bp.route('/reset_password_request', methods=['GET', "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        redirect(url_for('main.main'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Следуйте инструкциям, поступившим на почту!')
        redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form, title='Сброс пароля')


@bp.route('/reset_password/<token>', methods=['GET', "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.main"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.main'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменён!')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)