import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_ecommerce_data():
    print("Generating synthetic data for 10 tables...")
    
    # Define parameters
    organisations = ["org_101", "org_202", "org_303"]
    start_date = datetime.now() - timedelta(days=7)
    dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    
    os.makedirs("data_output", exist_ok=True)
    
    for org in organisations:
        for d in dates:
            # 1. Users
            users = pd.DataFrame({
                "user_id": [f"usr_{i}" for i in range(1, 51)],
                "organisation_id": org,
                "signup_date": d,
                "email": [f"user_{i}@{org}.com" for i in range(1, 51)]
            })
            
            # 2. Categories
            categories = pd.DataFrame({
                "category_id": [f"cat_{i}" for i in range(1, 6)],
                "organisation_id": org,
                "category_name": [f"Category_{i}" for i in range(1, 6)]
            })
            
            # 3. Products
            products = pd.DataFrame({
                "product_id": [f"prod_{i}" for i in range(1, 21)],
                "organisation_id": org,
                "category_id": [f"cat_{np.random.randint(1, 6)}" for _ in range(20)],
                "price": np.random.uniform(10.0, 500.0, 20).round(2)
            })
            
            # 4. Coupons
            coupons = pd.DataFrame({
                "coupon_id": [f"coup_{i}" for i in range(1, 4)],
                "organisation_id": org,
                "discount_percent": [10, 20, 30]
            })
            
            # 5. Orders
            orders = pd.DataFrame({
                "order_id": [f"ord_{i}" for i in range(1, 101)],
                "organisation_id": org,
                "user_id": [f"usr_{np.random.randint(1, 51)}" for _ in range(100)],
                "order_date": d,
                "status": "completed"
            })
            
            # 6. Order Items
            order_items = pd.DataFrame({
                "item_id": [f"item_{i}" for i in range(1, 151)],
                "organisation_id": org,
                "order_id": [f"ord_{np.random.randint(1, 101)}" for _ in range(150)],
                "product_id": [f"prod_{np.random.randint(1, 21)}" for _ in range(150)],
                "quantity": np.random.randint(1, 4, 150)
            })
            
            # 7. Payments
            payments = pd.DataFrame({
                "payment_id": [f"pay_{i}" for i in range(1, 101)],
                "organisation_id": org,
                "order_id": [f"ord_{i}" for i in range(1, 101)],
                "amount": np.random.uniform(20.0, 1000.0, 100).round(2)
            })
            
            # 8. Shipments
            shipments = pd.DataFrame({
                "shipment_id": [f"ship_{i}" for i in range(1, 101)],
                "organisation_id": org,
                "order_id": [f"ord_{i}" for i in range(1, 101)],
                "carrier": np.random.choice(["FedEx", "UPS", "DHL"], 100)
            })
            
            # 9. Reviews
            reviews = pd.DataFrame({
                "review_id": [f"rev_{i}" for i in range(1, 31)],
                "organisation_id": org,
                "product_id": [f"prod_{np.random.randint(1, 21)}" for _ in range(30)],
                "rating": np.random.randint(1, 6, 30)
            })
            
            # 10. Refunds
            refunds = pd.DataFrame({
                "refund_id": [f"ref_{i}" for i in range(1, 11)],
                "organisation_id": org,
                "order_id": [f"ord_{np.random.randint(1, 101)}" for _ in range(10)],
                "reason": np.random.choice(["Defective", "Wrong Size", "Not Needed"], 10)
            })
            
            tables = {
                "users": users, "categories": categories, "products": products,
                "coupons": coupons, "orders": orders, "order_items": order_items,
                "payments": payments, "shipments": shipments, "reviews": reviews,
                "refunds": refunds
            }
            
            # Save each table as an ORC file partitioned structure
            for t_name, df in tables.items():
                folder = f"data_output/{t_name}/{org}/{d}"
                os.makedirs(folder, exist_ok=True)
                df.to_orc(f"{folder}/data.orc")
                
    print("Synthetic ORC data generation complete!")

if __name__ == "__main__":
    generate_ecommerce_data()
