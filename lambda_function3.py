import pymysql
import logging
import boto3
import subprocess

def lambda_handler(event, context):
    s3_Client = boto3.client('s3')
    try:
        #s3://rameshlodhbucket
        s3_create = s3_Client.create_bucket(Bucket='rameshlodhbucket',CreateBucketConfiguration={'LocationConstraint':'us-west-2'},)
        if s3_create:
            print("Bucket created successfully")
        else:
            print("Bucket not created successfully")

        s3_list = s3_Client.list_buckets()
        if s3_list:
            print('Bucket Exists')
        for bucket in s3_list ['Buckets']:
            print(f'Name of bucket is:{bucket["Name"]}')

        # rds_client = boto3.client('rds')
        # rds_create = rds_client.create_db_instance(
        #         DBInstanceIdentifier='mysqldb',
        #         AllocatedStorage=5,
        #         Engine='MySQL',
        #         DBInstanceClass='db.t2.micro',
        #         MasterUsername='rameshlodh',
        #         MasterUserPassword='rahul123',)
        # if rds_create:
        #     print("Database created successfully")
        # else:
        #     print("Database not created successfully")

        #########how to get host before creating db instance???###########
        host = 'mysqldb1.corlgu8ddbzz.us-west-2.rds.amazonaws.com'
        user = 'rameshlodh'
        password = 'rahul123'

        db = pymysql.Connect(host=host, user=user, password=password)

        cursor = db.cursor()
        sql = 'create database IF NOT EXISTS db_student'
        cursor.execute(sql)
        cursor.execute('show databases')
        cursor.fetchall()
        db.select_db('db_student')

        # str = """create table tbl_student (
        #             std_id int,
        #             std_name varchar(20),
        #             std_lname varchar(20),);
        #             """
        cursor.execute("CREATE TABLE tbl_student (id int, name VARCHAR(255), address VARCHAR(255))")
        cursor.execute('show tables')

        ###########mysqldump is .exe file??? also where backup.sql will store??? #########
        backup =f"mysqldump --set-gtid-purged=OFF -h{host} -u{user} -p{password} db_student > C:\\Users\\rahul\\Desktop\\auto_scripts\\backup.sql"
        backup_run = subprocess.run(backup, shell=True)

        ######### how to give filename/path on cloud??? ##########
        
        file_name = 'C:\\Users\\rahul\\Desktop\\auto_scripts\\backup.sql'
        bucket = 'rameshlodhbucket'
        object_name = "backup.sql" 
        file_name_download = 'C:\\Users\\rahul\\Desktop\\auto_scripts\\download\\backup.sql'

        s3_upload = s3_Client.upload_file(file_name, bucket, object_name)
        if s3_upload:
            print("file uploaded successfully")
        else:
            print("file not uploaded !!")

        s3_download = s3_Client.download_file(bucket, object_name, file_name_download)
        if s3_download:
            print("file downloaded successfully")
        else:
            print("file not downloaded !!")

    except Exception as e:
        logging.error(e)
        return False
    return True    
lambda_handler(None,None)
