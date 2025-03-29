CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT DEFAULT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('Deposit', 'Withdraw', 'User to User') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES wallet(wallet_id),
    FOREIGN KEY (receiver_id) REFERENCES wallet(wallet_id)
);