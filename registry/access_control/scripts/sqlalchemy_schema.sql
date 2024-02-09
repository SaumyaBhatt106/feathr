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
