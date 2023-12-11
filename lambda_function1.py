import boto3
import os
import logging
import subprocess
import pymysql

# def list_bucket():
#     try:
#         s3 = boto3.client('s3')
#         response =s3.list_buckets()
#         if response:
#             print('Bucket Exists')
#             for bucket in response ['Buckets']:
#                 print(f'Name of bucket is:{bucket["Name"]}')
#     except Exception as e:
#         logging.error(e)
#         return False
#     return True

# list_bucket()

# def upload_file(file_name, bucket, object_name=None):
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     s3_Client = boto3.client('s3')
#     try:
#         response = s3_Client.upload_file(file_name, bucket, object_name)
#     except Exception as e:
#         logging.error(e)
#         return False
#     return True

# result_upload = upload_file("C:\\Users\\rahul\\Desktop\\auto scripts\Dump20231021.sql", "rameshlodhbucket", "Dump20231021.sql")
# if result_upload:
#     print("bucket file uploaded done")
# else:
#     print("bucket file uploaded failed")

def download_file(file_name, bucket, object_name):
    s3_Client = boto3.client('s3')
    try:
        s3_Client.download_file(bucket, object_name, file_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

result_download =  download_file("C:\\Users\\rahul\\Desktop\\auto scripts\Dump20231021.sql", "rameshlodhbucket", "Dump20231021.sql")
if result_download:
    print("bucket file download done")
else:
    print("bucket file download failed")

# def lambda_handler(event, context):
#     rds_client = boto3.client('rds')
#     try:
#         response = rds_client.create_db_instance(
#             DBInstanceIdentifier='mydbbackup',
#             AllocatedStorage=5,
#             Engine='MySQL',
#             DBInstanceClass='db.t2.micro',
#             MasterUsername='rameshlodh',
#             MasterUserPassword='rahul123',
#         )
#         if response:
#             print("Database created")
#         else:
#             print("Database not created")
#     except Exception as e:
#         logging.error(e)
#         return False
#     return True
# lambda_handler(None,None)












