import datetime
import gzip
import json
import os
import subprocess

import boto3
from pymongo import MongoClient


# Custom JSON encoder class to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return super().default(obj)


# MongoDB connection settings
mongo_uri = os.environ['MONGO_URI']

# Amazon S3 settings
s3_bucket = os.environ['S3_BUCKET']
s3_path = os.environ['S3_PATH']
s3_endpoint = os.environ['S3_ENDPOINT']
s3_region = os.environ['S3_REGION']
s3_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
s3_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Get current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create a backup directory
backup_dir = f"{current_date}_backup"
os.makedirs(backup_dir)

# Get list of databases
databases = client.list_database_names()

# Dump each database to a JSON file and gzip it
for database in databases:
    # Skip system databases
    if database in ['admin', 'local', 'config']:
        continue

    # Create a directory for the database backup
    database_dir = os.path.join(backup_dir, database)
    os.makedirs(database_dir)
    
    # Dump the database to a JSON file
    dump_file = os.path.join(database_dir, f"{database}.json")
    cmd = f"mongodump --authenticationDatabase=admin --uri='{mongo_uri}/?ssl=false&authSource=admin' --db '{database}' --out '{database_dir}'"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode != 0:
        raise Exception(f"Error dumping database {database}. {process.stderr} {process.stout}")
    

    # # Gzip the JSON file
    # gzipped_file = f"{dump_file}.gz"
    # with open(dump_file, 'rb') as f_in:
    #     with gzip.open(gzipped_file, 'wb') as f_out:
    #         f_out.writelines(f_in)

    # # Remove the uncompressed JSON file
    # os.remove(dump_file)


# Create a unique archive name
archive_name = f"{current_date}_backup.tar.gz"

# Create a tarball of the backup directory
os.system(f"tar -czvf {archive_name} {backup_dir}")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=s3_region,
    # endpoint_url=s3_endpoint,
    aws_access_key_id=s3_access_key_id,
    aws_secret_access_key=s3_secret_access_key
)

# Upload the archive to S3
s3_client.upload_file(archive_name, s3_bucket, os.path.join(s3_path, archive_name))

# Remove the backup directory and archive
# os.remove(archive_name)
os.system(f"rm -r {backup_dir}")

# Print success message
print(f"Backup {archive_name} completed and uploaded to S3.")