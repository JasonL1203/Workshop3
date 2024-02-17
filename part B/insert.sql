-- Insertion de données dans la table Product
INSERT INTO Product (name_product, category, sell_price, inventory_product, purchase_price, description)
VALUES 
    ('Product A', 'Electronics', 49.99, 100, 35.00, 'Description of Product A'),
    ('Product B', 'Clothing', 29.99, 150, 20.00, 'Description of Product B'),
    ('Product C', 'Home and Garden', 99.99, 50, 75.00, 'Description of Product C');

-- Insertion de données dans la table Client
INSERT INTO Client (firstname_client, lastname_client, email_client, address_client)
VALUES
    ('John', 'Doe', 'john.doe@example.com', '123 Main Street'),
    ('Jane', 'Smith', 'jane.smith@example.com', '456 Oak Avenue'),
    ('Bob', 'Johnson', 'bob.johnson@example.com', '789 Pine Road');

-- Insertion de données dans la table Order
INSERT INTO Order_ (products_order, status_order, id_client)
VALUES
    ('[{"id_product": 1, "quantity": 2}, {"id_product": 2, "quantity": 1}]', 'In preparation', 1),
    ('[{"id_product": 2, "quantity": 3}]', 'On hold', 2),
    ('[{"id_product": 3, "quantity": 1}, {"id_product": 3, "quantity": 2}]', 'Delivered', 3);

-- Insertion de données dans la table Cart
INSERT INTO Cart (products_cart, id_client)
VALUES
    ('[{"id_product": 2, "quantity": 2}]', 2),
    ('[{"id_product": 3, "quantity": 1}]', 3),
    ('[{"id_product": 1, "quantity": 3}]', 1);