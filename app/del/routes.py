# -*- coding: utf-8 -*-

from app import app, db

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
#
#
# @app.route('/explore')
# @login_required
# def explore():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
#     prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
#     return render_template('main.html', title='Explore', posts=posts.items,
#                            next_url=next_url, prev_url=prev_url)
#
#
# @app.route('/', methods=['GET', "POST"])
# @login_required
# def main():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Ваша запись опубликована')
#         return redirect(url_for('main'))
#     # posts = current_user.followed_posts().all()
#     page = request.args.get('page', 1, type=int)
#     posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main', page=posts.next_num) if posts.has_next else None
#     prev_url = url_for('main', page=posts.prev_num) if posts.has_prev else None
#     return render_template('main.html', posts=posts.items, title='Главная страница',
#                            form=form, next_url=next_url, prev_url=prev_url)
#
#
# @app.route('/blog', methods=['GET'])
# @login_required
# def blog():
#     return render_template('blog.html')
#
#
# @app.route('/about', methods=['GET'])
# def about():
#     return render_template('about.html')
#
#
# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('user', username=user.username, page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('user', username=user.username, page=posts.prev_num) \
#         if posts.has_prev else None
#     form = EmptyForm()
#     return render_template('user.html', posts=posts.items, user=user, form=form, next_url=next_url, prev_url=prev_url)
#
#
# @app.route('/edit_profile', methods=['GET', "POST"])
# @login_required
# def edit_profile():
#     form = EditProfileForm(current_user.username)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         db.session.commit()
#         flash('Изменения успешно сохранены')
#         return redirect(url_for('edit_profile'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', form=form, title='Изменения профиля')
#
#
# @app.route('/follow/<username>', methods=['POST'])
# @login_required
# def follow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first()
#         if user is None:
#             flash(f'Пользователь {username} не найден')
#             return redirect(url_for('main'))
#         if user == current_user:
#             flash(f'Вы не можете подписаться на себя')
#             return redirect(url_for('user', username=username))
#         current_user.follow(user)
#         db.session.commit()
#         flash(f'Вы подписались на {username}!')
#         return redirect(url_for('user', username=username))
#     else:
#         return redirect(url_for('main'))
#
#
# @app.route('/unfollow/<username>', methods=['POST'])
# @login_required
# def unfollow(username):
#     form = EmptyForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=username).first()
#         if user is None:
#             flash(f'Пользователь {username} не найден')
#             return redirect(url_for('main'))
#         if user == current_user:
#             flash(f'Вы не можете отписаться от себя')
#             return redirect(url_for('user', username=username))
#         current_user.unfollow(user)
#         db.session.commit()
#         flash(f'Вы отписались от {username}!')
#         return redirect(url_for('user', username=username))
#     else:
#         return redirect(url_for('main'))