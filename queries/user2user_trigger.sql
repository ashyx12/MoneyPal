DELIMITER //

DROP TRIGGER IF EXISTS user2user_trigger;

CREATE TRIGGER user2user_trigger
AFTER UPDATE ON wallet
FOR EACH ROW
BEGIN
    IF NEW.bal < OLD.bal AND NEW.last_transaction_type = 3 THEN
        INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
        VALUES (OLD.wallet_id, (SELECT wallet_id FROM wallet WHERE wallet_id = NEW.last_reciever_id LIMIT 1), ABS(NEW.bal - OLD.bal), "User to User");
    END IF;
END //

DELIMITER ;
