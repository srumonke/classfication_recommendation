import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Step 1: Load the dataset
file_path = "large_meaningful_sensitivity_dataset.csv"
data = pd.read_csv(file_path)

# Step 2: Data Preprocessing
data["Features"] = data["Table Name"] + " " + data["Column Name"] + " " + data["Data Type"] + " " + data["Example Values"].astype(str)
X = data["Features"]
y = data["Sensitivity Level"]

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Create a pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500)),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Step 5: Train the model
pipeline.fit(X_train, y_train)

# Step 6: Test the model
y_pred = pipeline.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Step 7: Function to classify sensitivity dynamically
def classify_sensitivity():
    """
    Dynamically collect input data and classify sensitivity levels.
    """
    print("Enter new data to classify sensitivity (enter 'done' to stop):")
    new_data = []
    
    while True:
        table_name = input("Table Name: ")
        if table_name.lower() == "done":
            break
        column_name = input("Column Name: ")
        data_type = input("Data Type: ")
        example_value = input("Example Value: ")
        
        new_data.append({
            "Table Name": table_name,
            "Column Name": column_name,
            "Data Type": data_type,
            "Example Values": example_value
        })
    
    if new_data:
        new_df = pd.DataFrame(new_data)
        new_df["Features"] = (
            new_df["Table Name"] + " " +
            new_df["Column Name"] + " " +
            new_df["Data Type"] + " " +
            new_df["Example Values"]
        )
        new_df["Predicted Sensitivity"] = pipeline.predict(new_df["Features"])
        print("\nClassified Data:")
        print(new_df)
    else:
        print("No data provided.")

# Step 8: Classify sensitivity for user input
classify_sensitivity()
