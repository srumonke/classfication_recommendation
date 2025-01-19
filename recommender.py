import discord
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Create a client instance of the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load your dataset
data = pd.read_csv('training_sensitivity.csv')  # Update with your file path
data["Features"] = data["Table Name"] + " " + data["Column Name"] + " " + data["Data Type"] + " " + data["Example Values"].astype(str)

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
y_pred = pipeline.predict(X_test)
print(f"Initial Model Accuracy: {accuracy_score(y_test, y_pred)}")

# Function to save new labeled data
def save_feedback(input_data, predicted_sensitivity, feedback):
    # Save this to a CSV or database for retraining
    new_data = pd.DataFrame({
        'Features': [input_data],
        'Sensitivity Level': [predicted_sensitivity] if feedback == 'yes' else ['None']
    })
    new_data.to_csv('feedback_data.csv', mode='a', header=False, index=False)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!classify'):
        # Collect the data input from the user
        user_input = message.content[9:].strip()
        
        if not user_input:
            await message.channel.send("Please provide the data input in the format: 'Table Name, Column Name, Data Type, Example Value'.")
            return
        
        # Predict sensitivity
        prediction = pipeline.predict([user_input])[0]
        await message.channel.send(f"Recommendation: The sensitivity level for '{user_input}' is {prediction}. Do you accept this recommendation? (yes/no)")
        
        # Wait for user response
        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content.lower() in ['yes', 'no']

        try:
            response = await client.wait_for('message', check=check, timeout=60)
            
            if response.content.lower() == 'yes':
                await message.channel.send("Thank you! We will use this feedback to improve the system.")
                # Save feedback to improve the system
                save_feedback(user_input, prediction, 'yes')
            else:
                await message.channel.send("Understood. We will not use this recommendation.")
                # Optionally, save this feedback as well
                save_feedback(user_input, prediction, 'no')
            
        except Exception as e:
            await message.channel.send("No response received in time. Please try again.")
            print(e)

# Load the token from a file and run the bot
with open('token.txt', 'r') as file:
    token = file.read().strip()

client.run(token)
