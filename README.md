# API Data Extraction and Transformation

This project retrieves sample customer records from the JSONPlaceholder users
API, inspects and transforms the response, and exports a flattened CSV file.

## Approach

The workflow in `starter.py` is:

1. Fetch the user list from `https://jsonplaceholder.typicode.com/users` with a
   10-second request timeout.
2. Report the top-level, record, and nested value types in the first record.
3. Extract a smaller set of core fields (ID, name, email, city, and company),
   and build example name, `(id, email)`, and `id-to-city` Python structures.
4. Recursively flatten nested user records, joining nested keys with
   underscores (for example, `address_geo_lat`).
5. Build a pandas DataFrame, rename `id` to `customer_id`, convert latitude
   and longitude to numeric values, and arrange the output columns in the
   expected order.
6. Create the output directory if necessary and write the DataFrame to CSV.

The smaller core-field records and example Python structures demonstrate the
assignment transformations; the exported CSV contains the flattened full user
records.

## Requirements

- Python 3
- Internet access to reach the JSONPlaceholder API
- Packages listed in `requirements.txt` (`requests` and `pandas`)

## Run

From the project directory, create and activate a virtual environment in
PowerShell, then install the dependencies:

```powershell
py -m venv myenv
.\myenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the extraction using either entry point:

```powershell
python extract_customers.py
```

or:

```powershell
python starter.py
```

The script prints progress, a summary of the DataFrame, and the CSV path. It
exits with an error message if the request fails, times out, returns an
unsuccessful HTTP status, or contains invalid JSON.

## Output

The generated file is `output/customers_clean.csv`, relative to the current
working directory. The output has one row per user and these columns, in order:

`customer_id`, `name`, `username`, `email`, `phone`, `website`,
`address_street`, `address_suite`, `address_city`, `address_zipcode`,
`address_geo_lat`, `address_geo_lng`, `company_name`,
`company_catchPhrase`, `company_bs`

Running the script again overwrites this CSV.

## Assumptions

- The API returns a JSON array of user objects, with nested `address`,
  `address.geo`, and `company` objects in the shape used by JSONPlaceholder.
- The API is available over the network when the script runs; there is no
  local input-data fallback.
- The output path is relative to the directory from which the script is
  launched.
- The output schema is fixed to the listed columns. If a source field is
  absent, its corresponding DataFrame cell is empty; additional response fields
  are not included in the exported CSV.