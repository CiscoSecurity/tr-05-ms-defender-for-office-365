import json

from pydantic import BaseModel


class Settings(BaseModel):
    SETTINGS: dict = json.load(open("container_settings.json", "r"))
    VERSION: str = SETTINGS["VERSION"]
    CTR_DEFAULT_ENTITIES_LIMIT: int = 100
    CTIM_SCHEMA_VERSION: str = "1.3.13"
    CTR_HEADERS: dict = {"User-Agent": "Cisco-XDR MicrosoftDefenderForOffice365/1.0.0"}

    API_HOST: str = "https://api.security.microsoft.com"
    BASE_URL: str = f"{API_HOST}/api"
    ADVANCED_HUNTING_URL: str = f"{BASE_URL}/advancedhunting/run"
    SCOPE: str = f"{API_HOST}/.default"

    OBSERVABLE_TYPES: dict = {
        "sha1": "SHA1",
        "sha256": "SHA256",
        "ip": "IP",
        "ms_machine_id": "ms_machine_id",
        "hostname": "hostname",
    }

    RESPOND_TYPES: dict = {
        "sha1": "FileSha1",
        "sha256": "FileSha256",
        "ip": "IpAddress",
        "ms_machine_id": "ms_machine_id",
        "hostname": "hostname",
    }

    # Token data
    HEADER: dict = {"kid": "02B1174234C29F8EFB69911438F597FF3FFEE6B7"}
    JWK_HOST: str = "yb2olpbxka.execute-api.us-east-1.amazonaws.com/dev"
    PRIVATE_KEY: str = open("api/key.pak", "r").read()
    TENANT: str = "f131e32e-2532-4e5f-80fc-f9cd8fcaea27"
    TOKEN_URL: str = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"
