CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL NOT NULL
);

INSERT INTO products (name, price) VALUES
    ('Помидоры', 130.00),
    ('Огурцы', 99.10),
    ('Бананы', 200.99)
ON CONFLICT (id) DO NOTHING;