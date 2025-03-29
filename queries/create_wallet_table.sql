CREATE TABLE IF NOT EXISTS wallet (
    wallet_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    bal DECIMAL(10, 2) DEFAULT 0.00,
    last_transaction_type INT,
    last_reciever_id INT,
    FOREIGN KEY (wallet_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users(username)
);
