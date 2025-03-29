INSERT INTO users (first_name, last_name, username, password_hashed, created_at) 
VALUES (%s, %s, %s, %s, NOW());
