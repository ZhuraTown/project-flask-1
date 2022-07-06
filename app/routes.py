# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm
from app.models import User, Post
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('main.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/', methods=['GET', "POST"])
@login_required
def main():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваша запись опубликована')
        return redirect(url_for('main'))
    # posts = current_user.followed_posts().all()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main', page=posts.prev_num) if posts.has_prev else None
    return render_template('main.html', posts=posts.items, title='Главная страница',
                           form=form, next_url=next_url, prev_url=prev_url)


@app.route('/blog', methods=['GET'])
@login_required
def blog():
    return render_template('blog.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/register_user', methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация, прошла успешно')
        return redirect(url_for('main'))
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', posts=posts.items, user=user, form=form, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения успешно сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, title='Изменения профиля')


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'Пользователь {username} не найден')
            return redirect(url_for('main'))
        if user == current_user:
            flash(f'Вы не можете подписаться на себя')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'Вы подписались на {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('main'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'Пользователь {username} не найден')
            return redirect(url_for('main'))
        if user == current_user:
            flash(f'Вы не можете отписаться от себя')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'Вы отписались от {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('main'))


@app.route('/reset_password_request', methods=['GET', "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        redirect(url_for('main'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Следуйте инструкциям, поступившим на почту!')
        redirect(url_for('login'))
    return render_template('reset_password_request.html', form=form, title='Сброс пароля')


@app.route('/reset_password/<token>', methods=['GET', "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменён!')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)