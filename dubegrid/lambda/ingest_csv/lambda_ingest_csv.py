import boto3
import csv
import io
import urllib.parse   # ⬅ NEW: to decode the S3 key

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    # 🔍 Debug incoming S3 event values
    print(f"DEBUG — Incoming bucket: {bucket}")
    print(f"DEBUG — Incoming key:    {key}")

    # ✅ Decode URL‑encoded characters (e.g. %3D → =)
    key = urllib.parse.unquote_plus(key)

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))

    # 🔗 Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DubeGridAssetData')

    for i, row in enumerate(reader, start=1):
        if i <= 5:  # show only first 5 rows for sanity check
            print(row)

        # 📝 Insert each row into DynamoDB
        table.put_item(Item={
            'asset_id': row['asset_id'],
            'timestamp': row['timestamp'],
            'value': row['value']  # adjust based on your actual CSV columns
        })

    print(f"✅ Processed {i} rows and inserted into DynamoDB")
