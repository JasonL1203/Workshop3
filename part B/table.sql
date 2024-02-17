-- Create the ecommerce database
CREATE DATABASE ecommerce;

-- Connect to the ecommerce database
\c ecommerce;

-- Create the Product table
CREATE TABLE Product (
    id_product SERIAL PRIMARY KEY,
    name_product VARCHAR(50),
    category VARCHAR(50),
    sell_price DOUBLE PRECISION CHECK (sell_price > 0.0),
    inventory_product INT CHECK (inventory_product > 0),
    purchase_price DOUBLE PRECISION CHECK (purchase_price > 0.0),
    description VARCHAR(100)
);

-- Create the Client table
CREATE TABLE Client (
    id_client SERIAL PRIMARY KEY,
    firstname_client VARCHAR(30),
    lastname_client VARCHAR(50),
    email_client VARCHAR(30),
    address_client VARCHAR(100)
);

-- Create the Order table
CREATE TABLE Order_ (
    id_order SERIAL PRIMARY KEY,
    products_order JSONB, -- Assuming a JSONB field to store a list of products and their quantities
    status_order VARCHAR(30) CHECK (status_order IN ('In preparation', 'On hold', 'In the process of delivery', 'Delivered')),
    id_client SERIAL REFERENCES Client(id_client)
);

-- Create the Cart table
CREATE TABLE Cart (
    id_cart SERIAL PRIMARY KEY,
    products_cart JSONB, -- Assuming a JSONB field to store a list of products and their quantities
    id_client SERIAL REFERENCES Client(id_client)
);