CREATE TRIGGER IF NOT EXISTS user2user_trigger
AFTER UPDATE ON wallet
WHEN NEW.bal < OLD.bal AND EXISTS (
    SELECT 1 FROM wallet 
    WHERE wallet_id != NEW.wallet_id 
    AND bal = (SELECT bal FROM wallet WHERE wallet_id = wallet.wallet_id) + (OLD.bal - NEW.bal)
)
BEGIN
    INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
    SELECT 
        OLD.wallet_id,
        (SELECT wallet_id FROM wallet WHERE bal = bal + ABS(NEW.bal - OLD.bal)),
        ABS(NEW.bal - OLD.bal),
        'User to User';
END;