from tabulate import tabulate
import re
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from connect_db import conn_db

def get_column_input(columns, selected_columns):
    """
    Function to get user input for selecting a column from a list of columns.
    It ensures that the selected column is valid and has not been selected before.

    Parameters:
    - columns: List of available columns.
    - selected_columns: List of columns already selected.

    Returns:
    - The selected column name.
    """
    while True:
        column_name = input("Choose a column: ")
        if column_name.lower() in [x.lower() for x in columns]:
            column_name = column_name if column_name.lower() != "all" else f"*"
            if column_name in selected_columns:
                print("You have selected that column. Please select another column.")
            else:
                return column_name
        else:
            print("Invalid column name. Please choose from the columns list.")


def get_filter_input(filters):
    """
    Function to get user input for selecting a filter from a list of filters.

    Parameters:
    - filters: List of available filters.

    Returns:
    - The selected filter key.
    """
    while True:
        filter_key = input("Choose a filter: ")
        if filter_key in filters:
            return filter_key


def get_yes_no_input(message):
    """
    Function to get user input for yes/no questions.

    Parameters:
    - message: The message to display to the user.

    Returns:
    - "y" for yes, "n" for no.
    """
    while True:
        user_input = input(message)
        if user_input.lower() in ["y", "n"]:
            return user_input.lower()
        print("Please enter a valid input (Y/N).")


def read_data_employee():
    """
    Function to read employee data based on user-defined filters.

    The function prompts the user to select columns and apply filters to the employee data.

    Returns:
    - Prints the tabulated results of the query.
    """
    # List of available columns
    list_columns = ['ALL', 'e_id', 'name', 'id_number', 'address', 'dob', 'phone', 'email',
                    'position', 'departments', 'status', 'salary', 'hire_date',
                    'insurance_status', 'insurance_name', 'insurance_number']

    # Prompt user to choose columns to filter
    print("=" * 75)
    print(("\t" * 6) + "FILTER BASED ON")
    print("=" * 75)
    for i, value in enumerate(list_columns):
        print(f"{i + 1}. {value}")
    print("=" * 75)

    filter_columns = []
    num_columns_to_filter = int(input("Number of columns to filter: "))

    # Get user input for columns to filter
    for _ in range(num_columns_to_filter):
        column_name = get_column_input(list_columns, filter_columns)
        filter_columns.append(column_name)

    # Get user input to add filters
    add_filter = get_yes_no_input("Do you want to add a filter? (Y/N): ")

    filter_query = []

    # Loop to add filters
    while add_filter == "y":
        column_filter = ['name', 'position', 'departments', 'insurance_name']

        print("=" * 75)
        print(("\t" * 6) + "FILTER BASED ON")
        print("=" * 75)
        for i, value in enumerate(column_filter):
            print(f"{i + 1}. {value}")
        print("=" * 75)

        filter_key = get_filter_input(column_filter)
        filter_value = input("Enter keywords: ")
        filter_query.append([filter_key, filter_value])
        add_filter = get_yes_no_input("Add more filters? (Y/N): ")

    # Build WHERE clause for the SQL query
    where_filter = [f"LOWER({key}) LIKE LOWER('%{value}%')" if key in ["name", "position"]
                    else f"LOWER({key}) = LOWER('{value}')" for key, value in filter_query]

    where_query = f"WHERE {' OR '.join(where_filter)}" if where_filter else ""

    # Construct the SQL query
    query = f"""
    SELECT 
        {", ".join(filter_columns)}
    FROM
        `voltaic-reducer-399714.inti_corpora.employee_data` AS i 
    {where_query}
    """

    # Execute the query and display the results
    results = conn_db(query)
    results_df = results.to_dataframe()
    print(tabulate(results_df, headers=results_df.keys(), tablefmt='psql', showindex=False))
