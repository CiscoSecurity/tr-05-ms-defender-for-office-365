import hashlib

from code.config import Settings
from utils import timestamp_to_iso

CONFIDENCE = "High"
DESCRIPTION = ""
HOSTNAME = "hostname"
IP = "ip"
INDICATOR = "indicator"
MAC_ADDRESS = "mac_address"
MSO_ID = ""
PRODUCER = ""
SENSOR = ""
SOURCE = ""
SIGHTING = "sighting"
TARGET_TYPE = ""


class Sighting:
    """Mapping of sightings"""

    def __init__(self, observable: dict, credentials: dict):
        self.defaults = {
            "confidence": CONFIDENCE,
            "count": 1,
            "description": DESCRIPTION,
            "internal": True,
            "schema_version": Settings.CTIM_SCHEMA_VERSION,
            "sensor": SENSOR,
            "source": SOURCE,
            "type": SIGHTING,
        }
        self.api_base_url = credentials.get("api_base_url")
        self.obs_types = Settings.OBSERVABLE_TYPES
        self.observable = observable

    def _get_ext_ids(self, data) -> list:
        return [data]

    def _get_ext_refs(self, data) -> list:
        return [
            {"source_name": PRODUCER, "description": "", "external_id": "", "url": ""}
        ]

    @staticmethod
    def _get_observed_time(device):
        return {"start_time": timestamp_to_iso(device.get("creationTime"))}

    def _get_relations(self, alert: dict) -> list[dict]:
        pass

    @staticmethod
    def _get_severity(alert: dict) -> str:
        pass

    def _get_targets(self, alert: dict) -> list[dict]:
        pass

    @staticmethod
    def _get_transient_id(pid) -> str:
        # todo: switch pid to something relevant
        hashed = hashlib.sha256(
            f"{SIGHTING}|{pid}|cisco.xdr.mso365.integration".encode("UTF-8")
        )
        return f"transient:{SIGHTING}-{hashed.hexdigest()}"

    def extract(self, alert: dict) -> dict:
        """Extract sighting from the Darktrace data."""

        return {
            "external_ids": self._get_ext_ids(alert),
            "external_references": self._get_ext_refs(alert),
            "id": self._get_transient_id(alert),
            "observables": [self.observable],
            "observed_time": self._get_observed_time(alert),
            "relations": self._get_relations(alert),
            "severity": self._get_severity(alert),
            "targets": self._get_targets(alert),
            **self.defaults,
        }


class Indicator:
    """Mapping for the indicators"""

    defaults = {
        "confidence": CONFIDENCE,
        "producer": PRODUCER,
        "schema_version": Settings.CTIM_SCHEMA_VERSION,
        "type": INDICATOR,
        "valid_time": {},
    }

    @staticmethod
    def _transient_id(entity_type: str, model: dict, uuid=None) -> str:
        if uuid:
            return f"transient:{entity_type}-{uuid}"

        hashed = hashlib.sha256(
            f"{entity_type}|{model['uuid']}|"
            "cisco.xdr.mso365.integration".encode("UTF-8")
        )
        return f"transient:{entity_type}-{hashed.hexdigest()}"

    def extract(self, item: dict) -> dict:
        """Extract indicator from the Darktrace data of model."""

        # todo: update keys with appropriate ones

        model = item["model"]["then"]

        return {
            "id": self._transient_id(INDICATOR, model),
            "title": model["name"],
            **({"description": ds} if (ds := model.get("description")) else {}),
            "external_ids": [model["uuid"]],
            **self.defaults,
        }
