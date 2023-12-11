import json
import os

from pydantic import BaseModel


class Settings(BaseModel):
    settings: dict = json.load(open("container_settings.json", "r"))
    VERSION: str = settings["VERSION"]
    CTR_DEFAULT_ENTITIES_LIMIT: int = 100

    API_HOST: str = "https://api.securitycenter.windows.com"
    SCOPE_URL: str = f"{API_HOST}/.default"
    API_VERSION: str = "v1.0"

    BASE_URL: str = f"{API_HOST}/api/{API_VERSION}"
    API_URL: str = BASE_URL + "/{entity}/{value}"
    API_HEALTH_ENDPOINT: str = f"{API_HOST}/api/exposureScore"
    ADVANCED_HUNTING_URL: str = f"{BASE_URL}/advancedqueries/run"
    INDICATOR_URL: str = f"{BASE_URL}/indicators"
    DEFENDER_URL: str = "https://security.microsoft.com"

    # Token data
    HEADER: dict = {"kid": "02B1174234C29F8EFB69911438F597FF3FFEE6B7"}
    JWK_HOST: str = "yb2olpbxka.execute-api.us-east-1.amazonaws.com/dev"
    PRIVATE_KEY: str = open("api/key.pak", "r").read()

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

    CTIM_SCHEMA_VERSION: str = "1.3.13"
    CTR_HEADERS: str = {"User-Agent": "Cisco-XDR MicrosoftDefenderForOffice365/1.0.0"}

    # ------------------------------------------------------------------------------------

    SECRET_KEY: str = os.environ.get("SECRET_KEY")
