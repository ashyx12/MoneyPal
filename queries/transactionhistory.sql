SELECT
    t.id,
    t.sender_id, 
    t.receiver_id, 
    t.amount, 
    t.transaction_type,
    t.timestamp
FROM 
    transactions t
WHERE 
    (t.sender_id = ?) OR (t.receiver_id = ?)
ORDER BY 
    t.timestamp DESC;
