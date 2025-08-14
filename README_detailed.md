# 📄 DubeGrid – Cloud Data Pipeline *(LV Load Monitor Edition)*

## 📌 Project Goal
Build a **modular, cloud‑native pipeline** that ingests UK low‑voltage substation load data, processes it automatically with **AWS Lambda**, and produces **asset‑level performance summaries** for strategic decision‑making in the energy sector.

This project showcases:
- **Event‑driven ingestion** from AWS S3.
- **Serverless processing** and transformation in AWS Lambda.
- **Structured, queryable storage** in DynamoDB and Athena.
- **Scalable, cost‑efficient architecture** for real‑world asset intelligence workflows.

---

## 🧠 Why It Matters
Modern grid operations demand **timely insights** into load patterns, anomalies, and usage trends.  
**DubeGrid** is designed to:
- Reduce manual data handling.
- Deliver near real‑time asset metrics.
- Form the backbone for **dashboards, alerts, and analytics** in the utilities domain.

---

## 🧰 Tools & Services

| Layer        | Tool / Service                         | Purpose |
|--------------|----------------------------------------|---------|
| **Cloud Infra** | AWS S3                                | Store raw and processed data |
|              | AWS Lambda                            | Serverless ingestion and transformation |
|              | AWS DynamoDB                           | Queryable asset‑level storage |
|              | AWS Athena                             | Batch analytics via SQL |
|              | AWS IAM                                | Secure access control |
|              | AWS CloudWatch                         | Logs, monitoring, debugging |
| **IaC**      | Terraform                              | Provision AWS resources |
| **Code**     | Python                                 | Transformation and enrichment logic |
| **Local Dev**| VS Code                                | Editing and testing |
| **VCS**      | GitHub                                 | Version control & portfolio hosting |
| **Docs**     | Markdown / Notion                      | Documentation & tracking |
| **Data Source** | National Grid DSO LV Load Monitor    | Live substation load CSVs |

---

## 📂 Current Folder Structure
```text
dubegrid/
├── data/
│   ├── lv_data_2025_04.csv
│   ├── lv_data_2025_08.csv
│   └── README.md
├── lambda/
│   └── ingest_csv/
│       ├── lambda_ingest_csv.py
│       ├── trust-policy.json
│       ├── function.zip
│       ├── event.json
│       ├── lambda_config.json
│       ├── output.json
│       ├── s3-notify.json
│       └── sample.csv
├── diagrams/
│   └── dubegrid_architecture.png
└── README.md
```

```
DubeGrid Architecture

                   ┌──────────────┐
                   │  Source CSVs │
                   └──────┬───────┘
                          │
                          v
                 ┌─────────────────┐
                 │   Amazon S3      │
                 │ raw/prod/lv/...  │
                 └──────┬───────────┘
            S3 ObjectCreated (Trigger)
                          │
                          v
              ┌─────────────────────────┐
              │ AWS Lambda               │
              │ Ingest / Parse / Transform │
              └──────┬───────────────────┘
                     │ PutItem (processed rows)
                     v
            ┌─────────────────────────┐
            │ Amazon DynamoDB          │
            │ PK: asset_id  SK: timestamp │
            └─────────────────────────┘
                     
     Logs & Metrics       Query & Results via S3
           │                       ▲
           v                       │
┌────────────────┐         ┌──────────────────────┐
│ Amazon CloudWatch │      │ Amazon Athena         │
│ Logs & Metrics    │      │ SQL over S3 (external │
└────────────────┘         │ table)                │
                           └──────────────────────┘

[IAM: Execution Role & Permissions apply to S3, Lambda, and DynamoDB]


```

---

## 🗂 Dataset – LV Load Monitor Data

**Description:**  
Substation‑level load patterns across NGED licence areas.

**Source:**  
National Grid Connected Data Portal – LV Load Monitor dataset.

**Schema Overview:**
| CSV Column         | Athena Column Name  | Type   | Example |
|--------------------|---------------------|--------|---------|
| Substation Number  | `substation_number` | STRING | LV123   |
| Substation Name    | `substation_name`   | STRING | Main St |
| Timestamp          | `timestamp`         | STRING | 2025‑08‑14T15:00:00Z |
| Attribute Type     | `attribute_type`    | STRING | feeder  |
| Feeder ID          | `feeder_id`         | STRING | 05      |
| Description        | `description`       | STRING | L3 Reactive Power |
| Units              | `units`             | STRING | kVAR    |
| Value              | `value`             | DOUBLE | 42.7    |

---

## 🧭 High‑Level Pipeline Flow

**Technical Lens:**  
1. File lands in S3 → Event fires → Lambda reads & processes file → Logs results → Data stored in DynamoDB / queried in Athena.

**Analogy Lens:**  
Think of **S3** as a smart mailbox. Every time a letter *(CSV)* arrives, a robot *(Lambda)* opens it instantly, reads it, and files it neatly *(DynamoDB)*. No one checks the mailbox manually — and if 100 letters arrive, 100 robots show up at once.

---

## 🖼 Architecture Diagram
*(Located at: `diagrams/dubegrid_architecture.png` — embed in your README for visual impact)*

**Flow:**
1. **S3 (raw/)** – Stores LV load monitor CSVs with partitioned structure:  
   `raw/prod/lv/y=YYYY/m=MM/file.csv`
2. **S3 Event Notification** – Triggers Lambda on `.csv` creation.
3. **Lambda Function** –  
   - Reads file from S3.  
   - Transforms/validates data.  
   - Writes rows to DynamoDB *(and/or processed S3)*.
4. **DynamoDB** – Queryable by asset ID & timestamp.
5. **Athena** – SQL over raw S3 for batch queries & analytics.
6. **CloudWatch** – End‑to‑end logging & monitoring.
7. *(Optional)* **Kinesis / QuickSight / Streamlit** – Real‑time or visual dashboards.

---

## 📍 Phase 1 Deliverables
- [x] **S3 bucket** (`dubegrid-data-ingest`) – partitioned, production‑style layout.
- [x] **Lambda ingestion function** with CSV parsing.
- [x] **IAM role & permissions** for S3 + logging.
- [x] **Event trigger** from S3 → Lambda.
- [x] Tested ingestion & DynamoDB writes with LV CSV samples.
- [x] README *(this doc)* + architecture diagram.


---

# ⚙️ Environment Setup & Lambda Bootstrapping

## 1️⃣ Prerequisites
Before building the ingestion pipeline, make sure you have:

- **AWS Account** with permissions for S3, Lambda, IAM, DynamoDB, and CloudWatch.
- **AWS CLI** installed and configured with an access key/secret key.
- **Python 3.12** installed locally.
- **VS Code** (or your preferred editor).
- Basic understanding of AWS Regions and CLI commands.

---

## 2️⃣ Set AWS CLI Default Region
We’ll use **`us-east-1`** for this project, but you can change it if needed.

```bash
aws configure set region us-east-1
```

---

## 3️⃣ Create S3 Ingest Bucket
This is where the LV Load Monitor CSVs will be dropped.

```bash
aws s3 mb s3://dubegrid-data-ingest --region us-east-1
```

---

## 4️⃣ Local Project Folder Structure

From your **home** directory (not Desktop):

```bash
mkdir -p ~/CloudProjects/dubegrid/lambda/ingest_csv
mkdir -p ~/CloudProjects/dubegrid/data
mkdir -p ~/CloudProjects/dubegrid/diagrams
```

Confirm layout:

```bash
tree ~/CloudProjects/dubegrid
```

You should see:

```text
dubegrid/
├── data/
├── lambda/
│   └── ingest_csv/
└── diagrams/
```

---

## 5️⃣ Create Lambda Handler File

Navigate to the Lambda source folder:

```bash
cd ~/CloudProjects/dubegrid/lambda/ingest_csv
touch lambda_ingest_csv.py
```

Paste this starter handler:

```python
import boto3
import csv
import io

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))

    for row in reader:
        print(row)

    return {'statusCode': 200, 'body': 'CSV processed'}
```

---

## 6️⃣ Create Trust Policy for IAM Role

Still inside `ingest_csv/`:

```bash
touch trust-policy.json
```

Paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
```

---

## 7️⃣ Create IAM Role for Lambda

From inside the **`ingest_csv/`** folder:

```bash
aws iam create-role \
  --role-name DubeGridLambdaRole \
  --assume-role-policy-document file://trust-policy.json \
  --region us-east-1
```

Copy the returned **Role ARN** — we’ll need it when creating the Lambda.

---

## 8️⃣ Attach Required Policies

### S3 Full Access
```bash
aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess \
  --region us-east-1
```

### CloudWatch Logs (Basic Execution Role)
```bash
aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  --region us-east-1
```

---

## 9️⃣ Package the Lambda

```bash
zip function.zip lambda_ingest_csv.py
```

---

## 🔟 Create the Lambda Function

Replace `<Role-ARN>` with your actual IAM Role ARN:

```bash
aws lambda create-function \
  --function-name DubeGridIngestCSV \
  --runtime python3.12 \
  --role <Role-ARN> \
  --handler lambda_ingest_csv.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 512 \
  --region us-east-1
```

---

## ✅ Result
You now have:
- A **dedicated S3 ingest bucket**.
- A **local, modular project folder structure**.
- **Lambda ingestion code** in place.
- **IAM role & permissions** set up for S3 and CloudWatch.
- **Deployed Lambda function** ready to be invoked.

---

wire S3 → Lambda triggers, run manual invokes with `event.json`, and tail CloudWatch logs for troubleshooting.

---

# 🚦 Testing & Wiring the S3 → Lambda Trigger

## 1️⃣ Create a Test Event File
We’ll simulate what S3 would send when a `.csv` is uploaded.

From inside `~/CloudProjects/dubegrid/lambda/ingest_csv`:

```bash
touch event.json
```

Paste:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "dubegrid-data-ingest" },
        "object": { "key": "sample.csv" }
      }
    }
  ]
}
```

---

## 2️⃣ Invoke the Lambda Manually
First, zip (or re‑zip) the code if updated:

```bash
zip function.zip lambda_ingest_csv.py
```

Invoke with **fileb://** (important for JSON payloads):

```bash
aws lambda invoke \
  --function-name DubeGridIngestCSV \
  --payload fileb://event.json \
  --region us-east-1 \
  output.json
```

Check:

```bash
cat output.json
```

---

## 3️⃣ Enable CloudWatch Logging
If you see a `ResourceNotFoundException` when tailing logs, attach the basic execution role:

```bash
aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  --region us-east-1
```

---

## 4️⃣ Tail Logs in Real Time
```bash
aws logs tail /aws/lambda/DubeGridIngestCSV --region us-east-1 --follow
```

You should see:
- `START` / `END` / `REPORT` markers.
- `print()` output from your handler.
- Any error stack traces.

---

## 5️⃣ Fixing NoSuchKey in Tests
If you see an error that `sample.csv` isn’t found:
- **Option A:** Upload it:

```bash
echo "asset_id,timestamp,value
LV123,2025-08-14T15:00:00Z,42.7" > sample.csv

aws s3 cp sample.csv s3://dubegrid-data-ingest/sample.csv --region us-east-1
```

- **Option B:** Change `event.json` to reference an existing object in S3:

```bash
aws s3 ls s3://dubegrid-data-ingest --region us-east-1
```

---

## 6️⃣ Wire S3 Event Notifications → Lambda

### Add Invoke Permission
```bash
aws lambda add-permission \
  --function-name DubeGridIngestCSV \
  --statement-id s3invoke-dubegrid \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::dubegrid-data-ingest \
  --region us-east-1
```

### Create Notification Config
Inside `lambda/ingest_csv/`:

```bash
cat > s3-notify.json << 'JSON'
{
  "LambdaFunctionConfigurations": [
    {
      "Id": "InvokeDubeGridIngestOnCSV",
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:<account-id>:function:DubeGridIngestCSV",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            { "Name": "suffix", "Value": ".csv" }
          ]
        }
      }
    }
  ]
}
JSON
```

Apply:

```bash
aws s3api put-bucket-notification-configuration \
  --bucket dubegrid-data-ingest \
  --notification-configuration file://s3-notify.json \
  --region us-east-1
```

---

## 7️⃣ End‑to‑End Test

Upload a file to trigger the pipeline automatically:

```bash
aws s3 cp sample.csv s3://dubegrid-data-ingest/test/sample.csv --region us-east-1
```

Tail the logs:

```bash
aws logs tail /aws/lambda/DubeGridIngestCSV --region us-east-1 --follow
```

You should see the parsed CSV rows and the total processed count.

---

## ✅ Outcome
- **Manual invokes** confirm Lambda logic in isolation.
- **CloudWatch logs** provide real‑time visibility.
- **S3 event notifications** make the ingestion pipeline reactive — no manual runs.
- The system now ingests **any CSV dropped into S3** that matches the trigger rules.

---

**DynamoDB integration** for asset‑level queries, manage S3 prefix structures for organised ingestion, and verify multi‑file processing.  


---

# 🗄 DynamoDB Integration & Structured Ingestion

## 1️⃣ Create the DynamoDB Table
We’ll store asset readings with a **composite key**:  
- **Partition key** = `asset_id` → groups readings per asset.  
- **Sort key** = `timestamp` → enables time‑range queries.

```bash
aws dynamodb create-table \
  --table-name DubeGridAssetData \
  --attribute-definitions \
    AttributeName=asset_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=S \
  --key-schema \
    AttributeName=asset_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

---

## 2️⃣ Update Lambda to Insert into DynamoDB
Open `lambda_ingest_csv.py` and extend it:

```python
import boto3
import csv
import io
import urllib.parse
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DubeGridAssetData')

def lambda_handler(event, context):
    print("Event:", event)
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key    = urllib.parse.unquote_plus(record['s3']['object']['key'])

        # Fetch CSV from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content  = response['Body'].read().decode('utf-8')
        reader   = csv.DictReader(io.StringIO(content))

        for i, row in enumerate(reader, start=1):
            if i <= 5:  # sanity check output
                print(row)

            # Write each row to DynamoDB
            table.put_item(Item={
                'asset_id': row['asset_id'],
                'timestamp': row['timestamp'],
                'value': row['value']  # adjust to your CSV schema
            })

        print(f"✅ Processed {i} rows and inserted into DynamoDB")
    except ClientError as e:
        print("AWS ClientError:", str(e))
    except Exception as e:
        print("Unhandled error:", str(e))
```

---

## 3️⃣ Grant DynamoDB Write Permissions to Lambda
```bash
aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess \
  --region us-east-1
```
*(You can scope this down later to just `PutItem` on the specific table.)*

---

## 4️⃣ Redeploy the Updated Code
```bash
zip function.zip lambda_ingest_csv.py
aws lambda update-function-code \
  --function-name DubeGridIngestCSV \
  --zip-file fileb://function.zip \
  --region us-east-1
```

---

## 5️⃣ S3 Prefix Convention for Production
Organise raw data by dataset and date for easy partitioning in Athena later.

Example production upload path:

```text
raw/prod/lv/y=2025/m=05/lv_data_0525.csv
```

Upload May & August datasets:

```bash
aws s3 cp ~/CloudProjects/dubegrid/data/lv_data_0525.csv \
  s3://dubegrid-data-ingest/raw/prod/lv/y=2025/m=05/ \
  --region us-east-1

aws s3 cp ~/CloudProjects/dubegrid/data/lv_data_0825.csv \
  s3://dubegrid-data-ingest/raw/prod/lv/y=2025/m=08/ \
  --region us-east-1
```

---

## 6️⃣ Verify Multi‑File Ingestion
After uploading both files, check DynamoDB:

```bash
aws dynamodb scan \
  --table-name DubeGridAssetData \
  --region us-east-1 \
  --output table
```

Example **query by asset and date**:

```bash
aws dynamodb query \
  --table-name DubeGridAssetData \
  --key-condition-expression "asset_id = :aid AND begins_with(#ts, :ts)" \
  --expression-attribute-names '{"#ts": "timestamp"}' \
  --expression-attribute-values '{":aid":{"S":"LV123"}, ":ts":{"S":"2025-08-14"}}' \
  --region us-east-1 \
  --output table
```

---

## ✅ Outcome
- **Event‑driven S3 ingestion** writes directly to DynamoDB.
- Data is **immediately queryable** by asset and time.
- Prefix‑based S3 organisation supports efficient downstream analytics.

---

# 📊 Athena Integration & Batch Analytics

## 1️⃣ Create Athena Database (One‑Time)

In the Athena console **Query Editor**, run:

```sql
CREATE DATABASE dubegrid_db;
```

Select `dubegrid_db` from the database dropdown before creating tables.

---

## 2️⃣ Match Table Schema to CSV Headers
Our LV Load Monitor CSV schema:

| CSV Column         | Athena Column Name  | Type   |
|--------------------|---------------------|--------|
| Substation Number  | substation_number   | STRING |
| Substation Name    | substation_name     | STRING |
| Timestamp          | timestamp           | STRING |
| Attribute Type     | attribute_type      | STRING |
| Feeder ID          | feeder_id           | STRING |
| Description        | description         | STRING |
| Units              | units               | STRING |
| Value              | value               | DOUBLE |

---

## 3️⃣ Create External Table Over S3
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS dubegrid_db.lv_data (
  substation_number STRING,
  substation_name   STRING,
  timestamp         STRING,
  attribute_type    STRING,
  feeder_id         STRING,
  description       STRING,
  units             STRING,
  value             DOUBLE
)
PARTITIONED BY (
  y STRING,
  m STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\""
)
LOCATION 's3://dubegrid-data-ingest/raw/prod/lv/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

---

## 4️⃣ Load Partitions
Registers `y=YYYY/m=MM` folders as table partitions.

```sql
MSCK REPAIR TABLE lv_data;
```

---

## 5️⃣ Run an Insight Query
Example: **Average load per substation for May 2025**

```sql
SELECT substation_name, AVG(value) AS avg_load
FROM lv_data
WHERE y = '2025' AND m = '05'
GROUP BY substation_name
ORDER BY avg_load DESC;
```

---

## 6️⃣ Query Result Location
Athena requires a query results S3 bucket:

1. Click ⚙️ **Settings** in Athena.
2. Set “Query result location” to something like:
   ```
   s3://dubegrid-data-ingest/athena-results/
   ```

---

## 7️⃣ Alternative Insight Examples
- **Peak load per asset:**
```sql
SELECT asset_id, MAX(value) AS peak_load
FROM lv_data
GROUP BY asset_id;
```

- **Daily trend for one substation:**
```sql
SELECT date(parse_datetime(timestamp, 'yyyy-MM-dd''T''HH:mm:ss')) AS day,
       AVG(value) AS avg_daily_load
FROM lv_data
WHERE substation_name = 'Main St'
GROUP BY day
ORDER BY day;
```

---

## ✅ Outcome
- Raw S3 data is now **directly queryable via SQL**.
- Partition design supports efficient month/year queries.
- You can export query results as CSV for **Excel, Power BI, QuickSight, or Streamlit** dashboards.

---

# 🔄 End‑to‑End Flow & Strategic Roadmap

## 🖥 Technical Lens — How It All Runs
1. **File lands in S3**  
   - A `.csv` is uploaded into `dubegrid-data-ingest/raw/prod/lv/y=YYYY/m=MM/…`.
   - S3 instantly raises an **ObjectCreated** event.
2. **Lambda auto‑triggers**  
   - Reads bucket/key from event.
   - Fetches the file, parses CSV rows.
3. **Processing & Storage**  
   - Writes parsed rows into **DubeGridAssetData** in DynamoDB for fast asset/time queries.
   - Leaves raw file in S3 for batch analytics in Athena.
4. **Monitoring**  
   - Every run logged in **CloudWatch**: prints, errors, runtime, memory.
5. **Analytics Layer** *(on demand)*  
   - **DynamoDB** → Quick lookups and operational queries.  
   - **Athena** → Partition‑aware SQL over months/years of history.
6. **Visualisation / Reporting** *(optional)*  
   - Streamlit, QuickSight, or Excel for charts, trends, and stakeholder‑ready visuals.

---

## 📦 Analogy Lens — The Smart Mailroom
Think of **S3** as a **smart mailbox** in the utility company:

- A letter *(CSV)* arrives → your sorting robot *(Lambda)* opens it instantly.
- The robot **reads** the details (parse CSV), **logs** what it saw (CloudWatch),  
  and **files the info** into an indexed cabinet (DynamoDB) so you can look up any record instantly.
- If needed, it also **sends a copy** to the analytics department (Athena) for monthly or yearly studies.
- If 100 letters show up at once, 100 robots work in parallel — no queue, no coffee breaks.

---

## 🌍 Real‑World Impact
- **Energy asset intelligence**: Faster detection of peaks, anomalies, and usage trends.
- **Operational efficiency**: No manual file handling; ingestion is reactive and autonomous.
- **Scalability**: Handles a handful or thousands of files without redesign.
- **Portfolio strength**: Demonstrates end‑to‑end AWS skills — event‑driven design, IAM security, serverless compute, structured storage, and cloud analytics.

---

## 🛣 Roadmap — Where DubeGrid Goes Next
- **Data Transformation**  
  Calculate peak/average/variance in Lambda before storage.
- **Curated Zone in S3**  
  Write processed JSON/Parquet to `processed/` for BI tools.
- **Athena Optimisation**  
  Partition pruning, columnar formats (Parquet) for cost/performance.
- **Visual Dashboards**  
  - *QuickSight* → publish interactive asset load trends.  
  - *Streamlit* → portfolio‑ready live demo.
- **Data Quality Checks**  
  Validate schema, detect missing/invalid readings before insert.
- **Event Fan‑Out**  
  Push processed data to Kinesis/SNS for real‑time alerts.

---

## ✅ Current Build Status

| Component         | Status | Notes |
|-------------------|--------|-------|
| S3 bucket layout  | ✅ Done | Partitioned by dataset & date |
| Lambda function   | ✅ Done | Decodes event, parses CSV, inserts into DynamoDB |
| DynamoDB table    | ✅ Done | Queryable by asset/timestamp |
| Multi‑file ingest | ✅ Done | 05 25 & 08 25 datasets confirmed |
| Athena table      | ✅ Done | Schema matches LV Load Monitor CSV |
| CLI queries       | ✅ Done | Both point lookups & aggregations tested |
| CloudWatch logs   | ✅ Done | Real‑time tailing for debug/monitor |

---

💡 **Tip for Portfolio Presentation**:  
Embed your architecture diagram, add a short animated GIF of a CSV upload triggering the Lambda, and include 1–2 screenshot snippets of DynamoDB and Athena results. This turns the README into a **living case study** rather than just a build log.

---

