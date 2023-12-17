import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

def conn_db(query):
    """
    Function to connect to BigQuery and execute a query.

    Parameters:
    - query: SQL query string to execute.

    Returns:
    - results: Query results from BigQuery.
    """
    # Load Google Cloud credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file("voltaic-reducer-399714-87eda49329ec.json")

    # Set the Google Cloud project ID
    project_id = "voltaic-reducer-399714"

    # Create a BigQuery client using the provided credentials and project ID
    client = bigquery.Client(credentials=credentials, project=project_id)
    
    # Execute the query using the client
    query_job = client.query(query)
    
    # Get the results of the query
    results = query_job.result()
    
    return results
