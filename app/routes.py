# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, flash

from app import app
from app.forms import LoginForm


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# @app.route('/auth', methods=['GET'])
# def auth():
#     return render_template('auth.html')


@app.route('/register_user', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        print('lala')
        return render_template('register_form.html')
    elif request.method == "GET":
        return render_template('register_form.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('main'))
    return render_template('login.html', title='Sign In', form=form)
