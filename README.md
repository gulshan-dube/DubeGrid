# 🚀 DubeGrid  

Event‑Driven Cloud Data Pipeline on AWS (LV Load Monitor Edition)

**DubeGrid** is a hands‑on cloud engineering project that builds a **serverless, event‑driven ingestion pipeline** for UK substation load data. It demonstrates **AWS event triggers, serverless compute, and structured storage** — from raw CSV in S3 to asset‑level insights in DynamoDB and Athena.

---

## 🧠 Real‑World Analogy  
Think of **S3** as a smart mailbox. Every time a letter *(CSV)* arrives, a robot *(Lambda)* opens it instantly, reads it, and files it neatly *(DynamoDB)*. No one checks the mailbox manually — and if 100 letters arrive, 100 robots work at once.  
Athena is the archivist: when you need a monthly or yearly report, it searches the archives and hands you the answer in seconds.

---

## 📚 Table of Contents
- Real‑World Analogy
- Project Goals
- Tech Stack
- Folder Structure
- How It Works
- AWS CLI Setup
- Common Errors & Fixes
- AWS Console Steps
- Testing
- Example Queries
- Cleanup
- Final Notes

---

## 🎯 Project Goals
✅ Create a production‑style S3 bucket with partitioned folders  
✅ Deploy a Lambda function to parse LV load CSVs automatically  
✅ Store parsed rows in DynamoDB for fast asset/time lookups  
✅ Query raw S3 data with Athena for batch analytics  
✅ Configure CloudWatch for logging and debugging  
✅ Document key commands and fixes for reproducibility  

---

## 🛠 Tech Stack

| Service      | Purpose |
|--------------|---------|
| AWS S3       | Store raw data and enable event notifications |
| AWS Lambda   | Serverless ingestion & transformation |
| AWS DynamoDB | Queryable storage for processed rows |
| AWS Athena   | SQL over raw partitioned S3 data |
| AWS IAM      | Secure role‑based access |
| AWS CloudWatch | Logging and monitoring |
| Python       | Lambda processing logic |
| GitHub       | Code & documentation |
| CLI / VS Code| Development & testing tools |

---

## 📁 Folder Structure

```
DubeGrid/
├── data/
│   ├── lv_data_0525.csv
│   ├── lv_data_0825.csv
├── lambda/
│   └── ingest_csv/
│       ├── lambda_ingest_csv.py
│       ├── trust-policy.json
│       ├── event.json
│       ├── s3-notify.json
│       ├── function.zip
└── diagrams/
    └── dubegrid_architecture.png
```

---

## ⚙️ How It Works
1. **S3 bucket** `dubegrid-data-ingest` stores LV load monitor CSVs in partitioned folders:
   ```
   raw/prod/lv/y=2025/m=05/
   ```
2. **S3 event** triggers `DubeGridIngestCSV` Lambda on every `.csv` upload.
3. Lambda:
   - Reads the file from S3.
   - Parses CSV rows.
   - Inserts each row into DynamoDB table `DubeGridAssetData`.
4. **DynamoDB** enables asset/time queries.
5. **Athena** runs partition‑aware SQL over raw S3 data for batch analytics.
6. **CloudWatch** logs every execution for debugging and audit.

```
                   ┌──────────────┐
                   │   CSV File   │
                   └──────┬───────┘
                          │
                          v
                 ┌──────────────────┐
                 │    Amazon S3      │
                 │  raw/prod/lv/...  │
                 └──────┬────────────┘
            S3 ObjectCreated (Trigger)
                          │
                          v
              ┌──────────────────────────┐
              │        AWS Lambda         │
              │ Ingest / Parse / Transform│
              └──────┬────────────────────┘
                     │ PutItem (processed rows)
                     v
            ┌──────────────────────────┐
            │     Amazon DynamoDB       │
            │ PK: asset_id  SK: timestamp│
            └──────────────────────────┘
                     
     Logs & Metrics         Query & Results via S3
           │                          ▲
           v                          │
┌───────────────────┐        ┌─────────────────────┐
│ Amazon CloudWatch  │        │   Amazon Athena     │
│ Logs & Metrics     │        │ SQL over S3         │
└───────────────────┘        │ (external table)    │
                              └─────────────────────┘

[IAM: Execution Role & Permissions apply to S3, Lambda, and DynamoDB]


``` 
---

## 🧾 AWS CLI Setup — Core Commands

**S3 Bucket**

```bash
aws s3 mb s3://dubegrid-data-ingest --region us-east-1
```

**IAM Role + Policies**

```bash
aws iam create-role \
  --role-name DubeGridLambdaRole \
  --assume-role-policy-document file://trust-policy.json \
  --region us-east-1

aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy \
  --role-name DubeGridLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**Lambda Deploy**

```bash
zip function.zip lambda_ingest_csv.py
aws lambda create-function \
  --function-name DubeGridIngestCSV \
  --runtime python3.12 \
  --role <Role-ARN> \
  --handler lambda_ingest_csv.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 512
```

**DynamoDB Table**

```bash
aws dynamodb create-table \
  --table-name DubeGridAssetData \
  --attribute-definitions \
    AttributeName=asset_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=S \
  --key-schema \
    AttributeName=asset_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

---

## 🐞 Common Errors & Fixes

❌ **`NoSuchKey` during Lambda test**  
Fix: Ensure the referenced CSV exists in S3 or update `event.json` with an existing key.

❌ **`ResourceNotFoundException` when tailing logs**  
Fix: Attach `AWSLambdaBasicExecutionRole` policy so Lambda can write CloudWatch logs.

❌ **Lambda not triggering on upload**  
Fix: Add `lambda:AddPermission` for S3 principal and configure `put-bucket-notification-configuration`.

❌ **Athena column type mismatch**  
Fix: Ensure table schema matches CSV column order exactly.

---

## 🖥 AWS Console Steps
- Enable S3 event notifications (if not using CLI config).
- Verify Lambda trigger is active under *Configuration → Triggers*.
- Use *CloudWatch Logs* to view handler output and debug.
- In Athena: set a query results location and run `MSCK REPAIR TABLE lv_data;`.

---

## 🧪 Testing
**Manual Invoke**
```bash
aws lambda invoke \
  --function-name DubeGridIngestCSV \
  --payload fileb://event.json \
  output.json
```

**End‑to‑End Event**
```bash
aws s3 cp lv_data_0525.csv \
  s3://dubegrid-data-ingest/raw/prod/lv/y=2025/m=05/
```
Tail logs:
```bash
aws logs tail /aws/lambda/DubeGridIngestCSV --follow
```

**Athena Query**
```sql
SELECT substation_name, AVG(value) AS avg_load
FROM lv_data
WHERE y='2025' AND m='05'
GROUP BY substation_name
ORDER BY avg_load DESC;
```

---

## 🧹 Cleanup
- Empty & delete S3 bucket:
  ```bash
  aws s3 rb s3://dubegrid-data-ingest --force
  ```
- Delete Lambda function and IAM role.
- Drop DynamoDB and Athena tables if no longer needed.

---

## 📝 Final Notes
DubeGrid demonstrates **serverless event‑driven ingestion**, **structured storage**, and **cloud analytics** in AWS.  
It’s modular — ready for:
- Real‑time streams (Kinesis/SNS).
- Curated S3 zones with Parquet.
- Visual dashboards in QuickSight or Streamlit.
