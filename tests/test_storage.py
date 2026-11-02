import json
import os
from pathlib import Path

import pytest

from src.wardrobe.storage import JsonStorage, StorageError
from src.wardrobe.validation import DataValidationError


def valid_item(item_id="item-001", name="Zimní kabát"):
    return {
        "id": item_id,
        "name": name,
        "category_id": "coats",
        "color": "šedá",
        "size": "40",
        "season": "winter",
        "condition": "good",
        "notes": "Teplý kabát",
    }


def test_initialize_creates_directory_and_expected_files(tmp_path):
    data_dir = tmp_path / "nested" / "data"
    storage = JsonStorage(data_dir)

    storage.initialize()

    assert data_dir.is_dir()
    categories = json.loads(storage.categories_path.read_text(encoding="utf-8"))
    items = json.loads(storage.items_path.read_text(encoding="utf-8"))
    assert [category["id"] for category in categories] == [
        "tops",
        "blouses",
        "shirts",
        "sweaters",
        "dresses",
        "skirts",
        "trousers",
        "jeans",
        "jackets",
        "coats",
    ]
    assert items == []


def test_initialize_preserves_existing_files(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    categories_path = data_dir / "categories.json"
    items_path = data_dir / "items.json"
    categories_content = '[{"id":"custom","name":"Moje kategorie"}]\n'
    items_content = "[]\n"
    categories_path.write_text(categories_content, encoding="utf-8")
    items_path.write_text(items_content, encoding="utf-8")

    JsonStorage(data_dir).initialize()

    assert categories_path.read_text(encoding="utf-8") == categories_content
    assert items_path.read_text(encoding="utf-8") == items_content


def test_loads_existing_valid_json_files(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    categories_path = data_dir / "categories.json"
    items_path = data_dir / "items.json"
    categories = [{"id": "coats", "name": "Kabáty"}]
    items = [valid_item()]
    categories_path.write_text(
        json.dumps(categories, ensure_ascii=False), encoding="utf-8"
    )
    items_path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")

    loaded_items = JsonStorage(data_dir).load_items()

    assert loaded_items == items


def test_loading_missing_items_file_creates_and_returns_empty_list(tmp_path):
    storage = JsonStorage(tmp_path / "data")

    loaded_items = storage.load_items()

    assert loaded_items == []
    assert json.loads(storage.items_path.read_text(encoding="utf-8")) == []


def test_load_and_save_items_preserves_czech_text(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    item = valid_item()

    storage.save_items([item])

    contents = storage.items_path.read_text(encoding="utf-8")
    assert "šedá" in contents
    assert storage.load_items() == [item]


def test_load_items_accepts_missing_optional_notes(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    item = valid_item()
    del item["notes"]
    storage.save_items([item])

    assert storage.load_items() == [item]


def test_load_categories_rejects_empty_existing_array_without_replacing_it(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    storage.initialize()
    storage.categories_path.write_text("[]\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="alespoň jednu kategorii"):
        storage.load_categories()

    assert storage.categories_path.read_text(encoding="utf-8") == "[]\n"


@pytest.mark.parametrize(
    "contents",
    [
        "{invalid json",
        '[{"id":"tops","id":"duplicate","name":"Topy"}]',
        '[{"id":"tops","name":"Topy","extra":"value"}]',
    ],
)
def test_load_categories_rejects_invalid_json_and_schema(tmp_path, contents):
    storage = JsonStorage(tmp_path / "data")
    storage.initialize()
    storage.categories_path.write_text(contents, encoding="utf-8")

    with pytest.raises(DataValidationError):
        storage.load_categories()


@pytest.mark.parametrize(
    "mutate_item",
    [
        lambda item: item.update(season="monsoon"),
        lambda item: item.update(category_id="unknown"),
        lambda item: item.update(extra="unexpected"),
        lambda item: item.update(color=42),
    ],
)
def test_save_items_rejects_invalid_records_without_replacing_data(
    tmp_path, mutate_item
):
    storage = JsonStorage(tmp_path / "data")
    existing_item = valid_item()
    storage.save_items([existing_item])
    original_contents = storage.items_path.read_text(encoding="utf-8")
    invalid_item = valid_item(item_id="item-002")
    mutate_item(invalid_item)

    with pytest.raises(DataValidationError):
        storage.save_items([existing_item, invalid_item])

    assert storage.items_path.read_text(encoding="utf-8") == original_contents


def test_save_items_cannot_remove_or_change_existing_items(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    existing_item = valid_item()
    storage.save_items([existing_item])
    original_contents = storage.items_path.read_text(encoding="utf-8")

    with pytest.raises(DataValidationError, match="nesmí odstranit ani změnit"):
        storage.save_items([])

    changed_item = valid_item(name="Upravený kabát")
    with pytest.raises(DataValidationError, match="nesmí odstranit ani změnit"):
        storage.save_items([changed_item])

    assert storage.items_path.read_text(encoding="utf-8") == original_contents


def test_load_items_rejects_a_file_with_one_invalid_record(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    storage.initialize()
    valid = valid_item()
    invalid = valid_item(item_id="item-002")
    invalid["condition"] = "unknown"
    storage.items_path.write_text(
        json.dumps([valid, invalid], ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(DataValidationError, match="nepovolený stav"):
        storage.load_items()


def test_load_items_rejects_corrupted_json_without_changing_file(tmp_path):
    storage = JsonStorage(tmp_path / "data")
    storage.initialize()
    corrupted_contents = '[{"id": "item-001",'
    storage.items_path.write_text(corrupted_contents, encoding="utf-8")

    with pytest.raises(DataValidationError, match="platný UTF-8 JSON"):
        storage.load_items()

    assert storage.items_path.read_text(encoding="utf-8") == corrupted_contents


def test_failed_atomic_replace_keeps_original_items_file(tmp_path, monkeypatch):
    storage = JsonStorage(tmp_path / "data")
    original_items = [valid_item()]
    storage.save_items(original_items)
    original_contents = storage.items_path.read_text(encoding="utf-8")

    def fail_replace(source, destination):
        raise OSError("simulované selhání zápisu")

    monkeypatch.setattr(os, "replace", fail_replace)

    with pytest.raises(StorageError, match="bezpečně uložit"):
        storage.save_items(original_items + [valid_item(item_id="item-002")])

    assert storage.items_path.read_text(encoding="utf-8") == original_contents
    assert list(Path(storage.data_dir).glob(".items-*.tmp")) == []