**API DATA EXTRACTION AND TRANSFORMATION PROJECT OVERVIEW**

This project aims to retrieve sample customer records from the JSONPlaceholder users API, inspects and transforms the response, and exports a flattened CSV file.

**Approach and Workflow**

The workflow in starter.py is:

1. Fetch the user list from https://jsonplaceholder.typicode.com/users with a 10-second request timeout.
2. Report the top-level, record, and nested value types in the first record.
3. Extract a smaller set of core fields (ID, name, email, city, and company), and build example name, (id, email), and id-to-city Python structures.
4. Recursively flatten nested user records, joining nested keys with underscores (for example, address_geo_lat).
5. Build a pandas DataFrame, rename id to customer_id, convert latitude and longitude to numeric values, and arrange the output columns in the expected order.
6. Create the output directory if necessary and write the DataFrame to CSV.
   
The core-field extraction and python data structures demonstrate the required transformations.

The final CSV contains the flattened full user records.

**Requirements**

1. Python 3
2. Internet access to reach the JSONPlaceholder API
3. Packages listed in requirements.txt (requests and pandas)
   
**Setup and Execution/Run**


From the project directory, create and activate a virtual environment in powershell, then install the dependencies.

**Create a virtual environment**

py -m venv 'name of your environmnent

**Activate the virtual environment**

.\nameofyourenvironment\Scripts\Activate.ps1

**Install dependencies**

python -m pip install -r requirements.txt

**Run the extraction pipeline**

python extract_customers.py 

Alternatively run,

python starter.py

- python extract_customers.py
or python starter.py

**Output**

The generated file is output/customers_clean.csv, relative to the current working directory.
   
The output has one row per user and these columns, in order:

**customer_id, name, username, email, phone,website, address_street,address_suite, address_city,address_zipcode,address_geo_lat, address_geo_lng, company_name, company_catchPhrase, company_bs**

**Assumptions**

The API returns a JSON array of user objects, with nested address, address_geo, and company objects in the shape used by JSONplaceholder.

1. The API is available over the network when the script runs ; there is no local input-data fallback.
2. The output path is relative to the current directory from which the script is launched.
3. The output schema is fixed to the 15 required columns.
