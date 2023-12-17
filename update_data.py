from tabulate import tabulate
import re
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from connect_db import conn_db

def get_update_input(column_list):
    """
    Function to get user input for updating employee data columns.

    Parameters:
    - column_list (dict): A dictionary containing sections as keys and lists of column names as values.

    Returns:
    - list: A list containing the selected column name and the new value.
    """
    column_name = input("Choose a column: ")
    if column_name in column_list:
        value = input("Enter new value: ")
        return [column_name, value]
    else:
        print("Invalid column name. Please choose from the columns list.")

def get_yes_no_input(message):
    """
    Function to get user input for yes or no questions.

    Parameters:
    - message (str): The message to display when asking for input.

    Returns:
    - str: 'y' if the user enters 'yes', 'n' if the user enters 'no'.
    """
    while True:
        user_input = input(message)
        if user_input.lower() in ["y", "n"]:
            return user_input.lower()
        print("Please enter a valid input (Y/N).")

column_list = {
    "IDENTITY DATA": ["name", "id_number", "address", "dob", "phone", "email"],
    "JOB DATA": ["position", "departments", "status", "salary", "hire_date"],
    "INSURANCE DATA": ['insurance_status', 'insurance_name', 'insurance_number']
}

def update_data_employee():
    """
    Function to update employee data based on user input.

    The function prompts the user to enter an employee ID and displays the corresponding data.
    The user can then choose columns to update and provide new values.
    The function displays the old and new data for confirmation before updating the database.

    Note: This function assumes the existence of a BigQuery table named 'voltaic-reducer-399714.inti_corpora.employee_data'.

    Returns:
    - None
    """
    true_data = "n"
    
    # Loop until the user confirms the displayed data
    while true_data == "n":
        employee_id = input("Enter Employee ID Number : ")

        # Construct a SELECT query to retrieve employee data based on the entered ID
        query = f"""
            SELECT name, id_number, address, position, departments
            FROM voltaic-reducer-399714.inti_corpora.employee_data
            WHERE id_number = {employee_id}
        """

        # Execute the query and retrieve the results
        results = conn_db(query)
        results_df = results.to_dataframe()

        # Display the retrieved data for user confirmation
        print(tabulate(results_df, headers=results_df.keys(), tablefmt='psql', showindex=False))

        # Ask the user if the displayed data is correct
        true_data = get_yes_no_input("Is the displayed data correct?(Y/N): ")

    print("=" * 75)
    print(("\t" * 8) + "COLUMN LIST")
    
    # Display the available columns for each section
    for section, column_name in column_list.items():
        print("=" * 75)
        print(section)
        for i, value in enumerate(column_name):
            print(f"{i + 1}. {value}")
    print("=" * 75)

    changes_list = []

    # Prompt the user to choose columns to update and provide new values
    add_changes = "y"
    merged_list = [column for sublist in column_list.values() for column in sublist]
    
    while add_changes.lower() == "y":
        update_data = get_update_input(merged_list)
        changes_list.append(update_data)
        add_changes = get_yes_no_input("Are there still columns that you want to change? (Y/N): ")

    # Construct a SELECT query to check the old data for the updated columns
    query_checking = f"""
        SELECT {", ".join(changes_list[i][0] for i in range(len(changes_list)))}
        FROM voltaic-reducer-399714.inti_corpora.employee_data
        WHERE id_number = {employee_id}
    """

    # Execute the query and retrieve the old data
    checking = conn_db(query_checking)
    checking_df = checking.to_dataframe()
    checking_df = checking_df.astype(str)

    # Display the OLD DATA
    print("=" * 75)
    print("OLD DATA")
    print("=" * 75)
    print(tabulate(checking_df, headers=checking_df.keys(), tablefmt='psql', showindex=False))

    # Update the values in the DataFrame based on user input
    for check in changes_list:
        checking_df.at[0, check[0]] = check[1]

    # Display the NEW DATA
    print("=" * 75)
    print("NEW DATA")
    print("=" * 75)
    print(tabulate(checking_df, headers=checking_df.keys(), tablefmt='psql', showindex=False))

    # Prepare a list for the SET clause in the UPDATE query
    new_change_list = [
        f"{key_change} = {repr(value_change) if key_change not in ['phone', 'insurance_number', 'id_number'] else str(value_change)}"
        for key_change, value_change in changes_list
    ]

    # Construct the UPDATE query
    update_query = f"""
        UPDATE voltaic-reducer-399714.inti_corpora.employee_data
        SET {", ".join(new_change_list)}
        WHERE id_number = {employee_id};
    """

    # Confirm if the displayed data is correct
    true_data = get_yes_no_input("Is the displayed data correct? (Y/N): ")

    # If the data is correct, execute the UPDATE query
    if true_data.lower() == "y":
        conn_db(update_query)
        print("Data has been successfully updated.")
    else:
        print("No changes have been made.")
