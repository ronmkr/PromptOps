import json
import os
import sys
from typing import Any

from ..config import Colors, StoragePaths


class Vault:
    """Manages secure API keys in the vault."""

    @staticmethod
    def set_key(provider: str, key: str) -> bool:
        """Securely stores an API key for a provider."""
        from ..config import USER_CONFIG_DIR

        os.makedirs(USER_CONFIG_DIR, exist_ok=True)
        vault_data = {}
        if os.path.exists(StoragePaths.VAULT_FILE):
            with open(StoragePaths.VAULT_FILE) as f_vault:
                try:
                    vault_data = json.load(f_vault)
                except json.JSONDecodeError:
                    pass

        vault_data[provider] = key
        with open(StoragePaths.VAULT_FILE, "w") as f_vault:
            json.dump(vault_data, f_vault)
        return True

    @staticmethod
    def get_key(provider: str) -> str | None:
        """Retrieves an API key for a provider."""
        if not os.path.exists(StoragePaths.VAULT_FILE):
            return None

        with open(StoragePaths.VAULT_FILE) as f_vault:
            try:
                vault_data = json.load(f_vault)
                return vault_data.get(provider)
            except json.JSONDecodeError:
                return None

    @staticmethod
    def list_keys() -> list[str]:
        """Lists providers with keys in the vault."""
        if not os.path.exists(StoragePaths.VAULT_FILE):
            return []
        with open(StoragePaths.VAULT_FILE) as f_vault:
            try:
                vault_data = json.load(f_vault)
                return list(vault_data.keys())
            except json.JSONDecodeError:
                return []

    @staticmethod
    def delete_key(provider: str) -> bool:
        """Removes a provider's key from the vault."""
        if not os.path.exists(StoragePaths.VAULT_FILE):
            return False

        with open(StoragePaths.VAULT_FILE) as f_vault:
            try:
                vault_data = json.load(f_vault)
            except json.JSONDecodeError:
                return False

        if provider in vault_data:
            del vault_data[provider]
            with open(StoragePaths.VAULT_FILE, "w") as f_vault:
                json.dump(vault_data, f_vault)
            return True
        return False


class LLMProvider:
    """Abstracts LLM provider interactions."""

    @staticmethod
    def get_client_and_model() -> tuple[Any, str | None]:
        """Returns an OpenAI-compatible client and target model ID."""
        try:
            from openai import OpenAI
        except ImportError:
            return None, None

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = Vault.get_key("openai")

        base_url = os.getenv("OPENAI_BASE_URL")
        model_id = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

        # Fallback to Gemini
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            gemini_api_key = Vault.get_key("gemini")

        if not api_key and gemini_api_key:
            api_key = gemini_api_key
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            model_id = os.getenv("OPENAI_MODEL_NAME", "gemini-2.0-flash")

        if not api_key:
            return None, None

        client = OpenAI(api_key=api_key, base_url=base_url)
        return client, model_id

    @staticmethod
    def execute(
        prompt: str, system_prompt: str | None = None, model_override: str | None = None
    ) -> str | None:
        """Executes a prompt and returns the string response."""
        client, model_id = LLMProvider.get_client_and_model()
        if not client:
            return None

        target_model = model_override or model_id

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(
                model=target_model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"{Colors.RED}Error calling LLM: {e}{Colors.RESET}", file=sys.stderr)
            return None
