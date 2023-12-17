from tabulate import tabulate
import re
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from connect_db import conn_db

class create_data():
    def identity(self, name_input, nik_input, adress_input, dob_input, phone_input, email_input):
        # Function to create identity data
        self.name = name_input
        self.nik = nik_input
        self.adress = adress_input
        self.dob = dob_input
        self.phone = phone_input
        self.email = email_input
        return [self.name, self.nik, adress_input, dob_input, phone_input, email_input]

    def job(self, position_input, departments_input, status_input, salary_input, hire_date_input):
        # Function to create job-related data
        self.position = position_input
        self.departments = departments_input
        self.status = status_input
        self.salary = salary_input
        self.hire_date = hire_date_input
        return [position_input, departments_input, status_input, salary_input, hire_date_input]

    def insurance(self, status_input, insurance_name_input, insurance_number_input):
        # Function to create insurance-related data
        self.status = status_input
        self.insurance_name = insurance_name_input
        self.insurance_number = insurance_number_input
        return [status_input, insurance_name_input, insurance_number_input]

def get_input(section, auto):
    """
    Function to get user input for various sections (identity, job, insurance).

    Parameters:
    - section: The section for which user input is required.
    - auto: A boolean flag indicating whether to use default/auto values.

    Returns:
    - Dictionary containing user input data for the specified section.
    """
    if section == "identity":
        input_data = {
            "name": input("Full Name" + '\t' * 5 + ": ") if not auto else "rhamdan syahrul",
            "id_number": input("ID Number" + '\t' * 5 + ": ") if not auto else "3175052911000007",
            "address": input("Address" + '\t' * 6 + ": ") if not auto else "Jl.belly",
            "dob": input("Date of Birth (yyyy-mm-dd)\t: ") if not auto else "2000-11-29",
            "phone": input("Phone Number (8xx)" + '\t' * 3 + ": ") if not auto else "81282003717",
            "email": input("E-mail" + '\t' * 6 + ": ") if not auto else "rhamdan@gmail.com"
        }
    elif section == "job":
        input_data = {
            "position": input("Position" + '\t' * 4 + ": ") if not auto else "data analyst",
            "departments": input("Departments" + '\t' * 4 + ": ") if not auto else "IT",
            "status": input("Status" + '\t' * 5 + ": ") if not auto else "contract",
            "salary": input("Salary" + '\t' * 5 + ": ") if not auto else "2000000",
            "hire_date": input("Hire Date(yyyy-mm-dd)" + '\t' * 1 + ": ") if not auto else "2023-08-11"
        }
    elif section == "insurance":
        input_data = {
            "status": input("status" + '\t' * 4 + ": ") if not auto else "active",
            "insurance_name": input("insurance_name" + '\t' * 2 + ": ") if not auto else "ABC Insurance",
            "insurance_number": input("insurance_number" + '\t' * 1 + ": ") if not auto else "74519284"
        }
    else:
        raise ValueError("Invalid category")

    return input_data

def check_condition(data, section):
    """
    Function to check conditions for data validity based on the specified section.

    Parameters:
    - data: List containing data to be checked.
    - section: The section for which conditions are checked (identity, job, insurance).

    Returns:
    - Tuple of boolean values indicating whether data meets specified conditions.
    """
    if section == "identity":
        conditions = (
            len(str(data[1])) == 16,  # Check ID number length
            re.match(r"\d{4}-\d{2}-\d{2}", data[3]),  # Check date of birth format
            str(data[4]).startswith("8") and len(str(data[4])) == 11,  # Check phone number format
            all(isinstance(value, str) for value in [data[i] for i in [0, 2, 5]]),  # Check string types
            re.match(r"[^@]+@[^@]+\.[^@]+", data[5]),  # Check email format
        )

        try:
            int_values_check = all(isinstance(int(value), int) for value in [data[i] for i in [1, 4]])  # Check integer values
        except ValueError:
            int_values_check = False

        conditions += (int_values_check,)
    elif section == "job":
        conditions = (
            re.match(r"\d{4}-\d{2}-\d{2}", data[4]),  # Check hire date format
            all(isinstance(value, str) for value in [data[i] for i in [0, 1, 2]]),  # Check string types
        )

        try:
            int_values_check = all(isinstance(int(value), int) for value in [data[i] for i in [3]])  # Check integer values
        except ValueError:
            int_values_check = False

        conditions += (int_values_check,)
    elif section == "insurance":
        conditions = (
            all(isinstance(value, str) for value in [data[i] for i in [0, 1]]),  # Check string types
        )

        try:
            int_values_check = all(isinstance(int(value), int) for value in [data[i] for i in [2]])  # Check integer values
        except ValueError:
            int_values_check = False

        conditions += (int_values_check,)

    return conditions


def get_information(employee, section, title, auto_input):
    """
    Function to get user information for a specified section (identity, job, insurance).

    Parameters:
    - employee: An instance of the create_data class.
    - section: The section for which user input is required (identity, job, insurance).
    - title: A string indicating the title of the information being collected.
    - auto_input: A boolean flag indicating whether to use default/auto values.

    Returns:
    - A DataFrame containing user data and a list with user data for the specified section.
    """
    has_complete = False
    full_fill_identity = False

    while not has_complete:
        while not full_fill_identity:
            print("=" * 75)
            print(title)
            print("=" * 75)

            # Get user input based on the specified section
            if section == "identity":
                data_input = get_input(section, auto_input)
                data = employee.identity(*[data_input[key] for key in data_input])
                data[0] = data[0].title()  # Capitalize the name
            elif section == "job":
                data_input = get_input(section, auto_input)
                data = employee.job(*[data_input[key] for key in data_input])
            elif section == "insurance":
                data_input = get_input(section, auto_input)
                data = employee.insurance(*[data_input[key] for key in data_input])

            conditions = check_condition(data, section)  # Check conditions for data validity

            full_fill_identity = all(item != '' for item in data) and all(conditions)
            print("\nThere are still error input or blanks on the form" if not full_fill_identity else f"\n{section} Data Inputed")
        else:
            identity_column = [list(data_input.keys())]
            print(tabulate(pd.DataFrame([data], columns=identity_column), headers=data_input.keys(), tablefmt='psql',
                           showindex=False))

            print("=" * 75)
            check_data = input("Have all the fields been filled in correctly?(Y/N)")
            if check_data.lower() == "y":
                has_complete = True
            elif check_data.lower() == "n":
                full_fill_identity = False
            else:
                print("please enter the correct input !")

    return pd.DataFrame([data], columns=identity_column), data

def new_data_employee(auto_input):
    """
    Function to collect and submit new employee data.

    Parameters:
    - auto_input: A boolean flag indicating whether to use default/auto values.

    Steps:
    1. Create an instance of the create_data class.
    2. Set flags to control the loop.
    3. Loop until all data is finalized.
        a. Execute only on the first iteration:
            - Get information for each section (identity, job, insurance).
        b. Display the collected information for each section.
        c. Prompt the user to confirm data submission.
        d. If confirmed:
            - Set the flag to end the loop.
        e. If not confirmed:
            - Prompt the user to choose a section to modify.
                - Execute based on the selected section:
                    - Get updated information for the selected section.
                - If an invalid section is selected, prompt the user to select from the list.
            - Continue the loop.
        f. If an incorrect input is provided, prompt the user to enter the correct input.
    4. After finalization:
        a. Check if the employee with the provided id_number already exists.
        b. Display a message if the id_number already exists.
        c. If not, prepare values for SQL insertion.
        d. Construct the SQL INSERT query.
        e. Execute the SQL INSERT query.
    """
    # Create an instance of the create_data class
    employee = create_data()

    # Flag to control the loop
    all_finish = False

    # Flag to check if it's the first time entering the loop
    first_time = True

    # Loop until all data is finalized
    while not all_finish:
        # Execute only on the first iteration
        while first_time:
            # Get information for each section (identity, job, insurance)
            identity_df, identity_list = get_information(employee, "identity", "PERSONAL INFORMATION", auto_input)
            job_df, job_list = get_information(employee, "job", "JOB INFORMATION", auto_input)
            insurance_df, insurance_list = get_information(employee, "insurance", "INSURANCE INFORMATION", auto_input)

            # Mark that it's not the first time anymore
            first_time = False

        # Display the collected information for each section
        dataframes = [identity_df, job_df, insurance_df]
        for df in dataframes:
            print(tabulate(df, headers=df.keys(), tablefmt='psql', showindex=False))

        # Prompt user to confirm data submission
        check_final_data = input("Are you sure to send data??(Y/N)")
        if check_final_data.lower() == "y":
            all_finish = True
        elif check_final_data.lower() == "n":
            # Prompt user to choose a section to modify
            section = ['identity', 'job', 'insurance']
            print("=" * 75)
            print(("\t" * 6) + "SELECT THE SECTION THAT YOU WANT TO REPLACE")
            print("=" * 75)
            for i, value in enumerate(section):
                print(f"{i + 1}. {value}")
            print("=" * 75)

            change_section = input("Section : ")

            # Execute based on the selected section
            if change_section == 'identity':
                identity_df, identity_list = get_information(employee, "identity", "PERSONAL INFORMATION")
            elif change_section == 'job':
                job_df, job_list = get_information(employee, "job", "JOB INFORMATION")
            elif change_section == 'insurance':
                insurance_df, insurance_list = get_information(employee, "insurance", "INSURANCE INFORMATION")
            else:
                print("Select the section in the list !")
        else:
            print("please enter the correct input !")
    else:
        # Check if the employee with the provided id_number already exists
        query = f"""
            SELECT 
                id_number
            FROM
                `voltaic-reducer-399714.inti_corpora.employee_data`
            WHERE
                id_number={identity_list[1]}
        """

        results = conn_db(query)

        # Display a message if the id_number already exists
        if len(list(results)) > 0:
            print(f"id_number {identity_list[1]} sudah ada.")
        else:
            # Prepare values for SQL insertion
            identity_value = "GENERATE_UUID(), " + ", ".join([item if i in [1, 4] else f"'{item}'" for i, item in enumerate(identity_list)])
            job_value = ", ".join([item if i in [3] else f"'{item}'" for i, item in enumerate(job_list)])
            insurance_value = ", ".join([item if i in [2] else f"'{item}'" for i, item in enumerate(insurance_list)])

            # Construct the SQL INSERT query
            add_query = f"""
                INSERT INTO voltaic-reducer-399714.inti_corpora.employee_data
                    (e_id, name, id_number, address, dob, phone, email, position, departments, status, salary, hire_date, insurance_status, insurance_name, insurance_number)
                VALUES
                    ({identity_value}, {job_value}, {insurance_value})
            """

            # Execute the SQL INSERT query
            query_job = conn_db(add_query)
            print("Data has been successfully updated.")









    