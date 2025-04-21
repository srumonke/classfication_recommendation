# Discord Bot Command Flowchart

This diagram shows how the bot responds to different commands and user interactions.

```mermaid
flowchart TD
    A[User Sends Command in Discord] --> B{Command Type?}

    B -->|!classify| C[AI Model Predicts Sensitivity]
    C --> D{User Accepts Prediction?}
    D -->|Yes| E[Save Prediction to feedback_data.csv]
    D -->|No| F[Ask for Correct Sensitivity Level]
    F --> G[User Provides Correction]
    G --> H[Save Correction to feedback_data.csv]

    B -->|!train| I[Parse 5 Fields from User]
    I --> J[Append to train_dataset.csv]

    B -->|!retrain| K[Reload train_dataset.csv]
    K --> L[Retrain Pipeline Model]

    B -->|!help| M[Display Help Message]
    B -->|!exit| N[Shutdown Discord Bot]

    classDef fileOps fill:#f9f,stroke:#333,stroke-width:1px;
    class E,H,J,K fileOps;
