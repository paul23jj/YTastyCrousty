CREATE TABLE
    restaurants (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL,
        address VARCHAR(100) NOT NULL,
        is_open BOOLEAN NOT NULL,
        opening_hours VARCHAR(100) NOT NULL,
        contact VARCHAR(50) NOT NULL
    );

CREATE TABLE
    users (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        username VARCHAR(12) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        restaurant_id INTEGER,
        CONSTRAINT fk_user_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
    );

CREATE TABLE
    product (
        product_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        image VARCHAR(255),
        description VARCHAR(500) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        is_available BOOLEAN NOT NULL,
        ingredients VARCHAR(255) NOT NULL,
        restaurant_id INTEGER NOT NULL,
        CONSTRAINT fk_product_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    );

CREATE TABLE
    orders (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        order_id VARCHAR(50) NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        total_price NUMERIC(10, 2) NOT NULL,
        status VARCHAR(50) NOT NULL,
        pickup_mode VARCHAR(50) NOT NULL,
        restaurant_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        CONSTRAINT fk_order_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
        CONSTRAINT fk_order_user FOREIGN KEY (user_id) REFERENCES users (id)
    );

CREATE TABLE
    order_items (
        order_items_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        quantity INTEGER NOT NULL,
        id INTEGER NOT NULL,
        product_id VARCHAR(50) NOT NULL,
        CONSTRAINT fk_order_item_order FOREIGN KEY (id) REFERENCES orders (id),
        CONSTRAINT fk_order_item_product FOREIGN KEY (product_id) REFERENCES product (product_id)
    );
