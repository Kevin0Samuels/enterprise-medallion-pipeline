import os
from minio import Minio

def upload_data():
    client = Minio(
        "localhost:9002",
        access_key="admin",
        secret_key="password123",
        secure=False
    )
    
    bucket_name = "bronze"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created bucket: {bucket_name}")
        
    local_dir = "data_output"
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            # Compute relative path to maintain folder structure
            rel_path = os.path.relpath(local_path, local_dir)
            object_name = rel_path.replace(os.sep, "/")
            
            client.fput_object(bucket_name, object_name, local_path)
            print(f"Uploaded: {object_name}")
            
    print("All data successfully uploaded to MinIO!")

if __name__ == "__main__":
    upload_data()
