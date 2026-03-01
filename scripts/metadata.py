import datetime
import re
from typing import Any
import yaml


_FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(?P<frontmatter>.*?\n)---\s*(?:\n|$)",
    re.DOTALL,
)


def _normalize_dates(obj: Any) -> Any:
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, dict):
        return {k: _normalize_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize_dates(item) for item in obj]
    return obj


def parse_metadata(md: str) -> dict:
    match = _FRONTMATTER_RE.match(md)
    if match is None:
        return {}

    raw = match.group("frontmatter")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {}

    if not isinstance(data, dict):
        return {}

    return _normalize_dates(data)
