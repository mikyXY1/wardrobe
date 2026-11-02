"""Domain validation for Wardrobe JSON data and item input."""

from typing import Any, Dict, List, Set


class DataValidationError(ValueError):
    """Raised when Wardrobe data does not match the specified schema."""


CATEGORY_FIELDS = {"id", "name"}
ITEM_REQUIRED_FIELDS = {
    "id",
    "name",
    "category_id",
    "color",
    "size",
    "season",
    "condition",
}
ITEM_FIELDS = ITEM_REQUIRED_FIELDS | {"notes"}
SEASONS = {"spring", "summer", "autumn", "winter", "all"}
CONDITIONS = {"new", "good", "worn", "damaged"}


def _validate_keys(
    record: Any,
    required_fields: Set[str],
    allowed_fields: Set[str],
    description: str,
) -> Dict[str, Any]:
    if not isinstance(record, dict):
        raise DataValidationError("{} musí být JSON objekt.".format(description))

    missing_fields = required_fields - set(record)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise DataValidationError(
            "{} neobsahuje povinná pole: {}.".format(description, missing)
        )

    unknown_fields = set(record) - allowed_fields
    if unknown_fields:
        unknown = ", ".join(sorted(unknown_fields))
        raise DataValidationError(
            "{} obsahuje nepovolená pole: {}.".format(description, unknown)
        )

    return record


def _validate_non_empty_string(value: Any, field: str, description: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DataValidationError(
            "Pole '{}' v {} musí být neprázdný řetězec.".format(field, description)
        )
    return value


def validate_categories(data: Any) -> List[Dict[str, str]]:
    """Validate the complete category array and return it unchanged."""
    if not isinstance(data, list):
        raise DataValidationError("Soubor kategorií musí obsahovat JSON pole.")
    if not data:
        raise DataValidationError("Soubor kategorií musí obsahovat alespoň jednu kategorii.")

    seen_ids = set()
    for index, value in enumerate(data):
        description = "Kategorie na pozici {}".format(index)
        record = _validate_keys(value, CATEGORY_FIELDS, CATEGORY_FIELDS, description)
        category_id = _validate_non_empty_string(record["id"], "id", description)
        _validate_non_empty_string(record["name"], "name", description)
        if category_id in seen_ids:
            raise DataValidationError(
                "ID kategorie '{}' se v souboru opakuje.".format(category_id)
            )
        seen_ids.add(category_id)

    return data


def validate_items(data: Any, categories: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Validate the complete item array against its categories."""
    if not isinstance(data, list):
        raise DataValidationError("Soubor položek musí obsahovat JSON pole.")

    category_ids = {category["id"] for category in categories}
    seen_ids = set()

    for index, value in enumerate(data):
        description = "Položka na pozici {}".format(index)
        record = _validate_keys(
            value, ITEM_REQUIRED_FIELDS, ITEM_FIELDS, description
        )

        for field in ITEM_REQUIRED_FIELDS:
            item_value = _validate_non_empty_string(record[field], field, description)
            if field == "id":
                if item_value in seen_ids:
                    raise DataValidationError(
                        "ID položky '{}' se v souboru opakuje.".format(item_value)
                    )
                seen_ids.add(item_value)

        if record["category_id"] not in category_ids:
            raise DataValidationError(
                "Položka odkazuje na neexistující kategorii '{}'.".format(
                    record["category_id"]
                )
            )
        if record["season"] not in SEASONS:
            raise DataValidationError(
                "Položka obsahuje nepovolenou sezónu '{}'.".format(record["season"])
            )
        if record["condition"] not in CONDITIONS:
            raise DataValidationError(
                "Položka obsahuje nepovolený stav '{}'.".format(record["condition"])
            )
        if "notes" in record and not isinstance(record["notes"], str):
            raise DataValidationError(
                "Volitelné pole 'notes' v {} musí být řetězec.".format(description)
            )

    return data