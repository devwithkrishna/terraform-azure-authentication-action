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

    return secrets

def set_github_env_variables(secrets):
	"""
    Sets GitHub environment variables using workflow commands.

    This function takes a dictionary of secrets, sanitizes the keys to make them
    compatible with GitHub environment variable naming conventions, and writes
    them to the `GITHUB_ENV` file to be used as environment variables in a GitHub
    Actions workflow.

    Args:
        secrets (dict): A dictionary where keys are secret names and values are
                        the corresponding secret values.

    Raises:
        FileNotFoundError: If the `GITHUB_ENV` file is not found.
    """
	logger = logging.getLogger(__name__)
	github_env_file = os.getenv('GITHUB_ENV')

	# Mask values in GitHub logs
	print(f"::add-mask::{secrets['ARM_TENANT_ID']}")
	print(f"::add-mask::{secrets['ARM_CLIENT_ID']}")
	print(f"::add-mask::{secrets['ARM_CLIENT_SECRET']}")

	with open(github_env_file, 'a') as f:
		for key, value in secrets.items():
			if value is not None:
					# Sanitize the key name to be compatible with GitHub env vars
				env_key = key.replace('-', '_').upper()
					# Use workflow command to set environment variable
				f.write(f"{env_key}={value}\n")
				logger.warning(f"Set environment variable: {env_key}")


def main():
	"""
	Main function to fetch a secret from Azure Key Vault.
	"""
	load_dotenv()
	setup_logging()
	logger = logging.getLogger(__name__)
	logger.info("Starting to fetch secrets from Azure Key Vault")
	secrets = fetch_kv_secret()
	set_github_env_variables(secrets)
	logger.info("Finished fetching secrets from Azure Key Vault")

if __name__ == "__main__":
	main()