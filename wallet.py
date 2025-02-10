import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

wallet = Flask(__name__)
wallet.config['DATABASE'] = 'instance/wallet.db'
wallet.secret_key = 'secret_key'

def get_db():
    db = sqlite3.connect(wallet.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def load_sql_file(sqlfile):
    with open(os.path.join(os.path.dirname(__file__), 'queries', sqlfile), 'r') as sqlfile:
        return sqlfile.read()


def init_db():
    db = get_db()
    command = db.cursor()

    create_table = load_sql_file('createtable.sql')
    command.execute(create_table)

    create_transaction_table = load_sql_file('createtransactiontable.sql')
    command.execute(create_transaction_table)

    db.commit()
    # create = load_sql_file('insert.sql')
    # record_transaction = load_sql_file('recordtransaction.sql')

    # for i in range(100):
    #     password = str(i + 1)
    #     hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    #     try:
    #         command.execute(create, (f'First{i+1}', f'Last{i+1}', i+1, hashed_password, 10000.00))
    #         command.execute(record_transaction, (i+1, None, 10000.00, 'Deposit'))
    #         db.commit()
    #     except sqlite3.IntegrityError:
    #         db.commit()
    db.close()
    

@wallet.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        db = get_db()
        command = db.cursor()

        insert = load_sql_file('insert.sql')

        try:
            command.execute(insert, (first_name, last_name, username, hashed_password, 0.00)) 
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username Unavailable")
        finally:
            db.close()

    return render_template('signup.html')

@wallet.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        command = db.cursor()

        select_acc = load_sql_file('selectfromusername.sql')
        command.execute(select_acc, (username,))
        wallet_user = command.fetchone()
        db.close()

        if wallet_user and check_password_hash(wallet_user['password'], password):
            session['user_id'] = wallet_user['id']
            return redirect(url_for('wallet_view'))
        else:
            return render_template('login.html', error="Invalid Username or Password")
    
    return render_template('login.html')

@wallet.route('/wallet', methods=['GET', 'POST'])
def wallet_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    command = db.cursor()
    select_acc = load_sql_file('selectfromid.sql')
    command.execute(select_acc, (session['user_id'],))
    wallet_user = command.fetchone()
    db.close()

    if request.method == 'POST':
        amount = float(request.form['amount'])

        if 'deposit' in request.form:
            if amount <= 0:
                return render_template('wallet.html', user=wallet_user, error="Amount can't be Negative or Zero")
            
            new_balance = wallet_user['bal'] + amount

            db = get_db()
            command = db.cursor()

            update_bal = load_sql_file('updatebalance.sql')
            command.execute(update_bal, (new_balance, wallet_user['id']))
            record_transaction = load_sql_file('recordtransaction.sql')
            command.execute(record_transaction, (wallet_user['id'], None, amount, 'Deposit'))

            db.commit()
            db.close()
            return redirect(url_for('wallet_view'))

        elif 'withdraw' in request.form:
            if amount <= 0:
                return render_template('wallet.html', user=wallet_user, error="Amount can't be Negative or Zero")
            
            if wallet_user['bal'] >= amount:
                new_balance = wallet_user['bal'] - amount

                db = get_db()
                command = db.cursor()

                update_bal = load_sql_file('updatebalance.sql')
                command.execute(update_bal, (new_balance, wallet_user['id']))
                record_transaction = load_sql_file('recordtransaction.sql')
                command.execute(record_transaction, (wallet_user['id'], None, amount, 'Withdraw'))

                db.commit()
                db.close()
                return redirect(url_for('wallet_view'))
            else:
                return render_template('wallet.html', user=wallet_user, error="Insufficient balance")

    db = get_db()
    command = db.cursor()
    command.execute(select_acc, (session['user_id'],))
    wallet_user = command.fetchone()
    db.close()

    return render_template('wallet.html', user=wallet_user)

@wallet.route('/user2user', methods=['GET', 'POST'])
def user2user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form['username']
        amount = float(request.form['amount'])

        db = get_db()
        command = db.cursor()
        sender_acc = load_sql_file('selectfromid.sql')

        command.execute(sender_acc, (user_id,))
        wallet_user = command.fetchone()

        if wallet_user['bal'] < amount:
            return render_template('transactions.html', error="Insufficient Balance")
        
        if amount <= 0:
            return render_template('transactions.html', error="Amount can't be Negative or Zero")
        
        receiver_exists = load_sql_file('selectfromusername.sql')
        command.execute(receiver_exists, (username,))
        reciever = command.fetchone()

        if reciever:
            update_bal = load_sql_file('updatebalance.sql')
            new_balance_sender = wallet_user['bal'] - amount
            command.execute(update_bal, (new_balance_sender, user_id))

            new_balance_receiver = reciever['bal'] + amount
            command.execute(update_bal, (new_balance_receiver, reciever['id']))

            record_transaction = load_sql_file('recordtransaction.sql')
            command.execute(record_transaction, (user_id, reciever['id'], amount, 'User to User'))
            
            db.commit()
            db.close()

            return render_template('transactions.html', success="Transaction Successful!")
        else:
            db.close()
            return render_template('transactions.html', error="Reciever Not Found")

    return render_template('transactions.html')

@wallet.route('/transaction_history')
def transaction_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    db = get_db()
    command = db.cursor()

    history = load_sql_file('transactionhistory.sql')
    command.execute(history, (user_id, user_id))
    transactions = command.fetchall()

    username_fetch = load_sql_file('selectfromid.sql')
    command.execute(username_fetch, (user_id,))
    username = command.fetchone()

    db.close

    final_transactions = []
    seen = set()

    for transaction in transactions:
        if transaction['id'] not in seen:
            final_transactions.append(transaction)
            seen.add(transaction['id'])

    return render_template('transactionhistory.html', transactions = final_transactions, username = username['username'], id = user_id)

if __name__ == '__main__':
    init_db()
    wallet.run(debug=True)
