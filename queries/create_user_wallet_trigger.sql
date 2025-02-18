CREATE TRIGGER IF NOT EXISTS userwallettrigger
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO wallet (wallet_id, username, bal, last_transaction_type) VALUES (NEW.user_id, NEW.username, 0.00, NULL);
END;