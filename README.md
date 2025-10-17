# MoneyPal: A Digital Wallet Application

**Disclaimer:** This is a portfolio project created to demonstrate Database Managemet. It is not a real digital wallet.

MoneyPal is a web-based digital wallet application built with Python, Flask, and MySQL. It provides users with a simple way to manage their digital funds. The application focuses on efficient and secure database management.

## Features

* **User Authentication:** User registration and login functionality.
* **Wallet Management:** Users can deposit and withdraw funds from their wallets.
* **User-to-User Transactions:** Send money to other registered users.
* **Transaction History:** View a detailed history of all transactions.
* **Account Deletion:** Users have the option to delete their accounts.

## Technology Stack

* **Database:** MySQL

## Database Management

The core of MoneyPal's functionality lies in its database management system. The application utilizes a relational database schema with three main tables: `users`, `wallet`, and `transactions`.

### Schema

* **`users`:** Stores user information, including `user_id` (primary key), `first_name`, `last_name`, `username`, and a hashed `password` for security.
* **`wallet`:** Manages each user's wallet, linked to the `users` table via `wallet_id` (which is also a foreign key to `users.user_id`). This table tracks the current `bal` (balance), `last_transaction_type`, and `last_reciever_id`.
* **`transactions`:** Logs all transactions, with a `transaction_id` as the primary key. It includes `sender_id`, `receiver_id`, `amount`, `transaction_type`, and a `timestamp`.

### Triggers

To ensure data integrity and automate transaction logging, the database employs several triggers:

* **`userwallettrigger`:** Automatically creates a new wallet for a user upon registration.
* **`deposit_trigger`:** Logs a 'Deposit' transaction whenever a user's balance increases.
* **`withdraw_trigger`:** Logs a 'Withdraw' transaction whenever a user's balance decreases.
* **`user2user_trigger`:** Logs a 'User to User' transaction when money is transferred between users.

### SQL Queries

All database interactions are handled through parameterized SQL queries to prevent SQL injection vulnerabilities. The application uses a variety of queries for:

* **Creating, reading, updating, and deleting** user and wallet data.
* **Fetching transaction histories**.
* **Managing user sessions securely.**

## Installation and Setup

To run MoneyPal locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ashyx12/MoneyPal.git
    cd moneypal
    ```
2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up the MySQL database:**
    * Create a database named `wallet`.
    * Update the database credentials in `wallet.py`.
4.  **Run the application:**
    ```bash
    python wallet.py
    ```
5.  **Access the application** at `http://localhost:5000` in your web browser.
