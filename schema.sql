-- =============================================================
-- Database Schema — fastapi_crud
-- =============================================================
-- Run this manually OR let SQLAlchemy / Alembic create it.
-- Tested on PostgreSQL 15+
-- =============================================================

-- Create the database (run as a superuser, outside a transaction)
-- CREATE DATABASE crud_db;

-- ---------------------------------------------------------------
-- Table: users
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL          PRIMARY KEY,
    username    VARCHAR(50)     NOT NULL UNIQUE,
    email       VARCHAR(255)    NOT NULL UNIQUE,
    full_name   VARCHAR(100),
    is_active   BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Speed up lookups by username and email
CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);
CREATE INDEX IF NOT EXISTS ix_users_email    ON users (email);

-- ---------------------------------------------------------------
-- Table: tasks
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id           SERIAL          PRIMARY KEY,
    title        VARCHAR(200)    NOT NULL,
    description  TEXT,
    is_completed BOOLEAN         NOT NULL DEFAULT FALSE,
    owner_id     INTEGER         NOT NULL
                                 REFERENCES users(id) ON DELETE CASCADE,
    created_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Speed up "all tasks for user X" queries
CREATE INDEX IF NOT EXISTS ix_tasks_owner_id ON tasks (owner_id);

-- ---------------------------------------------------------------
-- Trigger: auto-update updated_at on row change
-- ---------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER trg_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------
-- Sample seed data (optional)
-- ---------------------------------------------------------------
INSERT INTO users (username, email, full_name) VALUES
    ('alice',   'alice@example.com',   'Alice Smith'),
    ('bob',     'bob@example.com',     'Bob Jones'),
    ('charlie', 'charlie@example.com', 'Charlie Brown')
ON CONFLICT DO NOTHING;

INSERT INTO tasks (title, description, owner_id) VALUES
    ('Buy groceries',     'Milk, eggs, bread',            1),
    ('Write unit tests',  'Cover service layer',           1),
    ('Read FastAPI docs', 'Focus on dependency injection', 2),
    ('Fix login bug',     'JWT expiry not refreshing',     3)
ON CONFLICT DO NOTHING;