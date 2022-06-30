from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')


@app.route('/register_user', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        print('lala')
        return render_template('register_form.html')
    elif request.method == "GET":
        return render_template('register_form.html')


if __name__ == "__main__":
    app.run(debug=True)