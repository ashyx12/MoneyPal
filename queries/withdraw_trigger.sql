DELIMITER //

DROP TRIGGER IF EXISTS withdraw_trigger;

CREATE TRIGGER withdraw_trigger
AFTER UPDATE ON wallet
FOR EACH ROW
BEGIN
    IF OLD.bal > NEW.bal AND NEW.last_transaction_type = 2 THEN
        INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
        VALUES (NEW.wallet_id, NULL, OLD.bal - NEW.bal, "Withdraw");
    END IF;
END //

DELIMITER ;
