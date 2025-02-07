from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

wallet = Flask(__name__)
wallet.config['KEY'] = 'key'
wallet.secret_key = wallet.config['KEY']
wallet.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallet.db'
data = SQLAlchemy(wallet)

class Wallet(data.Model):
  
    id = data.Column(data.Integer, primary_key = True)
    username = data.Column(data.String(20), unique = True, nullable = False)
    password = data.Column(data.String(20), nullable = False)
    bal = data.Column(data.Float, default = 0.00)

@wallet.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method = 'pbkdf2:sha256', salt_length = 8)
        new_wallet = Wallet(username = username, password = password)
        data.session.add(new_wallet)
        data.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@wallet.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        wallet_user = Wallet.query.filter_by(username = username).first()
        
        if wallet_user and check_password_hash(wallet_user.password, password):
            session['user_id'] = wallet_user.id
        return redirect(url_for('wallet_view'))
    
    return render_template('login.html')

@wallet.route('/wallet', methods = ['GET', 'POST'])
def wallet_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    wallet_user = Wallet.query.filter_by(id = session['user_id']).first()

    if request.method == 'POST':
        if 'deposit' in request.form:
            amount = float(request.form['amount'])
            wallet_user.bal += amount
        elif 'withdraw' in request.form:
            amount = float(request.form['amount'])
            if wallet_user.bal >= amount:
                wallet_user.bal -= amount
        data.session.commit()
    return render_template('wallet.html', user = wallet_user)

if  __name__ == '__main__':
    with wallet.app_context():
        data.create_all()
    wallet.run(debug = True)