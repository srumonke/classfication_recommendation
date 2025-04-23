# 🤖 ClassifyBot

ClassifyBot is a smart Discord bot that classifies table column sensitivity as **public**, **private**, or **secret** using a trained Random Forest model. It's built for intelligent cloud data governance with user feedback, retraining, and GCP deployment support.

---

## 🌟 Features

- Predicts sensitivity of table columns using ML
- Accepts feedback and updates its model dynamically
- Supports Discord chat commands for classification, training, and retraining
- Deployed using Docker and Google Cloud Run Jobs
- Secrets (like the Discord token) managed securely using GCP Secret Manager
- Fully automated CI/CD via GitHub Actions

---

## 💬 Bot Commands

| Command     | Function                                                                 |
|-------------|--------------------------------------------------------------------------|
| `!classify` | Classify a column. Format: `Table, Column, Type, Example`                |
| `!train`    | Add a new training record. Format: `Table, Column, Type, Sensitivity, Example` |
| `!retrain`  | Retrain the model with all available data                                |
| `!exit`     | Shutdown the bot                                                         |
| `!help`     | Show help message                                                        |

---

## 🧠 How It Works

The bot uses:
- `train_dataset.csv` for initial training data
- `feedback_data.csv` to store real-time feedback from users
- A **Random Forest classifier** trained with scikit-learn
- Discord.py for bot interactions

---

## 🧪 Local Setup

```bash
pip install -r requirements.txt
python bot.py
```

Ensure you have `DISCORD_TOKEN` set in your environment or read from GCP Secret Manager in production.

---

## 🚀 Cloud Deployment (GCP)

We use GitHub Actions to build and deploy this bot as a Cloud Run Job.

### 📁 .github/workflows/deploy.yml

- On `main` branch push/PR:
  - Authenticates using GCP service account
  - Builds and pushes Docker image to Artifact Registry
  - Deploys or updates a Cloud Run Job
  - Executes the Job immediately

See [`deploy.yml`](.github/workflows/deploy.yml) for full setup.

---

## 🔐 Secret Management

Create a secret in GCP Secret Manager for DISCORD_TOKEN

Grant access to the GitHub Actions service account:
```bash
gcloud secrets add-iam-policy-binding DISCORD_TOKEN \
--member="serviceAccount:<service-account-email>" \
--role="roles/secretmanager.secretAccessor"
```

---

## 🐳 Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
```

---

## 📊 Diagrams

- [`system_design.excalidraw`](system_design.excalidraw) — Architecture design (can be opened in [Excalidraw](https://excalidraw.com))
- [`discord_flow_diagram.md`](discord_flow_diagram.md) — Discord interaction flow (diagram as markdown)

---

## 📁 Project Structure

```
.
├── bot.py
├── train_dataset.csv
├── feedback_data.csv
├── Dockerfile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── deploy.yml
├── system_design.excalidraw
├── discord_flow_diagram.md
└── README.md
```

---

## 🛠 Tech Stack

- Python, Discord.py, scikit-learn, pandas
- Docker
- Google Cloud Platform: Artifact Registry, Cloud Run, Secret Manager
- GitHub Actions for CI/CD

---

##  📬 Contributions
Want to improve the bot or the classification model? Open issues, submit pull requests, or drop suggestions!

---

##  ⚠️ Disclaimer
This project is built using synthetic data and is for educational and research purposes only. It does not expose real user information.
