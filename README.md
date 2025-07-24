# terraform-azure-authentication-action

An action to set the Terraform environment variables to access Azure.

## Overview

This GitHub Action fetches secrets from Azure Key Vault and sets them as environment variables required for Terraform to authenticate with Azure. It supports both local development and GitHub Actions workflows.

## Features

- Fetch secrets from Azure Key Vault using service principal credentials.
- Set secrets as environment variables for Terraform.
- Integrate with GitHub Actions by writing secrets to the `GITHUB_ENV` file.

## Prerequisites

- Python 3.11
- Azure subscription with a Key Vault and registered secrets.
- Service principal credentials (`AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`) set in a `.env` file.
- `config.toml` file specifying Key Vault name and secret names.
- poetry to manage dependencies. use `poetry install` to install dependencies.
- ### run the code as **poetry run python3 fetch_kv_secret.py** to execute the script.

