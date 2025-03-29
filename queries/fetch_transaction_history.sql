SELECT
    t.transaction_id,
    t.sender_id, 
    t.receiver_id, 
    t.amount, 
    t.transaction_type,
    t.timestamp
FROM 
    transactions t
WHERE 
    (t.sender_id = %s) OR (t.receiver_id = %s)
ORDER BY 
    t.timestamp DESC;
    