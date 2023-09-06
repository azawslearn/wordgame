from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize Azure credentials
credential = DefaultAzureCredential()

# Initialize the SecretClient
secret_client = SecretClient(vault_url="https://<YourVaultName>.vault.azure.net/", credential=credential)

# Retrieve secrets from Azure Key Vault
DB_USERNAME = secret_client.get_secret("DB_USERNAME").value
DB_PASSWORD = secret_client.get_secret("DB_PASSWORD").value
DB_HOST = secret_client.get_secret("DB_HOST").value or 'default_value_if_not_set'
DB_NAME = secret_client.get_secret("DB_NAME").value
