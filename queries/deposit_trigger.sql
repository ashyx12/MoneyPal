DELIMITER //

DROP TRIGGER IF EXISTS deposit_trigger;

CREATE TRIGGER deposit_trigger
AFTER UPDATE ON wallet
FOR EACH ROW
BEGIN
    IF NEW.bal > OLD.bal AND NEW.last_transaction_type = 1 THEN
        INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
        VALUES (NEW.wallet_id, NULL, NEW.bal - OLD.bal, "Deposit");
    END IF;
END //

DELIMITER ;
