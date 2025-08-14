import os
import subprocess

# Local path on your Mac that maps to /data in your container
LOCAL_DIR = "./data"
DBFS_DIR = "dbfs:/mnt/raw_data/"

# Loop through JSONL files and upload to DBFS
for file in os.listdir(LOCAL_DIR):
    if file.endswith(".jsonl"):
        local_path = os.path.join(LOCAL_DIR, file)
        dbfs_path = DBFS_DIR + file
        print(f"Uploading {local_path} → {dbfs_path}")
        subprocess.run(["databricks", "fs", "cp", local_path, dbfs_path, "--overwrite"])
