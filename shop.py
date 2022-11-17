import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, url_for, redirect, abort, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
from db_util import Database


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasgas097dsfsasdgbgd'
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config['DATABASE_URI'] = 'postgresql://gabnasyrov:Makalmak@localhost/web_shop'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
login_manager = LoginManager(app)

db = Database()

menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Профиль', 'url': '/profile'},
    {'name': 'Добавить товар', 'url': '/add_product'}
]

account = [
    {'name': 'Авторизация', 'url': '/login'},
    {'name': 'Регистрация', 'url': '/signup'}
]


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, db)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title='Главная', menu=menu, account=account, products=db.getProdAnonce())



@app.route('/profile')
@login_required
def catalog():
    return render_template("profile.html", title="Профиль", menu=menu, account=account)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():

    if request.method == "POST":
        res = db.addProd(request.form['name'], request.form['price'],
                         request.form['description'], request.files['img'].read())
        if not res:
            flash('Ошибка добавления товара')
        else:
            flash('Товар добавлен успешно')

    return render_template("add_product.html", title="Добавление продукта", menu=menu, account=account)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = db.getUserByLogin(request.form['login'])
        if user and check_password_hash(user[3], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('home'))

    return render_template("login.html", title="Авторизация", menu=menu, account=account)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if request.form['password'] == request.form['password_a']:
            psw = generate_password_hash(request.form['password'])
            res = db.addUser(request.form['name'], request.form['email'], request.form['login'], psw)
            if res:
                flash("Вы успешно зарегистрированы")
                return redirect(url_for('login'))
            else:
                flash("Ошибка регистрации")

    return render_template("signup.html", title="Регистрация", menu=menu, account=account)


# @app.route('/img_prod/<name>')
# def img_prod(name):
#     img = db.getImg(name)
#     if not img:
#         return ""
#
#     h = make_response(img)
#     h.headers['Content-Type'] = 'image/jpg'
#     return h


if __name__ == '__main__':
    app.run(debug=True)
