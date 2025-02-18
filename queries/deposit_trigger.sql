CREATE TRIGGER IF NOT EXISTS deposit_trigger
AFTER UPDATE ON wallet
WHEN NEW.bal > OLD.bal AND NEW.last_transaction_type = 1
BEGIN
    INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
    VALUES (NEW.wallet_id, NULL, NEW.bal - OLD.bal, 'Deposit');
END;
