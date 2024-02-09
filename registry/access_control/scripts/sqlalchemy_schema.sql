CREATE TABLE IF NOT EXISTS userroles (
    record_id SERIAL PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    role_name VARCHAR(50) NOT NULL,
    create_by VARCHAR(50) NOT NULL,
    create_reason VARCHAR(50) NOT NULL,
    create_time TIMESTAMP NOT NULL,
    delete_by VARCHAR(50),
    delete_reason VARCHAR(50),
    delete_time TIMESTAMP
);

INSERT INTO userroles (project_name, user_name, role_name, create_by, create_reason, create_time) 
SELECT 'global', 'saumi', 'admin', 'saumya.bhatt@theporter.in', 'Initialize First Global Admin', CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM userroles 
    WHERE project_name = 'global' 
    AND user_name = 'saumi' 
    AND role_name = 'admin'
);
