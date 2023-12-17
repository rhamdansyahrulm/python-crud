from tabulate import tabulate
import re
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from connect_db import conn_db

def delete_data_employee():
    """
    Function to delete employee data from the database based on provided employee IDs.

    The function prompts the user to enter employee ID numbers to be deleted.
    It then retrieves and displays the corresponding employee data for confirmation.
    If the user confirms, the data is deleted from the database.

    Note: This function assumes the existence of a BigQuery table named 'voltaic-reducer-399714.inti_corpora.employee_data'.
    """
    # Initialize an empty list to store employee IDs
    employee_list = []

    # Prompt the user to enter employee IDs until 'done' is entered
    while True:
        employee = input("Enter Employee ID Number (or type 'done' to finish): ")

        if employee.lower() == 'done':
            break
        else:
            employee_list.append(employee)

    # Construct a SQL query to retrieve employee data based on the entered IDs
    query = f"""
        SELECT name, id_number, address, position, departments
        FROM voltaic-reducer-399714.inti_corpora.employee_data
        WHERE id_number IN ({", ".join(employee_list)})
    """

    # Execute the query and retrieve the results
    results = conn_db(query)
    results_df = results.to_dataframe()

    # Check if any data is found for the provided employee IDs
    if results_df.shape[0] == 0:
        print("No data found for the provided employee IDs.")
    else:
        # Display the retrieved data for user confirmation
        print(tabulate(results_df, headers=results_df.keys(), tablefmt='psql', showindex=False))

        # Ask the user if the displayed data is correct
        answer = input("Is the displayed data correct? (Y/N): ")

        if answer.lower() == 'n':
            # If the data is incorrect, prompt the user to re-enter employee IDs
            employee_list = []
            while True:
                new_employee = input("Re-enter Employee ID Number (or type 'done' to finish): ")
                if new_employee.lower() == 'done':
                    break
                else:
                    employee_list.append(new_employee)

        if answer.lower() == 'y':
            # Execute a delete query based on the confirmed employee IDs
            delete_query = f"""
                DELETE FROM voltaic-reducer-399714.inti_corpora.employee_data
                WHERE id_number IN ({", ".join(employee_list)})
            """
            conn_db(delete_query)
            print("Data has been deleted.")
