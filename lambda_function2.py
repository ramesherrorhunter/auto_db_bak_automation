#Import and Install below requirement
import subprocess
import pymysql
import boto3
import logging
import cursor
#import mysqldump

#create function for bucket creation
def lambda_handler(event, context):
    s3_Client = boto3.client('s3')    
    try:
        response = s3_Client.create_bucket(Bucket='rameshlodhbucket',CreateBucketConfiguration={'LocationConstraint':'us-west-2'},)
        if response:
            print("Bucket created successfully:")
        else:
            print("Bucket not created")
    except Exception as e:
        logging.error(e)
        return False
    return True

#create function for bucket listing
def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        response =s3.list_buckets()
        if response:
            print('Bucket Exists')
            for bucket in response ['Buckets']:
                print(f'Name of bucket is:{bucket["Name"]}')
    except Exception as e:
        logging.error(e)
        return False
    return True
lambda_handler(None,None)

#create function for creating rds - mysql instance
def lambda_handler(event, context):
    rds_client = boto3.client('rds')
    try:
        response = rds_client.create_db_instance(
            DBInstanceIdentifier='mysqldb',
            AllocatedStorage=5,
            Engine='MySQL',
            DBInstanceClass='db.t2.micro',
            MasterUsername='rameshlodh',
            MasterUserPassword='rahul123',
        )
        if response:
            print("Database created successfully")
        else:
            print("Database not created successfully")
    except Exception as e:
        logging.error(e)
        return False
    return True

#defind below credentials to connect db instance
host = ''
user = 'rameshlodh'
password = 'rahul123'

db = pymysql.connect(
    host = host,
    user = user,
    password = password
)

cursor = db.cursor()
sql = 'create database IF NOT EXISTS db_student'
cursor.execute(sql)
cursor.execute('show databases')
cursor.fetchall()
db.select_db('db_student')

str = """create table tbl_student (
    std_id int,
    std_name varchar(20),
    std_lname varchar(20),
);
"""

cursor.execute(str)
cursor.execute('show tables')

backup = f"mysqldump --set-gtid-purged=OFF -h{host} -p{password} db_student > backup.sql"
backup_run = subprocess.run(backup, shell=True)

def lambda_handler(event, context):
    s3_upload = boto3.client('s3')
    try:
        file_name = 'backup.sql'
        bucket = 'rameshlodhbucket'
        object_name = file_name
        response = s3_upload.upload_file(file_name, bucket, object_name)
        if response:
            print("file uploaded successfully")
        else:
            print("file not uploaded successfully")
    except Exception as e:
        logging.error(e)
        return False
    return True















































