# from datetime import datetime
# from re import search, split
#
from datetime import datetime

from api.globals import g
from config import Settings

s = Settings()


# def get_base_url(creds: dict) -> str:
#     hostname = split("(https?://)?", creds.get("api_base_url"), 1)[-1]
#     return f"https://{hostname}"
#
#
# def filter_observables(observables):
#     supported_types = Settings.OBSERVABLE_TYPES
#     observables = remove_duplicates(observables)
#     return list(
#         filter(
#             lambda obs: (
#                 obs["type"] in supported_types
#                 and obs["value"] != "0"
#                 and not obs["value"].isspace()
#             ),
#             observables,
#         )
#     )
#
#
# def is_cyrillic(token: str) -> bool:
#     return bool(search("[\u0400-\u04FF]", token))
#
#
# def iso_to_timestamp(date: datetime) -> int:
#     return int(datetime.timestamp(date) * 1000)


def timestamp_to_iso(timestamp):
    return f"{datetime.utcfromtimestamp(timestamp // 1000).isoformat()}Z"


def set_entities_limit(payload):
    default = s.CTR_DEFAULT_ENTITIES_LIMIT
    try:
        value = int(payload["CTR_ENTITIES_LIMIT"])
        s.CTR_DEFAULT_ENTITIES_LIMIT = (
            value if value in range(1, default + 1) else default
        )
    except (ValueError, TypeError, KeyError):
        s.CTR_DEFAULT_ENTITIES_LIMIT = default


def format_docs(docs):
    return {"count": len(docs), "docs": docs}


def jsonify_errors(error):
    # According to the official documentation, an error here means that the
    # corresponding TR module is in an incorrect state and needs to be reconfigured:
    # https://visibility.amp.cisco.com/help/alerts-errors-warnings.
    error["type"] = "fatal"
    error["code"] = error.pop("code").lower().replace("_", " ")

    data = {"errors": [error]}

    if g.get("sightings") and g.sightings:
        data["data"] = {"sightings": format_docs(g.sightings)}

    return {"data": data}


# def remove_duplicates(observables):
#     return [dict(t) for t in {tuple(d.items()) for d in observables}]
#
#
# def jsonify_result():
#     """Jsonify result gathered inside g to valid json response"""
#
#     result = {"data": {}}
#
#     if g.get("sightings"):
#         result["data"]["sightings"] = format_docs(g.sightings)
#
#     if g.get("indicators"):
#         result["data"]["indicators"] = format_docs(g.indicators)
#
#     if g.get("relationships"):
#         result["data"]["relationships"] = format_docs(g.relationships)
#
#     if g.get("errors"):
#         result["errors"] = g.errors
#         if not result["data"]:
#             del result["data"]
#
#     return jsonify(result)
