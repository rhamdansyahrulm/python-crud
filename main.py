import pandas as pd
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from create_data import new_data_employee
from read_data import read_data_employee
from delete_data import delete_data_employee
from update_data import update_data_employee

def continue_access():
    """
    Function to prompt the user if they want to continue accessing the system.

    Returns:
    - bool: True if the user wants to continue, False if they want to exit.
    """
    while True:
        user_input = input("Do you want to continue accessing the system? (Y/N): ").lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            print("Please enter 'Y' for Yes or 'N' for No.")

def get_boolean_input(message):
    while True:
        user_input = input(message + " (True/False): ").lower()
        if user_input == "true":
            return True
        elif user_input == "false":
            return False
        else:
            print("Please enter 'True' or 'False'.")

still_access = True
while still_access:
    # Menu options for CRUD operations
    crud_options = ["Create", "Read", "Update", "Delete"]
    
    print("=" * 75)
    print(("\t" * 6) + "EMPLOYEE DATA MANAGEMENT")
    print("=" * 75)

    # Display the CRUD options to the user
    for i, option in enumerate(crud_options):
        print(f"{i + 1}. {option}")
    print("=" * 75)

    # Get user input for the desired operation
    selected_option = input("Open: ")

    # Execute the corresponding function based on user input
    if selected_option.lower() == "create":
        auto_input = get_boolean_input("Do you want to use auto input for testing?") # Ask for input to use True or False as a parameter
        new_data_employee(auto_input)
        still_access = continue_access()
    elif selected_option.lower() == "read":
        read_data_employee()
        still_access = continue_access()
    elif selected_option.lower() == "update":
        update_data_employee()
        still_access = continue_access()
    elif selected_option.lower() == "delete":
        delete_data_employee()
        still_access = continue_access()
    else:
        print("Select the Correct Menu !")
        still_access = continue_access()

print("Thank you for using the Employee Data Management System.")
