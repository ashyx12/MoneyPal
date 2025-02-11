CREATE TRIGGER IF NOT EXISTS withdraw_trigger
AFTER UPDATE ON wallet
WHEN NEW.bal < OLD.bal AND NEW.wallet_id = OLD.wallet_id
AND NOT EXISTS (
    SELECT 1 FROM transactions
    WHERE transaction_type = 'User to User'
    AND sender_id = NEW.wallet_id
)
BEGIN
    INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
    VALUES (NEW.wallet_id, NEW.wallet_id, OLD.bal - NEW.bal, 'Withdraw');
END;