CREATE TABLE IF NOT EXISTS wallet 
(
    wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    bal REAL DEFAULT 0.00,
    last_transaction_type INTEGER,
    last_reciever_id INTEGER,
    FOREIGN KEY (wallet_id) REFERENCES users(user_id) ON DELETE CASCADE
);