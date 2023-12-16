import boto3
import snowflake.connector

# Set up your Snowflake connection
conn = snowflake.connector.connect(
    user='email',
    authenticator = 'externalbrowser',
    account='id.eu-west-2',
    region = 'eu-west-2',
    # authenticator = 'externalbrowser',  # Replace with your Snowflake account URL
    warehouse='warehouse name',  # Replace with your Snowflake warehouse name
    database='database name',
    schema='schema name'
)

# Create a Snowflake cursor
cursor = conn.cursor()

# AWS credentials
s3_resource = boto3.resource(service_name='s3',
                             region_name='eu-west-2',
                             aws_access_key_id='YOUR_ACCESS_KEY',
                             aws_secret_access_key='YOUR_SECRET_KEY')

bucket_name = 'bucketname'

# Iterate through all objects in the S3 bucket
for obj in s3_resource.Bucket(bucket_name).objects.all():
    # Get the URL for each object
    object_url = f"https://{bucket_name}.s3.amazonaws.com/{obj.key}"
    
    # Insert the URL into the Snowflake table
    cursor.execute("INSERT INTO HERO_INFO_URL (URL) VALUES (%s)", (object_url,))

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
