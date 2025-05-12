# 🤖 ClassifyBot

ClassifyBot is a smart Discord bot that classifies table column sensitivity as public, private, or secret using a trained Random Forest model. It's built for intelligent cloud data governance with user feedback, retraining, and GCP deployment support.

---

## 🌟 Features

- Predicts sensitivity of table columns using ML  
- Accepts feedback and updates its model dynamically  
- Supports Discord chat commands for classification, training, and retraining  
- Deployed using Docker and Google Cloud Run Jobs  
- Secrets managed securely via GCP Secret Manager  
- Fully automated CI/CD using GitHub Actions  
- ✅ Triggered by GCS file uploads to launch the bot via Cloud Run Job  

---

## 💬 Bot Commands

| Command     | Function                                                   |
|-------------|------------------------------------------------------------|
| `!classify` | Classify a column. Format: Table, Column, Type, Example    |
| `!train`    | Add a new training record                                  |
| `!retrain`  | Retrain the model with all available data                  |
| `!exit`     | Shutdown the bot                                           |
| `!help`     | Show help message                                          |

---

## 🧠 How It Works

The bot uses:
- `train_dataset.csv` for initial training data  
- `feedback_data.csv` for real-time user feedback  
- A Random Forest classifier trained with `scikit-learn`  
- `discord.py` for bot interactions  
- Deployed using Docker and Cloud Run Jobs  

---

## 🧪 Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ClassifyBot.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot locally:
   ```bash
   python bot.py
   ```

Make sure you have `DISCORD_TOKEN` set in your environment or access it via GCP Secret Manager for production deployment.

---

## 🚀 Cloud Deployment (GCP)

We use **GitHub Actions** to deploy this bot to **Cloud Run Job**. The deployment will automatically build the Docker image, push it to Artifact Registry, and deploy it to Cloud Run.

### 📁 `.github/workflows/deploy.yml`

This workflow is triggered when there’s a push to the `main` branch:
- Authenticates using a GCP service account
- Builds and pushes the Docker image to Artifact Registry
- Deploys/updates the Cloud Run Job
- Immediately executes the Job

---

## 🔐 Secret Management

1. Create the secret for the `DISCORD_TOKEN`:
   ```bash
   gcloud secrets create DISCORD_TOKEN --replication-policy="automatic"
   ```

2. Add IAM policy binding to give the GitHub Actions service account access to the secret:
   ```bash
   gcloud secrets add-iam-policy-binding DISCORD_TOKEN      --member="serviceAccount:<github-service-account>"      --role="roles/secretmanager.secretAccessor"
   ```

---

## ✅ Storage Trigger Test Case (Cloud Function + Cloud Run Job)

This test case triggers the `discord-bot-job` whenever a new file is uploaded to a GCS bucket.

### 🔹 Architecture

1. **GCS Upload** → **Pub/Sub** → **Cloud Function** → **Cloud Run Job**

### 🔹 Setup Steps

#### 1. Create Pub/Sub Topic

```bash
gcloud pubsub topics create discord-bot-upload-topic
```

#### 2. Link GCS Bucket to Pub/Sub

```bash
gsutil notification create -t discord-bot-upload-topic -f json gs://discord-bot-test-bucket
```

#### 3. Cloud Function Code

##### `main.py`
```python
import functions_framework
from google.cloud import run_v2
import base64

@functions_framework.cloud_event
def trigger_discord_bot_job(cloud_event):
    project = "big-formula-457308-s5"
    region = "europe-west1"
    job = "discord-bot-job"
    client = run_v2.JobsClient()
    job_path = f"projects/{project}/locations/{region}/jobs/{job}"
    try:
        response = client.run_job(name=job_path)
        print(f"Triggered job: {response.name}")
    except Exception as e:
        print(f"Error triggering job: {e}")
```

##### `requirements.txt`
```
functions-framework
google-cloud-run
```

#### 4. Deploy the Function
```bash
gcloud functions deploy trigger-discord-bot-job   --runtime python311   --entry-point trigger_discord_bot_job   --trigger-topic discord-bot-upload-topic   --region europe-west1   --project big-formula-457308-s5   --service-account 356713197729-compute@developer.gserviceaccount.com
```

---

### 🔐 IAM Permissions

#### Cloud Function Service Account (`356713197729-compute@developer.gserviceaccount.com`)
```bash
# Allow invoking Cloud Run Job
gcloud projects add-iam-policy-binding big-formula-457308-s5   --member="serviceAccount:356713197729-compute@developer.gserviceaccount.com"   --role="roles/run.invoker"

# Allow reading Pub/Sub topic
gcloud pubsub topics add-iam-policy-binding discord-bot-upload-topic   --member="serviceAccount:356713197729-compute@developer.gserviceaccount.com"   --role="roles/pubsub.subscriber"
```

---

## 🐳 Dockerfile

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
```

---

## 📁 Project Structure

```
.
├── bot.py
├── train_dataset.csv
├── feedback_data.csv
├── Dockerfile                 
├── .github/
│   └── workflows/
│       └── deploy.yml
├── system_design.excalidraw
├── discord_flow_diagram.md
└── README.md
```

---

## 📊 Diagrams

- `system_design.excalidraw` — Architecture design (open with Excalidraw)
- `discord_flow_diagram.md` — Discord interaction flow

---

## 🛠 Tech Stack

- **Python**, **Discord.py**, **scikit-learn**, **pandas**
- **Docker**
- **Google Cloud Platform**: Artifact Registry, Cloud Run, Cloud Functions, Pub/Sub, Secret Manager
- **GitHub Actions** for CI/CD

---
---

##  📬 Contributions
Want to improve the bot or the classification model? Open issues, submit pull requests, or drop suggestions!

---

##  ⚠️ Disclaimer
This project is built using synthetic data and is for educational and research purposes only. It does not expose real user information.
