CREATE TABLE orders(
	order_id VARCHAR(20) PRIMARY KEY,
	customer_name VARCHAR(10) NOT NULL,
	customer_id	VARCHAR(36) NOT NULL,
	purchase_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_item(
	id SERIAL PRIMARY KEY,
	product_name VARCHAR(10) NOT NULL,
	product_id	VARCHAR(36) NOT NULL,
	amount INT NOT NULL,
	price INT NOT NULL,
	order_id VARCHAR(20),
    CONSTRAINT fk_orders
      FOREIGN KEY(order_id) 
	  	REFERENCES orders(order_id)
);

