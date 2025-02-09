CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id VARCHAR(20) NOT NULL,
    receiver_id VARCHAR(20),
    amount REAL NOT NULL,
    transaction_type VARCHAR(20),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES wallet(id),
    FOREIGN KEY (receiver_id) REFERENCES wallet(id)
);