INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?, datetime(CURRENT_TIMESTAMP, 'localtime'));
