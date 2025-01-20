import random
import faker
import csv

# Initialize Faker for generating random values
fake = faker.Faker()

# Define 100 meaningful column names with their corresponding data types
column_data = {
    "FullName": "TEXT", "Age": "INT", "Gender": "TEXT", "DateOfBirth": "DATE", "Address": "TEXT", 
    "PhoneNumber": "TEXT", "Email": "TEXT", "Occupation": "TEXT", "Salary": "DECIMAL", 
    "Country": "TEXT", "State": "TEXT", "City": "TEXT", "ZipCode": "TEXT", "MaritalStatus": "TEXT", 
    "ChildrenCount": "INT", "SpouseName": "TEXT", "Hobby": "TEXT", "SocialSecurityNumber": "TEXT", 
    "TaxID": "TEXT", "CreditCardNumber": "TEXT", "BankAccountNumber": "TEXT", "LoanAmount": "DECIMAL", 
    "InvestmentValue": "DECIMAL", "MortgageAmount": "DECIMAL", "HealthInsuranceNumber": "TEXT", 
    "MedicalHistory": "TEXT", "Diagnosis": "TEXT", "Prescription": "TEXT", "InsuranceClaims": "TEXT", 
    "PerformanceReviews": "TEXT", "PaymentHistory": "TEXT", "TransactionAmount": "DECIMAL", 
    "TransactionDate": "DATE", "PaymentMethod": "TEXT", "BrowserType": "TEXT", "LoginTime": "DATE", 
    "LastLoginTime": "DATE", "ProfilePictureURL": "TEXT", "IP_Address": "TEXT", "DeviceType": "TEXT", 
    "SocialMediaHandle": "TEXT", "AccountStatus": "TEXT", "MembershipStatus": "TEXT", 
    "PurchaseHistory": "TEXT", "Wishlist": "TEXT", "CartItems": "TEXT", "FavoriteProducts": "TEXT", 
    "CustomerFeedback": "TEXT", "ProductReviews": "TEXT", "OrderHistory": "TEXT", 
    "ShippingAddress": "TEXT", "BillingAddress": "TEXT", "DiscountCoupons": "TEXT", "LoyaltyPoints": "INT", 
    "EmployeeID": "TEXT", "Department": "TEXT", "JobTitle": "TEXT", "JobDescription": "TEXT", 
    "WorkLocation": "TEXT", "StartDate": "DATE", "EndDate": "DATE", "ContractType": "TEXT", 
    "EmployeePerformance": "TEXT", "ManagerName": "TEXT", "TeamMembers": "TEXT", "LeaveBalance": "INT", 
    "HealthRecord": "TEXT", "FamilyHistory": "TEXT", "EmergencyContact": "TEXT", "EmployeeBenefits": "TEXT", 
    "AnnualSalary": "DECIMAL", "BonusAmount": "DECIMAL", "TaxRate": "DECIMAL", "RetirementPlan": "TEXT", 
    "CompanyStockOptions": "TEXT", "PayrollDetails": "TEXT", "WorkEmail": "TEXT", "WorkPhone": "TEXT", 
    "CorporateCreditCard": "TEXT", "BusinessTravelHistory": "TEXT", "ConferenceAttendance": "TEXT", 
    "SystemAccessLevel": "TEXT", "LoginAttempts": "INT", "FailedLogins": "INT", "APIKey": "TEXT", 
    "SessionToken": "TEXT", "PasswordHash": "TEXT", "SecurityQuestions": "TEXT", "TwoFactorEnabled": "BOOLEAN", 
    "AuditLogs": "TEXT", "LastPasswordChange": "DATE", "SecurityBreachHistory": "TEXT", "NetworkAccessLogs": "TEXT", 
    "AccessControlLists": "TEXT", "ServerIPs": "TEXT", "FirewallRules": "TEXT", "BackupHistory": "TEXT", 
    "DisasterRecoveryPlan": "TEXT", "IncidentReports": "TEXT", "RiskAssessment": "TEXT", "ComplianceReports": "TEXT", 
    "SecurityPolicies": "TEXT", "DataEncryptionKeys": "TEXT", "SensitiveDataAccess": "TEXT", "DocumentVersion": "TEXT", 
    "ConfidentialReports": "TEXT", "InternalMeetings": "TEXT", "CompanyBudget": "DECIMAL", 
    "LegalDocuments": "TEXT", "VendorContracts": "TEXT", "SupplierDetails": "TEXT", "ThirdPartyContracts": "TEXT", 
    "InternalEmails": "TEXT", "MeetingNotes": "TEXT", "ExpenseReports": "TEXT", "ResourceAllocation": "TEXT", 
    "ProjectBudget": "DECIMAL", "ProjectTimeline": "TEXT", "TaskAssignments": "TEXT", "TeamCollaboration": "TEXT", 
    "ProjectFeedback": "TEXT", "ClientContracts": "TEXT", "ClientInvoices": "TEXT", "CustomerSupportTickets": "TEXT"
}

# Define sensitivity levels
sensitivity_levels = ['Public', 'Private', 'Confidential', 'Secret']

# Function to generate random example values based on the column name and data type
def generate_value(column_name, data_type):
    if data_type == 'TEXT':
        if column_name in ["FullName", "SpouseName", "EmployeeID", "TeamMembers", "ManagerName"]:
            return fake.name()
        elif column_name in ["Email", "WorkEmail"]:
            return fake.email()
        elif column_name in ["PhoneNumber"]:
            return fake.phone_number()
        elif column_name in ["Address"]:
            return fake.address()
        elif column_name in ["Country", "State", "City"]:
            return fake.city()
        elif column_name in ["SocialMediaHandle"]:
            return fake.user_name()
        else:
            return fake.text(max_nb_chars=50)

    elif data_type == 'DECIMAL':
        return round(random.uniform(1000, 100000), 2)  # Random decimal value

    elif data_type == 'VARCHAR':
        return fake.word()  # Single word for VARCHAR type

    elif data_type == 'INT':
        if column_name in ["Age", "ChildrenCount", "LoanAmount", "TransactionAmount", "Salary"]:
            return random.randint(18, 100)  # Random integer for age or salary, etc.
        else:
            return random.randint(1, 1000)  # Random integer

    elif data_type == 'DATE':
        return fake.date()  # Random date value

    elif data_type == 'BOOLEAN':
        return random.choice([True, False])  # Random Boolean value

# Open a CSV file for writing
with open('generated_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Table Name", "Column Name", "Data Type", "Sensitivity Level", "Example Values"])
    
    # Create 10,000 rows
    for i in range(10000):
        table_name = f"Table_{random.randint(1, 20)}"
        column_name = random.choice(list(column_data.keys()))
        data_type = column_data[column_name]
        sensitivity_level = random.choice(sensitivity_levels)
        example_value = generate_value(column_name, data_type)
        
        # Write a row
        writer.writerow([table_name, column_name, data_type, sensitivity_level, example_value])

print("CSV file with 10,000 rows generated successfully!")
