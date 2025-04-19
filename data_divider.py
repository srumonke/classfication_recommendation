import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("classified_dataset.csv")

# Split into train (80%) and validation (20%)
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the splits
train_df.to_csv("train_dataset.csv", index=False)
val_df.to_csv("val_dataset.csv", index=False)

print("Training and validation datasets saved as 'train_dataset.csv' and 'val_dataset.csv'")
