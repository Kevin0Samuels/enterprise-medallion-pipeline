import clickhouse_connect

def build_gold_layer():
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='password123'
    )
    
    print("Connected to ClickHouse for Gold Layer setup...")
    
    # Drop table if it exists
    client.command("DROP TABLE IF EXISTS gold_org_performance")
    
    # Create Gold Aggregated Table using SummingMergeTree or ReplacingMergeTree, 
    # strictly grouped by organisation_id to enforce multi-tenancy boundaries.
    query = """
    CREATE TABLE gold_org_performance (
        organisation_id LowCardinality(String),
        total_orders UInt32,
        total_revenue Float64,
        avg_payment_amount Float64
    ) ENGINE = ReplacingMergeTree()
    PRIMARY KEY (organisation_id)
    ORDER BY (organisation_id)
    """
    client.command(query)
    
    # Populate Gold table by aggregating from Silver tables
    populate_query = """
    INSERT INTO gold_org_performance
    SELECT 
        o.organisation_id,
        count(DISTINCT o.order_id) as total_orders,
        sum(p.amount) as total_revenue,
        avg(p.amount) as avg_payment_amount
    FROM silver_orders o
    LEFT JOIN silver_payments p ON o.order_id = p.order_id AND o.organisation_id = p.organisation_id
    GROUP BY o.organisation_id
    """
    client.command(populate_query)
    
    print("Gold aggregated table 'gold_org_performance' successfully created and populated!")

if __name__ == "__main__":
    build_gold_layer()
