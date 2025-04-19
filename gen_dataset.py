import random
import faker
import csv
import uuid
import hashlib
import secrets

# Initialize Faker
fake = faker.Faker()

# Define a mapping of meaningful tables to their relevant columns, types, and sensitivity
tables = {
    "Employee": {
        "FullName": ("TEXT", "Private"),
        "Age": ("INT", "Private"),
        "Gender": ("TEXT", "Private"),
        "DateOfBirth": ("DATE", "Private"),
        "Address": ("TEXT", "Private"),
        "PhoneNumber": ("TEXT", "Private"),
        "Email": ("TEXT", "Private"),
        "EmployeeID": ("TEXT", "Private"),
        "Department": ("TEXT", "Private"),
        "JobTitle": ("TEXT", "Private"),
        "Salary": ("DECIMAL", "Confidential"),
        "ManagerName": ("TEXT", "Private"),
    },
    "Finance": {
        "BankAccountNumber": ("TEXT", "Confidential"),
        "LoanAmount": ("DECIMAL", "Confidential"),
        "InvestmentValue": ("DECIMAL", "Confidential"),
        "CreditCardNumber": ("TEXT", "Secret"),
        "TaxID": ("TEXT", "Secret"),
        "CompanyBudget": ("DECIMAL", "Confidential"),
    },
    "Healthcare": {
        "MedicalHistory": ("TEXT", "Confidential"),
        "Diagnosis": ("TEXT", "Confidential"),
        "Prescription": ("TEXT", "Confidential"),
        "HealthInsuranceNumber": ("TEXT", "Secret"),
        "EmergencyContact": ("TEXT", "Private"),
    },
    "ITSecurity": {
        "APIKey": ("TEXT", "Secret"),
        "SessionToken": ("TEXT", "Secret"),
        "PasswordHash": ("TEXT", "Secret"),
        "TwoFactorEnabled": ("BOOLEAN", "Confidential"),
        "LoginAttempts": ("INT", "Private"),
    },
    "Sales": {
        "CustomerFeedback": ("TEXT", "Public"),
        "OrderHistory": ("TEXT", "Public"),
        "DiscountCoupons": ("TEXT", "Public"),
        "LoyaltyPoints": ("INT", "Private"),
        "FavoriteProducts": ("TEXT", "Public"),
    }
}

# Flatten column details
column_details = []
for table, columns in tables.items():
    for column, (dtype, sensitivity) in columns.items():
        column_details.append((table, column, dtype, sensitivity))

# Generate realistic values
def generate_value(column, dtype):
    if column == "Gender":
        return random.choice(["male", "female", "trans"])
    elif column == "APIKey":
        return secrets.token_hex(16)  # 32-character hex string
    elif column == "SessionToken":
        return str(uuid.uuid4())  # UUID v4 format
    elif column == "PasswordHash":
        return hashlib.sha256(fake.password().encode()).hexdigest()  # Simulated SHA-256 password hash
    elif dtype == "TEXT":
        if column in ["FullName", "ManagerName", "EmergencyContact"]:
            return fake.name()
        elif "Email" in column:
            return fake.email()
        elif "Phone" in column:
            return fake.phone_number()
        elif "Address" in column:
            return fake.address()
        elif column in ["BankAccountNumber", "CreditCardNumber", "HealthInsuranceNumber", "TaxID"]:
            return fake.iban()
        else:
            return fake.text(max_nb_chars=20)
    elif dtype == "INT":
        return random.randint(18, 100)
    elif dtype == "DECIMAL":
        return round(random.uniform(1000, 100000), 2)
    elif dtype == "DATE":
        return fake.date()
    elif dtype == "BOOLEAN":
        return random.choice([True, False])

# Create CSV file
with open('classified_dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Table Name", "Column Name", "Data Type", "Sensitivity Level", "Example Values"])

    for _ in range(10000):
        table_name, column_name, data_type, sensitivity_level = random.choice(column_details)
        example_value = generate_value(column_name, data_type)
        writer.writerow([table_name, column_name, data_type, sensitivity_level, example_value])

print("CSV file 'classified_dataset.csv' with 10,000 rows generated successfully!")
