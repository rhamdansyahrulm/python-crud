# Employee Data Management System (EDMS) - Python CRUD

## Overview

The Employee Data Management System (EDMS) is a Python-based project designed to facilitate the management of employee data through CRUD (Create, Read, Update, Delete) operations. This system provides a user-friendly interface for efficiently handling employee information.

## Features

1. **Create:** Add new employee data with validation checks to ensure accuracy.

2. **Read:** Retrieve and view employee information based on various filters.

3. **Update:** Modify existing employee records with an intuitive interface.

4. **Delete:** Remove employee records, ensuring data accuracy and compliance.

## Usage

### Create Employee Data

To add new employee data, follow these steps:

```python
# Example usage for creating employee identity data
name_input = input("Full Name: ")
nik_input = input("ID Number: ")
address_input = input("Address: ")
dob_input = input("Date of Birth (yyyy-mm-dd): ")
phone_input = input("Phone Number (8xx): ")
email_input = input("E-mail: ")

# Create an instance of the create_data class
employee = create_data()

# Call the identity function to create identity data
identity_data = employee.identity(name_input, nik_input, address_input, dob_input, phone_input, email_input)
```

### Read Employee Data

To retrieve and view employee information, execute the read_data_employee() function. Follow the prompts to filter and display relevant data.

```python
# Example usage for reading employee data
read_data_employee()
```

### Update Employee Data

To modify existing employee records, execute the `update_data_employee()` function. Follow the prompts to select the employee and the columns to update.

```python
# Example usage for updating employee data
update_data_employee()
```

### Delete Employee Data

To remove employee records, execute the `delete_data_employee()` function. Follow the prompts to enter the employee IDs for deletion.

```python
# Example usage for deleting employee data
delete_data_employee()
```

## Technologies Used

- `Python`: Core programming language for CRUD functionalities.
- `Google Cloud BigQuery`: Cloud-based data storage and retrieval.
- `Pandas`: Data manipulation and presentation in tabular formats.
- `Google Cloud Service Account`: Secure authentication for accessing Google Cloud services.






