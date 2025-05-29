import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

# Function to create a connection to MySQL
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Successfully connected to MySQL!")
    except Error as e:
        print(f"An error occurred: {e}")
    return connection

# Function to create the table to store exp data
def create_table_exp_data(connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exp_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255),
        exp_date DATE,
        UNIQUE(user_name, exp_date)  -- Adds a uniqueness constraint
    )
    ''')
    connection.commit()

# Define the authorization token for the API
token = "your_token_here"

# Function to make a request to the API
def fetch_planning_data(date):
    url = 'your_api_here'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    payload = {
        "team": ["team"],
        "startDate": date,
        "endDate": date
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Function to find data with "exp"
def find_exp_data(month, year):
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{(datetime(year, month + 1, 1) - timedelta(days=1)).day}"

    exp_entries = []

    # Iterate through each day of the month
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    while current_date <= datetime.strptime(end_date, "%Y-%m-%d"):
        date_str = current_date.strftime("%Y-%m-%d")
        data = fetch_planning_data(date_str)

        if data.get('success'):
            for entry in data['data']:
                if "exp" in entry['Morning']:
                    user_name = entry['user_name']  # Assuming `user_name` is available in the entry
                    exp_entries.append((user_name, date_str))

        current_date += timedelta(days=1)

    return exp_entries

# Function to check if the data already exists in the table
def check_exp_data_exists(connection, user_name, exp_date):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM exp_data WHERE user_name = %s AND exp_date = %s", (user_name, exp_date))
    count = cursor.fetchone()[0]
    return count > 0

# Function to insert data into the exp_data table
def insert_exp_data(connection, user_name, exp_date):
    if not check_exp_data_exists(connection, user_name, exp_date):
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO exp_data (user_name, exp_date) VALUES (%s, %s)", (user_name, exp_date))
            connection.commit()
            print(f"Data successfully inserted: {user_name} on {exp_date}.")
        except Error as e:
            print(f"An error occurred while inserting data: {e}")
    else:
        print(f"The user {user_name} already exists on {exp_date}. Not inserted.")

# Database configurations
host_name = "your_host"
user_name = "your_username"
user_password = "your_password"
db_name = "smb_grafana"

# Connect to the MySQL database
connection = create_connection(host_name, user_name, user_password, db_name)

if connection:
    # Create the table if it doesn't exist
    create_table_exp_data(connection)

    # Get the current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Execute the search for exp data
    exp_data_entries = find_exp_data(current_month, current_year)

    # Insert the data into the exp_data table
    for user_name, exp_date in exp_data_entries:
        insert_exp_data(connection, user_name, exp_date)

    # Close the connection to the database
    connection.close()
