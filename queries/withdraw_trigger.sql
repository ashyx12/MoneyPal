CREATE TRIGGER IF NOT EXISTS withdraw_trigger
AFTER UPDATE ON wallet
WHEN OLD.bal > NEW.bal AND NEW.last_transaction_type = 2
BEGIN
    INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
    VALUES (NEW.wallet_id, NULL, OLD.bal - NEW.bal, 'Withdraw');
END;
