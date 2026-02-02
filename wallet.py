import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

wallet = Flask(__name__)
wallet.config['DATABASE'] = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}
wallet.secret_key = 'secret_key'

def get_db():
    db = mysql.connector.connect(**wallet.config['DATABASE'])
    return db

def load_sql_file(sqlfile):
    with open(os.path.join(os.path.dirname(__file__), 'queries', sqlfile), 'r') as sqlfile:
        return sqlfile.read()


def init_db():
    db = get_db()
    command = db.cursor(dictionary=True)

    # create_user_sql = load_sql_file('create_users_table.sql')
    # command.execute(create_user_sql)

    # create_table_sql = load_sql_file('create_wallet_table.sql')
    # command.execute(create_table_sql)

    # try:
    #     create_trigger_sql = load_sql_file('create_user_wallet_trigger.sql')
    #     command.execute(create_trigger_sql)
    # except Exception as e:
    #     print("Error creating user_wallet trigger:", e)


    if not db.is_connected():
        db.reconnect(attempts=3, delay=2)

    # create_transaction_table_sql = load_sql_file('create_transactions_table.sql')
    # command.execute(create_transaction_table_sql)

    if not db.is_connected():
        db.reconnect(attempts=3, delay=2)

    # create_deposit_trigger = load_sql_file('deposit_trigger.sql')
    # command.execute(create_deposit_trigger)

    # if not db.is_connected():
    #     db.reconnect(attempts=3, delay=2)

    # create_withdraw_trigger = load_sql_file('withdraw_trigger.sql')
    # command.execute(create_withdraw_trigger)

    # if not db.is_connected():
    #     db.reconnect(attempts=3, delay=2)

    # create_user2user_trigger = load_sql_file('user2user_trigger.sql')
    # command.execute(create_user2user_trigger)

    # insert_sql = load_sql_file('insert_into_users.sql')
    # update_bal_sql = load_sql_file('update_balance.sql')

    # for i in range(100):
    #     password = str(i + 1)
    #     hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    #     if not db.is_connected():
    #         db.reconnect(attempts=3, delay=2)

    #     try:
    #         command = db.cursor(dictionary=True)

    #         command.execute(insert_sql, (f'First{i+1}', f'Last{i+1}', i+1, hashed_password))
    #         db.commit() 

    #         command.execute(update_bal_sql, (float(10000), int(1), None, int(i+1)))
    #         db.commit()

    #         command.close()

    #     except mysql.connector.IntegrityError:
    #         db.commit()

    db.close()


@wallet.route('/')
def home():
    return redirect('/signup')

@wallet.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        db = get_db()
        db.start_transaction()
        command = db.cursor(dictionary=True)

        try:
            insert_sql = load_sql_file('insert_into_users.sql')
            command.execute(insert_sql, (first_name, last_name, username, hashed_password))
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            db.rollback()
            return render_template('signup.html', error="Username Taken!")
        except Exception:
            db.rollback()
            return render_template('signup.html', error="Something Went Wronf")
        finally:
            db.close()

    return render_template('signup.html')

@wallet.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        command = db.cursor(dictionary=True)

        select_acc_sql = load_sql_file('select_from_username_in_users.sql')
        command.execute(select_acc_sql, (username,))
        wallet_user = command.fetchone()
        db.close()

        if wallet_user and check_password_hash(wallet_user['password_hashed'], password):
            session['user_id'] = wallet_user['user_id']
            return redirect(url_for('wallet_view'))
        else:
            return render_template('login.html', error="Invalid Username or Password")
    
    return render_template('login.html')

@wallet.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

@wallet.route('/wallet', methods=['GET', 'POST'])
def wallet_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db = get_db()
    command = db.cursor(dictionary=True)

    command.execute(load_sql_file('select_from_id_in_users.sql'), (user_id,))
    user_users = command.fetchone()
    command.execute(load_sql_file('select_from_id_in_wallet.sql'), (user_id,))
    user_wallet = command.fetchone()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        
        try:
            db.start_transaction()
            
            command.execute("SELECT bal, wallet_id FROM wallet WHERE wallet_id = %s FOR UPDATE", (user_id,))
            current_wallet = command.fetchone()

            if 'deposit' in request.form:
                if amount <= 0:
                    db.rollback()
                    return render_template('wallet.html', user_users=user_users, user_wallet=user_wallet, error="Invalid Amount")
                
                new_balance = float(current_wallet['bal']) + amount
                update_bal_sql = load_sql_file('update_balance.sql')
                command.execute(update_bal_sql, (float(new_balance), int(1), None, int(user_wallet['wallet_id'])))
                db.commit()

            elif 'withdraw' in request.form:
                if amount <= 0 or current_wallet['bal'] < amount:
                    db.rollback()
                    return render_template('wallet.html', user_users=user_users, user_wallet=user_wallet, error="Insufficient funds or invalid amount")
                
                new_balance = float(current_wallet['bal']) - amount
                update_bal_sql = load_sql_file('update_balance.sql')
                command.execute(update_bal_sql, (new_balance, int(2), None, user_wallet['wallet_id']))
                db.commit() 

            db.close()
            return redirect(url_for('wallet_view'))

        except Exception as e:
            db.rollback()
            return render_template('wallet.html', user_users=user_users, user_wallet=user_wallet, error="System Error")
        finally:
            if db.is_connected():
                db.close()

    db.close()
    return render_template('wallet.html', user_users=user_users, user_wallet=user_wallet)

@wallet.route('/deleteacc', methods=['GET', 'POST'])
def deleteacc():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return render_template('deleteacc.html', error="Passwords Don't Match")

        db = get_db()
        db.start_transaction()
        command = db.cursor(dictionary=True)

        try:
            select_acc_sql = load_sql_file('select_from_username_in_users.sql')
            command.execute(select_acc_sql, (username,))
            wallet_user = command.fetchone()       

            if wallet_user and check_password_hash(wallet_user['password_hashed'], password1) and session['user_id'] == wallet_user['user_id']:
                delete_wallet_sql = load_sql_file('delete_from_wallet.sql')
                command.execute(delete_wallet_sql, (wallet_user['user_id'],))

                delete_user_sql = load_sql_file('delete_from_users.sql')
                command.execute(delete_user_sql, (wallet_user['user_id'],))
                
                db.commit()
                session.clear() 
                return redirect(url_for('signup'))
            else:
                db.rollback()
                return render_template('deleteacc.html', error="Invalid Username or Password")

        except Exception as e:
            db.rollback()
            print(f"Delete failed: {e}")
            return render_template('deleteacc.html', error="Operation Failed")
        finally:
            db.close()
        
    return render_template('deleteacc.html')

@wallet.route('/user2user', methods=['GET', 'POST'])
def user2user():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        username = request.form['username']
        amount = float(request.form['amount'])

        db = get_db()
        db.start_transaction()
        command = db.cursor(dictionary=True)

        try:
            command.execute("SELECT bal FROM wallet WHERE wallet_id = %s FOR UPDATE", (user_id,))
            sender_wallet = command.fetchone()

            command.execute("SELECT wallet_id, bal FROM wallet WHERE username = %s FOR UPDATE", (username,))
            receiver_wallet = command.fetchone()

            if not receiver_wallet:
                db.rollback()
                return render_template('transactions.html', error="Receiver Not Found")
            
            if receiver_wallet['wallet_id'] == user_id:
                db.rollback()
                return render_template('transactions.html', error="Cannot send to yourself")

            if sender_wallet['bal'] < amount or amount <= 0:
                db.rollback()
                return render_template('transactions.html', error="Insufficient Balance or Invalid Amount")

            update_bal_sql = load_sql_file('update_balance.sql')
            
            new_sender_bal = float(sender_wallet['bal']) - amount
            command.execute(update_bal_sql, (new_sender_bal, 3, receiver_wallet['wallet_id'], user_id))

            new_receiver_bal = float(receiver_wallet['bal']) + amount
            command.execute(update_bal_sql, (new_receiver_bal, 3, None, receiver_wallet['wallet_id']))

            db.commit()
            return render_template('transactions.html', success="Transaction Successful!")

        except Exception as e:
            db.rollback()
            return render_template('transactions.html', error="Transaction Failed")
        finally:
            db.close()

    return render_template('transactions.html')

@wallet.route('/transaction_history')
def transaction_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    db = get_db()
    command = db.cursor(dictionary=True)

    transaction_history_sql = load_sql_file('fetch_transaction_history.sql')
    command.execute(transaction_history_sql, (user_id, user_id))
    transaction_history = command.fetchall()

    user_users_sql = load_sql_file('select_from_id_in_users.sql')
    command.execute(user_users_sql, (user_id,))
    username = command.fetchone()

    db.close()

    final_transactions = []
    seen = set()

    for transaction in transaction_history:
        if transaction['transaction_id'] not in seen:
            final_transactions.append(transaction)
            seen.add(transaction['transaction_id'])

    return render_template('transactionhistory.html', transactions = final_transactions, username = username['username'], id = user_id)

if __name__ == '__main__':
    init_db()
    wallet.run(host='0.0.0.0', port=5000, debug=False)
