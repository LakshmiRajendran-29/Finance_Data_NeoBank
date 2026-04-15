# Databricks notebook source
# =====================================================
# 1 Define Connection Variables (EDIT THESE)
# =====================================================

sqlserver_host = "nameofsqlserver.database.windows.net"
sqlserver_port = "1433"
sqlserver_database = "sqlserver_database_name"
sqlserver_user = "sqlserver_user_name"
sqlserver_password = "sqlserver_password"

# Secret scope / keys

# Secret scope name (will be created if not exists)
secret_scope_name = "banking-scope"

# Secret key name (single secret containing full JSON)
sql_secret_key_name = "sqlserver-connection-json"

gmail_secret_key_name = "gmail_api_key"

# JDBC driver
sqlserver_driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

put_secret(
    scope_name="banking-scope",
    key_name="gmail_api_key",
    secret_value="*** ***** **** ***"
)

gmail_api_key = dbutils.secrets.get(
    scope="banking-scope",
    key="gmail_api_key"
)


# COMMAND ----------

# =====================================================
# 2️⃣ Build JSON Object
# =====================================================

import json

connection_config = {
    "host": sqlserver_host,
    "port": sqlserver_port,
    "database": sqlserver_database,
    "user": sqlserver_user,
    "password": sqlserver_password,
    "driver": sqlserver_driver
}

connection_json = json.dumps(connection_config)

print("Generated JSON Configuration:")
print(connection_json)

# =====================================================
# 3. GET DATABRICKS WORKSPACE CONTEXT
# =====================================================

# Python cell in the same workspace notebook
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()

api_url  = ctx.apiUrl().getOrElse(None)     
# e.g. https://adb-...azuredatabricks.net
api_token = ctx.apiToken().getOrElse(None)  

if not api_url or not api_token:
    raise ValueError("Unable to retrieve Databricks API URL or session token.")

DATABRICKS_INSTANCE = api_url
DATABRICKS_TOKEN = api_token

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

print("Databricks workspace context retrieved successfully.")

print(api_url)
print(api_token)  # handle securely, do not log in real code

# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

def create_secret_scope_if_not_exists(scope_name: str) -> None:
    existing_scopes = [s.name for s in dbutils.secrets.listScopes()]

    if scope_name in existing_scopes:
        print(f"Secret scope '{scope_name}' already exists.")
        return

    url = f"{DATABRICKS_INSTANCE}/api/2.0/secrets/scopes/create"
    payload = {"scope": scope_name}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print(f"Secret scope '{scope_name}' created successfully.")
    else:
        raise Exception(
            f"Failed to create secret scope '{scope_name}'. "
            f"Status: {response.status_code}, Response: {response.text}"
        )


def put_secret(scope_name: str, key_name: str, secret_value: str) -> None:
    url = f"{DATABRICKS_INSTANCE}/api/2.0/secrets/put"
    payload = {
        "scope": scope_name,
        "key": key_name,
        "string_value": secret_value
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print(f"Secret '{key_name}' stored successfully in scope '{scope_name}'.")
    else:
        raise Exception(
            f"Failed to store secret '{key_name}'. "
            f"Status: {response.status_code}, Response: {response.text}"
        )


def verify_secret(scope_name: str, key_name: str) -> None:
    try:
        secret_value = dbutils.secrets.get(scope=scope_name, key=key_name)
        print(f"Secret '{key_name}' retrieved successfully from scope '{scope_name}'.")

        if key_name == sql_secret_key_name:
            parsed = json.loads(secret_value)
            print("Parsed SQL Server secret successfully.")
    except Exception as e:
        raise Exception(f"Secret verification failed for '{key_name}': {str(e)}")


# =====================================================
# 5. CREATE SECRET SCOPE IF NOT EXISTS
# =====================================================

create_secret_scope_if_not_exists(secret_scope_name)

# =====================================================
# 6. STORE SQL SERVER CONNECTION SECRET
# =====================================================

put_secret(
    scope_name=secret_scope_name,
    key_name=sql_secret_key_name,
    secret_value=connection_json
)

# =====================================================
# 7. VERIFY SQL SERVER SECRET
# =====================================================

verify_secret(
    scope_name=secret_scope_name,
    key_name=sql_secret_key_name
)

# Read SQL Server secret

secret_json = dbutils.secrets.get(
    scope="banking-scope",
    key="sqlserver-connection-json"
)

config = json.loads(secret_json)
print(config["host"])

gmail_api_key = dbutils.secrets.get(
    scope="banking-scope",
    key="gmail_api_key"
)

# ----------------------------------------
# API Endpoint
# ----------------------------------------
url = f"{DATABRICKS_INSTANCE}/api/2.0/secrets/scopes/create"

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "scope": scope_name
}

# ----------------------------------------
# Send request
# ----------------------------------------
response = requests.post(url, headers=headers, data=json.dumps(payload))

# ----------------------------------------
# Handle response
# ----------------------------------------
# if response.status_code == 200:
#     print(f"Secret scope '{scope_name}' created successfully.")
# else:
#     print("Failed to create secret scope.")
#     print("Status Code:", response.status_code)
#     print("Response:", response.text)


existing_scopes = [s.name for s in dbutils.secrets.listScopes()]

if scope_name not in existing_scopes:
    response = requests.post(
        f"{DATABRICKS_INSTANCE}/api/2.0/secrets/scopes/create",
        headers={
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "scope": scope_name,
            "scope_backend_type": backend_type
        })
    )

    if response.status_code == 200:
        print(f"Secret scope '{scope_name}' created successfully.")
    else:
        print("Failed to create secret scope.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

else:
    print(f"Secret scope '{scope_name}' already exists.")
# COMMAND ----------

import requests
import json

scope = secret_scope_name          # Already existing scope
secret_key = secret_key_name       # Name of the secret entry
secret_value = connection_json # Value to store securely

# -------------------------------------------------
# API Endpoint
# -------------------------------------------------
url = f"{DATABRICKS_INSTANCE}/api/2.0/secrets/put"

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "scope": scope,
    "key": secret_key,
    "string_value": secret_value
}

# -------------------------------------------------
# Send Request
# -------------------------------------------------
response = requests.post(url, headers=headers, data=json.dumps(payload))

# -------------------------------------------------
# Output
# -------------------------------------------------
if response.status_code == 200:
    print(f"Secret '{secret_key}' created successfully in scope '{scope}'.")
else:
    print("Failed to create secret.")
    print("Status:", response.status_code)
    print("Response:", response.text)

