# COSC2821 Cloud Developing — Assignment 2.1
**RMIT University | Semester 2, 2025**

A full-stack serverless cloud application built on AWS for a fictional online education institute called **CloudGuru**. The system handles course registration using a serverless, event-driven architecture deployed on AWS Academy Learner Lab.

---

## Architecture Overview

```
User Client (Browser)
    └── S3 Static Website (index.html)
            └── API Gateway REST API (s4088056-RESTAPI)
                    ├── GET  /records                      → Lambda: getRecord       → DynamoDB
                    ├── POST /records                      → Step Functions Workflow
                    │                                           ├── Lambda: validateRecord
                    │                                           ├── Lambda: saveRecord → DynamoDB
                    │                                           └── SNS: AddedRecord   → SQS + Email
                    └── GET  /{student_name}/{course_year} → Lambda: getRecord       → DynamoDB
```

![Step Functions Diagram](docs/stepfunctions_diagram.png)

**AWS Services:** DynamoDB · Lambda (Python 3.11) · API Gateway · Step Functions · SNS · SQS · S3 · ECR · Docker · CloudShell

---

## Tasks Completed

| Task | Description | Marks |
|------|-------------|-------|
| A | Docker container built with `httpd:2.4`, tagged as `s4088056`, pushed to ECR | 4 |
| B | DynamoDB table `Course_Registration` with GSI, data loaded via Python/Boto3 | 6 |
| C | 3 Lambda functions: `getRecord`, `validateRecord`, `saveRecord` | 5 |
| D | SNS topic + SQS queue with email subscription and test message | 3 |
| E | Step Functions state machine: ValidateRecord → SaveRecord → SNSSendMessage | 5 |
| F | REST API Gateway with GET/POST/GET methods, deployed to `dev` stage | 7 |
| G | HTML frontend hosted on S3 as static website | 7 |

---

## Repository Structure

```
├── code/
│   ├── docker/
│   │   ├── Dockerfile              # httpd:2.4 base image
│   │   └── s4088056.html           # Served HTML page
│   ├── dynamodb/
│   │   ├── records.json            # 7 course registration records (DynamoDB JSON format)
│   │   └── insert_records.py       # Boto3 batch insert script
│   ├── lambda/
│   │   ├── getRecord.py            # Query by primary index or GSI
│   │   ├── validateRecord.py       # Validate required fields + format
│   │   └── saveRecord.py           # Insert record into DynamoDB
│   └── frontend/
│       └── index.html              # S3-hosted static website
├── docs/
│   ├── stepfunctions_diagram.png   # Step Functions workflow diagram
│   ├── TaskA.docx                  # Screenshots: Docker + ECR
│   ├── TaskB.docx                  # Screenshots: DynamoDB setup + queries
│   ├── TASKC.docx                  # Screenshots: Lambda functions + tests
│   ├── TASKD.docx                  # Screenshots: SNS + SQS
│   ├── TASKE.docx                  # Screenshots: Step Functions
│   ├── TASKF.docx                  # Screenshots: API Gateway + curl tests
│   ├── TASKG.docx                  # Screenshots: S3 website + browser demo
│   └── S3websiteURL.txt            # Original S3 website URL
├── .gitignore
└── README.md
```

---

## Key Implementation Details

### Task A — Docker
```dockerfile
FROM httpd:2.4
COPY s4088056.html /usr/local/apache2/htdocs/s4088056.html
EXPOSE 80
```
- Image tagged as `s4088056:latest`, pushed to ECR repo `ecr-s4088056-repo`
- Container named `s4088056_1`, host port `8080` → container port `80`

### Task B — DynamoDB
- **Table:** `Course_Registration`
- **Partition key:** `course_name` (String) | **Sort key:** `student_id` (String)
- **GSI:** `studentname-year-index` on `student_name` + `course_year`
- **Capacity:** 6 RCU / 6 WCU
- First record inserted via CLI, remaining 7 via `insert_records.py`

### Task C — Lambda Functions
| Function | Purpose |
|----------|---------|
| `s4088056-getRecord` | Scan all records or query GSI by name + year |
| `s4088056-validateRecord` | Check all required fields exist and are correctly formatted |
| `s4088056-saveRecord` | Insert a validated record into DynamoDB |

All functions: Python 3.11 · 512MB memory · 3 min timeout

### Task E — Step Functions Workflow
```
Start
  └── ValidateRecord (Lambda)
        ├── [statusCode = 200] → SaveRecord (Lambda)
        │       ├── [statusCode = 200] → SNSSendMessage → End
        │       └── [Default] → Fail
        └── [Default] → Fail (1)
```

### Task F — API Gateway Endpoints
| Method | Resource | Backend |
|--------|----------|---------|
| GET | `/records` | Lambda: `s4088056-getRecord` |
| POST | `/records` | Step Functions: `s4088056-AddRecordWorkflow` |
| GET | `/{student_name}/{course_year}` | Lambda: `s4088056-getRecord` |

Deployed to stage: `dev` · Region: `us-east-1`

---

## Live Demo
The static website was hosted at:
`http://cosc2821-s4088056.s3-website-us-east-1.amazonaws.com/`

> ⚠️ The AWS Academy Learner Lab environment expires at end of semester. The API Gateway endpoints and live AWS resources are no longer active. All source code, configs, and screenshots are preserved in this repository.

---

## Tech Stack
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-httpd:2.4-blue?logo=docker)
![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-blue?logo=amazondynamodb)
