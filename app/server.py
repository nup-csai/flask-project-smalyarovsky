import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, \
    current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    meal = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    proteins = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    time = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash("Invalid credentials")
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is taken', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def root():
    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    foods = Food.query.filter_by(user_id=current_user.id)
    snacks = foods.filter_by(meal=False).order_by(Food.time.desc()).all()
    meals = foods.filter_by(meal=True).order_by(Food.time.desc()).all()
    total_spend, daily_spend = 0, 0
    calories_by_day = {}
    proteins_by_day = {}
    fats_by_day = {}

    for food in foods:
        if food.calories:
            calories_by_day[int(food.time)] = calories_by_day.get(int(food.time), 0) + int(food.calories)
            proteins_by_day[int(food.time)] = proteins_by_day.get(int(food.time), 0) + int(food.proteins or 0)
            fats_by_day[int(food.time)] = fats_by_day.get(int(food.time), 0) + int(food.fats or 0)
        if food.price:
            total_spend += food.price

    days = len(calories_by_day)
    total_calories = sum(calories_by_day.values())
    total_proteins = sum(proteins_by_day.values())
    total_fats = sum(fats_by_day.values())
    daily_calories = total_calories / days if days > 0 else 0
    daily_proteins = total_proteins / days if days > 0 else 0
    daily_fats = total_fats / days if days > 0 else 0
    daily_spend = total_spend / days if days > 0 else 0

    return render_template(
        'home.html',
        snacks=snacks,
        meals=meals,
        total_spend=total_spend,
        daily_spend=daily_spend,
        daily_calories=daily_calories,
        daily_proteins=daily_proteins,
        daily_fats=daily_fats,
        datetime=datetime,
    )


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        meal = request.form['meal'] == 'True'
        price = request.form.get('price', type=float)
        calories = request.form.get('calories', type=int)
        proteins = request.form.get('proteins', type=int)
        fats = request.form.get('fats', type=int)
        time = datetime.strptime(request.form.get('time'), "%Y-%m-%d").timestamp()

        new_food = Food(
            name=name,
            meal=meal,
            price=price,
            calories=calories,
            proteins=proteins,
            fats=fats,
            time=time,
            user_id=current_user.id
        )
        db.session.add(new_food)
        db.session.commit()
        flash('Food added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(port=8080)
