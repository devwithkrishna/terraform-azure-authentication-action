import os
import logging
import toml
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
from setup_logging import setup_logging


def fetch_kv_secret():
    """
    Fetches secrets from an Azure Key Vault and sets them as environment variables.

    This function reads the Key Vault name and secret names from a `config.toml` file,
    retrieves the secrets from the Key Vault using Azure SDK, and stores them in the
    environment variables for further use.

    Raises:
        KeyError: If the `config.toml` file does not contain the required keys.
        azure.core.exceptions.HttpResponseError: If there is an issue with the Azure Key Vault request.
    """
    # Initialize a logger for logging information and errors
    logger = logging.getLogger(__name__)

    # Authenticate using the default Azure credential chain
    credential = DefaultAzureCredential()

    # Load configuration from the `config.toml` file
    config = toml.load("config.toml")

    # Retrieve the Key Vault name from the configuration
    keyvault = keyvault_name = config["keyvault"]["name"]

    # Construct the Key Vault URL
    vault_url = f"https://{keyvault_name}.vault.azure.net/"

    # Retrieve the secret names from the configuration
    secret_names = config["secrets"]

    # Create a SecretClient to interact with the Azure Key Vault
    client = SecretClient(vault_url=vault_url, credential=credential)

    # Dictionary to store the retrieved secrets
    secrets = {}

    # Iterate over the secret names and fetch their values from the Key Vault
    for key, secret in secret_names.items():
        secret_name = secret
        # Retrieve the secret value from the Key Vault
        get_secret = client.get_secret(secret_name)
        # Store the secret value in the dictionary
        secrets[key] = get_secret.value
        # Set the secret value as an environment variable
        os.environ[key] = get_secret.value


def main():
	"""
	Main function to fetch a secret from Azure Key Vault.
	"""
	load_dotenv()
	setup_logging()
	logger = logging.getLogger(__name__)
	logger.info("Starting to fetch secrets from Azure Key Vault")
	fetch_kv_secret()
	logger.info("Finished fetching secrets from Azure Key Vault")

if __name__ == "__main__":
	main()