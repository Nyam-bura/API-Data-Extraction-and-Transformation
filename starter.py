"""
Day 1 - API Data Extraction and Transformation
Squad Python Specialization - Data Engineering

Fill in every function. Keep the signatures; you may add helpers of your own.
"""
import csv
import json
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = Path("output") / "customers_clean.csv"


def fetch_users(url: str = API_URL, timeout: float = 10.0) -> list[dict]:
    """Retrieve the list of users from the API.

    Must raise or report a clear error for: connection failures, timeouts,
    non-200 status codes and bodies that are not valid JSON.
    """

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        users = response.json()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            f"The request timed out after {timeout} seconds."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(
            f"The API returned an unsuccessful HTTP response: {exc}"
        ) from exc

    except requests.exceptions.JSONDecodeError as exc:
        raise RuntimeError(
            "The API response body is not valid JSON."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to the API: {exc}"
        ) from exc

    if not isinstance(users, list):
        raise RuntimeError("Expected the API to return a list of users.")

    return users

def describe_structure(payload) -> None:
    """Print what Python types the payload and one record are made of
    (the top-level container, a record, and each nested value)."""

    print("Payload type:", type(payload).__name__)

    if not isinstance(payload, list) or not payload:
        print("The payload is not a non-empty list.")
        return

    first_user = payload[0]
    print("First record type:", type(first_user).__name__)

    for key, value in first_user.items():
        print(f"{key}: {type(value).__name__}")

        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                print(
                    f"  {key}.{nested_key}: "
                    f"{type(nested_value).__name__}"
                )

                if isinstance(nested_value, dict):
                    for inner_key, inner_value in nested_value.items():
                        print(
                            f"    {key}.{nested_key}.{inner_key}: "
                            f"{type(inner_value).__name__}"
                        )



def extract_core_fields(users: list[dict]) -> list[dict]:
    """Return one small dict per user with id, name, email, city and company name."""
    core_users = []
    for user in users:
        address = user.get("address") or {}
        company = user.get("company") or {}
        core_user = {
             "id": user.get("id"),
             "name": user.get("name") or "",
             "email": user.get("email" or ""),
             "city": address.get("city") or "",
             "company": company.get("name") or ""
        }
        core_users.append(core_user)
    return core_users


def build_structures(users: list[dict]) -> tuple[list, list[tuple], dict]:
    """Return (list_of_names, list_of_(id, email)_tuples, dict_of_id_to_city).

    Use at least one list comprehension and one dict comprehension.
    """

    list_of_names = [user.get("name") or "" for user in users]

    list_of_id_email_tuples = [(user.get("id"), user.get("email") or "") for user in users]

    dict_of_id_to_city = {user.get("id"): (user.get("address") or {}).get( "city") or "" for user in users}

    return (list_of_names,
            list_of_id_email_tuples,
            dict_of_id_to_city
    )

def flatten_user(user: dict, parent_key: str = "", sep: str = "_") -> dict:
    """Flatten one nested user record into a single-level dict.

    e.g. a nested address -> geo -> lat becomes the key address_geo_lat.
    """
    flattened = {}
    for key, value in user.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value,dict):
            flattened.update(flatten_user(value, parent_key=new_key, sep=sep))
        else:
            flattened[new_key] = value
    return flattened

def to_dataframe(flat_users: list[dict]) -> pd.DataFrame:
    """Build a DataFrame with the columns in the expected-output order."""
    df = pd.DataFrame(flat_users)
    df = df.rename(columns={"id": "customer_id"})        #Renaming id to customer_id

    if "address_geo_lat" in df.columns:
        df["address_geo_lat"] = pd.to_numeric(df["address_geo_lat"])

    if "address_geo_lng" in df.columns:
        df["address_geo_lng"] = pd.to_numeric(df["address_geo_lng"])

    expected_order = [
        "customer_id",
        "name",
        "username",
        "email",
        "phone",
        "website",
        "address_street",
        "address_suite",
        "address_city",
        "address_zipcode",
        "address_geo_lat",
        "address_geo_lng",
        "company_name",
        "company_catchPhrase",
        "company_bs"
    ]
    df = df.reindex(columns=expected_order)
    return df

def export_csv(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> Path:
    """Write the DataFrame to CSV (creating the folder if needed) and return the path."""
    path.parent.mkdir(parents=True,exist_ok=True)

    df.to_csv(path, index=False)
    return path

def main() -> None:
    # TODO: wire the steps together and print a short run summary.
    try:
        users = fetch_users()
        print(f"Successfully fetched {len(users)} users.")

        describe_structure(users)

        core_users = extract_core_fields(users)
        print(f"Extracted core fields for {len(core_users)} users.")

        names, id_email_tuples, id_to_city = build_structures(users)
        print(f"Built structures for {len(names)} users.")

        flat_user = [flatten_user(user) for user in users]

        df = to_dataframe(flat_user)
        print("DataFrame Shape:", df.shape)
        print("\n DataFrame data types:")
        print(df.dtypes)

        output_path = export_csv(df)

        print("\nExtraction completed successfully!")
        print(f"Rows exported: {len(df)}")
        print(f"Columns exported: {len(df.columns)}")
        print(f"CSV location: {output_path}")

    except  (RuntimeError, ValueError, KeyError, OSError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1) from None

if __name__ == "__main__":
    main()
