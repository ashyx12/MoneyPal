CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER,
    amount REAL NOT NULL,
    transaction_type TEXT CHECK(transaction_type IN ('Deposit', 'Withdraw', 'User to User')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES wallet(id),
    FOREIGN KEY (receiver_id) REFERENCES wallet(id)
);
