"""UTF-8 JSON persistence for Wardrobe categories and items."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .validation import DataValidationError, validate_categories, validate_items


DEFAULT_CATEGORIES = (
    {"id": "tops", "name": "Trička a topy"},
    {"id": "blouses", "name": "Halenky"},
    {"id": "shirts", "name": "Košile"},
    {"id": "sweaters", "name": "Svetry a kardigany"},
    {"id": "dresses", "name": "Šaty"},
    {"id": "skirts", "name": "Sukně"},
    {"id": "trousers", "name": "Kalhoty"},
    {"id": "jeans", "name": "Džíny"},
    {"id": "jackets", "name": "Bundy a saka"},
    {"id": "coats", "name": "Kabáty"},
)


class StorageError(OSError):
    """Raised when a Wardrobe data file cannot be read or written."""


class DuplicateJsonKeyError(ValueError):
    """Raised when a JSON object contains the same key more than once."""


def _unique_object(pairs: List[Any]) -> Dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(
                "JSON objekt obsahuje duplicitní klíč '{}'".format(key)
            )
        result[key] = value
    return result


class JsonStorage:
    """Read and write the project's categories.json and items.json files."""

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        if data_dir is None:
            project_root = Path(__file__).resolve().parents[2]
            data_dir = project_root / "data"
        self.data_dir = Path(data_dir)
        self.categories_path = self.data_dir / "categories.json"
        self.items_path = self.data_dir / "items.json"

    def initialize(self) -> None:
        """Create missing storage paths and files without replacing existing data."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise StorageError(
                "Nelze vytvořit datový adresář '{}': {}".format(
                    self.data_dir, error
                )
            ) from error

        self._create_json_if_missing(self.categories_path, list(DEFAULT_CATEGORIES))
        self._create_json_if_missing(self.items_path, [])

    def load_categories(self) -> List[Dict[str, str]]:
        """Load and validate every category from categories.json."""
        self.initialize()
        data = self._read_json(self.categories_path)
        try:
            return validate_categories(data)
        except DataValidationError as error:
            raise DataValidationError(
                "Neplatný soubor '{}': {}".format(self.categories_path, error)
            ) from error

    def load_items(self) -> List[Dict[str, Any]]:
        """Load and validate every item against the category file."""
        categories = self.load_categories()
        data = self._read_json(self.items_path)
        try:
            return validate_items(data, categories)
        except DataValidationError as error:
            raise DataValidationError(
                "Neplatný soubor '{}': {}".format(self.items_path, error)
            ) from error

    def save_items(self, items: Sequence[Dict[str, Any]]) -> None:
        """Save items without removing or changing any previously stored item."""
        categories = self.load_categories()
        existing_data = self._read_json(self.items_path)
        try:
            existing_items = validate_items(existing_data, categories)
        except DataValidationError as error:
            raise DataValidationError(
                "Neplatný soubor '{}': {}".format(self.items_path, error)
            ) from error

        try:
            validated_items = validate_items(list(items), categories)
        except DataValidationError as error:
            raise DataValidationError("Nelze uložit položky: {}".format(error)) from error

        items_by_id = {item["id"]: item for item in validated_items}
        for existing_item in existing_items:
            if items_by_id.get(existing_item["id"]) != existing_item:
                raise DataValidationError(
                    "Uložení nesmí odstranit ani změnit existující položku '{}'.".format(
                        existing_item["id"]
                    )
                )

        self._write_items_atomically(validated_items)

    def _create_json_if_missing(self, path: Path, initial_data: Any) -> None:
        created = False
        try:
            with path.open("x", encoding="utf-8") as json_file:
                created = True
                json.dump(initial_data, json_file, ensure_ascii=False, indent=2)
                json_file.write("\n")
        except FileExistsError:
            return
        except OSError as error:
            if created:
                try:
                    path.unlink()
                except OSError:
                    pass
            raise StorageError(
                "Nelze vytvořit soubor '{}': {}".format(path, error)
            ) from error

    def _read_json(self, path: Path) -> Any:
        try:
            with path.open("r", encoding="utf-8") as json_file:
                return json.load(json_file, object_pairs_hook=_unique_object)
        except DuplicateJsonKeyError as error:
            raise DataValidationError(
                "Neplatný JSON v souboru '{}': {}.".format(path, error)
            ) from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise DataValidationError(
                "Soubor '{}' neobsahuje platný UTF-8 JSON: {}".format(path, error)
            ) from error
        except OSError as error:
            raise StorageError(
                "Nelze načíst soubor '{}': {}".format(path, error)
            ) from error

    def _write_items_atomically(self, items: List[Dict[str, Any]]) -> None:
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(self.data_dir),
                prefix=".items-",
                suffix=".tmp",
                delete=False,
            ) as json_file:
                temporary_path = Path(json_file.name)
                json.dump(items, json_file, ensure_ascii=False, indent=2)
                json_file.write("\n")
                json_file.flush()
                os.fsync(json_file.fileno())
            os.replace(str(temporary_path), str(self.items_path))
            temporary_path = None
        except OSError as error:
            raise StorageError(
                "Nelze bezpečně uložit soubor '{}': {}".format(
                    self.items_path, error
                )
            ) from error
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except OSError:
                    pass