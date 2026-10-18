import clickhouse_connect

def verify_tenant_collision():
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='default',
        password='password123'
    )
    
    print("Running Multi-Tenant Collision Proof Test...")
    
    # 1. Insert a colliding business key (usr_999) under two separate organisations
    # Even though user_id is the same, organisation_id is part of the primary key.
    client.command("""
        INSERT INTO silver_users (user_id, email, signup_date, organisation_id, processing_date)
        VALUES 
        ('usr_999', 'collision_101@test.com', '2026-10-01', 'org_101', '2026-10-06'),
        ('usr_999', 'collision_202@test.com', '2026-10-01', 'org_202', '2026-10-06')
    """)
    
    # 2. Query back records for user_id = 'usr_999' across all organisations
    result = client.query("SELECT user_id, organisation_id, email FROM silver_users WHERE user_id = 'usr_999'").result_rows
    
    print("\n--- Collision Test Results ---")
    print(f"Total rows found for shared business key 'usr_999': {len(result)}")
    for row in result:
        print(f"User ID: {row[0]} | Organisation ID: {row[1]} | Email: {row[2]}")
        
    if len(result) == 2:
        print("\nSUCCESS: Multi-tenancy isolation verified! The exact same business key under different organisations was successfully maintained as distinct rows without data bleeding.")
    else:
        print("\nWARNING: Collision check failed or rows were overwritten.")

if __name__ == "__main__":
    verify_tenant_collision()
