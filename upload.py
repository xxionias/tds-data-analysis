import boto3
from datetime import datetime

s3 = boto3.client('s3')

# print(s3.list_buckets()['Buckets'])

today_date = datetime.now().strftime("%m_%d_%Y")
bucket_name = datetime.now().strftime("%m-%d-%Y")
s3.create_bucket(Bucket=bucket_name)

article_filename = "article_" + today_date + ".json"
s3.upload_file(
    Filename="./raw_data/articles/" + article_filename,
    Bucket=bucket_name,
    Key=article_filename
)

article_command_output = "article_command_output_" + today_date + ".txt"
s3.upload_file(
    Filename="./raw_data/articles/" + article_command_output,
    Bucket=bucket_name,
    Key=article_command_output
)

profile_filename = "users_" + datetime.now().strftime("%m_%d_%Y") + ".json"
s3.upload_file(
    Filename="./raw_data/users/" + profile_filename,
    Bucket=bucket_name,
    Key=profile_filename
)

profile_command_output = "users_command_output_" + today_date + ".txt"
s3.upload_file(
    Filename="./raw_data/users/" + profile_command_output,
    Bucket=bucket_name,
    Key=profile_command_output
)
