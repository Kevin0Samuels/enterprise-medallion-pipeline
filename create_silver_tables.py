import clickhouse_connect

def build_silver_layer():
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='password123'
    )
    
    print("Creating Silver layer tables if they don't exist...")

    # --- Create silver tables ---
    client.command("""
        CREATE TABLE IF NOT EXISTS silver_users (
            user_id String,
            email String,
            signup_date DateTime,
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = MergeTree()
        ORDER BY (organisation_id, user_id)
    """)

    client.command("""
        CREATE TABLE IF NOT EXISTS silver_products (
            product_id String,
            category_id String,
            price Float32,
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = MergeTree()
        ORDER BY (organisation_id, product_id)
    """)

    client.command("""
        CREATE TABLE IF NOT EXISTS silver_orders (
            order_id String,
            user_id String,
            order_date DateTime,
            status String,
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = MergeTree()
        ORDER BY (organisation_id, order_id)
    """)

    client.command("""
        CREATE TABLE IF NOT EXISTS silver_order_items (
            item_id String,
            order_id String,
            product_id String,
            quantity Int32,
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = MergeTree()
        ORDER BY (organisation_id, item_id)
    """)

    client.command("""
        CREATE TABLE IF NOT EXISTS silver_payments (
            payment_id String,
            order_id String,
            amount Float32,
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = MergeTree()
        ORDER BY (organisation_id, payment_id)
    """)

    print("Populating Silver layer tables correctly...")
    
    # 1. Users
    client.command("TRUNCATE TABLE IF EXISTS silver_users")
    client.command("""
        INSERT INTO silver_users
        SELECT user_id, email, parseDateTimeBestEffort(signup_date) as signup_date, organisation_id, processing_date
        FROM bronze_users
    """)
    
    # 2. Products
    client.command("TRUNCATE TABLE IF EXISTS silver_products")
    client.command("""
        INSERT INTO silver_products
        SELECT product_id, category_id, price, organisation_id, processing_date
        FROM bronze_products
    """)
    
    # 3. Orders
    client.command("TRUNCATE TABLE IF EXISTS silver_orders")
    client.command("""
        INSERT INTO silver_orders
        SELECT order_id, user_id, parseDateTimeBestEffort(order_date) as order_date, status, organisation_id, processing_date
        FROM bronze_orders
    """)
    
    # 4. Order Items
    client.command("TRUNCATE TABLE IF EXISTS silver_order_items")
    client.command("""
        INSERT INTO silver_order_items
        SELECT item_id, order_id, product_id, quantity, organisation_id, processing_date
        FROM bronze_order_items
    """)
    
    # 5. Payments
    client.command("TRUNCATE TABLE IF EXISTS silver_payments")
    client.command("""
        INSERT INTO silver_payments
        SELECT payment_id, order_id, amount, organisation_id, processing_date
        FROM bronze_payments
    """)
    
    print("Silver tables successfully re-populated with data from Bronze!")

if __name__ == "__main__":
    build_silver_layer()
