import clickhouse_connect

def create_bronze_layers():
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='password123'
    )
    
    print("Connected to ClickHouse successfully.")
    
    tables = {
        "users": "user_id String, email String, signup_date String",
        "categories": "category_id String, category_name String",
        "products": "product_id String, category_id String, price Float32",
        "coupons": "coupon_id String, discount_percent Int32",
        "orders": "order_id String, user_id String, order_date String, status String",
        "order_items": "item_id String, order_id String, product_id String, quantity Int32",
        "payments": "payment_id String, order_id String, amount Float32",
        "shipments": "shipment_id String, order_id String, carrier String",
        "reviews": "review_id String, product_id String, rating Int32",
        "refunds": "refund_id String, order_id String, reason String"
    }
    
    for table_name, schema in tables.items():
        client.command(f"DROP TABLE IF EXISTS bronze_{table_name}")
        
        # Define table reading files via wildcard, extracting org and date from _path
        query = f"""
        CREATE TABLE bronze_{table_name} AS SELECT
            *,
            CAST(arrayElement(splitBy('/', _path), 3) AS LowCardinality(String)) as organisation_id,
            CAST(arrayElement(splitBy('/', _path), 4) AS Date) as processing_date
        FROM file(
            'http://minio:9000/bronze/{table_name}/*/*/data.orc',
            'ORC',
            '{schema}, organisation_id String, processing_date String'
        )
        """
        
        # Simpler and robust S3 Engine approach using standard wildcards:
        query = f"""
        CREATE TABLE bronze_{table_name} (
            {schema},
            organisation_id LowCardinality(String),
            processing_date Date
        ) ENGINE = S3(
            'http://minio:9000/bronze/{table_name}/org_*/*-*-*/data.orc',
            'admin',
            'password123',
            'ORC'
        )
        """
        
        client.command(query)
        print(f"Re-created Bronze table with pattern matching: bronze_{table_name}")

    print("All 10 Bronze tables updated!")

if __name__ == "__main__":
    create_bronze_layers()
