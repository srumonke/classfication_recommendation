import discord
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Create a client instance of the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# File path for training data
file_path = 'train_dataset.csv'

# Load dataset or create a new one
if os.path.isfile(file_path):
    data = pd.read_csv(file_path)
else:
    data = pd.DataFrame(columns=["Table Name", "Column Name", "Data Type", "Sensitivity Level", "Example Values"])

data["Features"] = (
    data["Table Name"] + " " + data["Column Name"] + " " + data["Data Type"] + " " + data["Example Values"].astype(str)
)

X = data["Features"]
y = data["Sensitivity Level"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a pipeline model
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500)),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X_train, y_train)

# Evaluate the model
if not X_test.empty:
    y_pred = pipeline.predict(X_test)
    print(f"Initial Model Accuracy: {accuracy_score(y_test, y_pred)}")

# Function to save new labeled data with the same format as the training dataset
def save_feedback(input_data, predicted_sensitivity, feedback):
    parts = input_data.split(",")
    if len(parts) < 4:
        return
    
    table_name = parts[0].strip()
    column_name = parts[1].strip()
    data_type = parts[2].strip()
    example_value = " ".join(parts[3:]).strip()

    new_row = {
        'Table Name': table_name,
        'Column Name': column_name,
        'Data Type': data_type,
        'Sensitivity Level': predicted_sensitivity if feedback == 'yes' else 'None',
        'Example Values': example_value
    }

    feedback_file = 'feedback_data.csv'
    file_exists = os.path.isfile(feedback_file)
    new_data = pd.DataFrame([new_row])
    new_data.to_csv(feedback_file, mode='a', header=not file_exists, index=False)

# Command to display options
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command to show available bot functions
    if message.content.startswith('!help'):
        await message.channel.send(
            "Here are the available commands:\n"
            "`!classify`: Classify a table column's sensitivity level.\n"
            "`!train`: Add new training data.\n"
            "`!retrain`: Retrain the model with updated data.\n"
        )

    # Command to classify input and give recommendation
    if message.content.startswith('!classify'):
        user_input = message.content[9:].strip()
        
        if not user_input:
            await message.channel.send("Please provide the data input in the format: 'Table Name, Column Name, Data Type, Example Value'.")
            return
        
        prediction = pipeline.predict([user_input])[0]
        await message.channel.send(f"Recommendation: The sensitivity level for '{user_input}' is {prediction}. Do you accept this recommendation? (yes/no)")

        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content.lower() in ['yes', 'no']

        try:
            response = await client.wait_for('message', check=check, timeout=60)
            
            if response.content.lower() == 'yes':
                await message.channel.send("Thank you! We will use this feedback to improve the system.")
                save_feedback(user_input, prediction, 'yes')
            else:
                await message.channel.send("Understood. We will not use this recommendation.")
                save_feedback(user_input, prediction, 'no')
            
        except Exception as e:
            await message.channel.send("No response received in time. Please try again.")
            print(e)

    # Command to submit new training data
    if message.content.startswith('!train'):
        user_input = message.content[7:].strip()

        if not user_input:
            await message.channel.send("Please provide the data input in the format: 'Table Name, Column Name, Data Type, Sensitivity Level, Example Value'.")
            return

        try:
            table_name, column_name, data_type, sensitivity_level, example_value = [x.strip() for x in user_input.split(',')]
        except ValueError:
            await message.channel.send("Invalid input format. Ensure the input has 5 comma-separated values.")
            return

        new_row = {
            'Table Name': table_name,
            'Column Name': column_name,
            'Data Type': data_type,
            'Sensitivity Level': sensitivity_level,
            'Example Values': example_value
        }

        try:
            file_exists = os.path.isfile(file_path)
            new_data = pd.DataFrame([new_row])
            new_data.to_csv(file_path, mode='a', header=not file_exists, index=False)
            await message.channel.send("Thank you! Your training data has been added.")
        except Exception as e:
            await message.channel.send("An error occurred while saving your data. Please try again.")
            print(e)

    # Command to retrain the model
    if message.content.startswith('!retrain'):
        try:
            data = pd.read_csv(file_path)
            data["Features"] = (
                data["Table Name"] + " " + data["Column Name"] + " " + data["Data Type"] + " " + data["Example Values"].astype(str)
            )
            X = data["Features"]
            y = data["Sensitivity Level"]
            pipeline.fit(X, y)
            await message.channel.send("The model has been successfully retrained with the new data!")
        except Exception as e:
            await message.channel.send("An error occurred during retraining. Please check the training data.")
            print(e)

# Load the token from a file and run the bot
with open('token.txt', 'r') as file:
    token = file.read().strip()

client.run(token)
