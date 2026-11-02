# Architektonický návrh Wardrobe

## Přehled

Wardrobe bude jednoduchá konzolová aplikace v Pythonu. Položky a kategorie ukládá do samostatných JSON souborů. Architektura odděluje konzolové rozhraní, datový model, validaci a práci se soubory; vystačí si se standardní knihovnou Pythonu.

Aplikace eviduje pouze oblečení. Při prvním spuštění vytvoří chybějící adresář `data/`, soubor kategorií naplní počátečními kategoriemi ze specifikace a soubor položek vytvoří jako prázdné pole. Existující prázdný soubor kategorií je neplatný. Existující soubory se při inicializaci nepřepisují. Celý obsah JSON souborů se ověřuje před použitím; při jediné chybě se odmítne celý soubor.

## Adresářová struktura

```text
wardrobe/
├── .github/
│   ├── agents/                  # Definice specializovaných agentů Copilotu
│   ├── instructions/            # Pravidla pro Python a testy
│   ├── skills/                  # Opakovaně použitelné návody agentů
│   └── copilot-instructions.md  # Společná projektová pravidla
├── data/
│   ├── categories.json          # Kategorie oblečení
│   └── items.json               # Evidované položky
├── src/
│   └── wardrobe/
│       ├── __init__.py          # Označení Python balíčku
│       ├── models.py            # Datové struktury Category a Item
│       ├── validation.py        # Validace vstupů a načtených dat
│       ├── storage.py           # Cesty, inicializace a JSON čtení/zápis
│       ├── add_item.py          # Konzolový příkaz pro přidávání položek
│       └── list_items.py        # Výpis a filtrování položek
├── tests/
│   ├── test_storage.py          # Testy JSON úložiště
│   ├── test_validation.py       # Testy validace
│   ├── test_add_item.py         # Testy přidávání položek
│   └── test_list_items.py       # Testy výpisu a filtrování
├── specification.md             # Funkční požadavky a datový model
├── architecture.md              # Tento architektonický návrh
├── README.md                    # Nastavení, spuštění a příklady
└── .gitignore                   # Vyloučené soubory, například __pycache__
```

Jde o cílový návrh. V době jeho vytvoření obsahuje checkout pouze dokumentaci a složku `.github`; zdrojové moduly, testy a `data/` se vytvoří až při implementaci.

## Odpovědnosti modulů

### `models.py`

Definuje jednoduché datové třídy `Category` a `Item`. Kategorie má `id` a `name`. Položka obsahuje pole stanovená specifikací a odkazuje na kategorii prostřednictvím `category_id`.

### `validation.py`

Vlastní veškerou doménovou validaci načtených i nově zadaných dat. Ověřuje povinná textová pole, povolené hodnoty sezóny a stavu, strukturu kategorií a položek, jedinečnost identifikátorů a existenci kategorie odkazované položkou. Při načítání ověřuje všechny záznamy; částečné přijetí souboru není dovoleno. Pravidla validace nepatří do `storage.py`.

### `storage.py`

Odvozuje cesty k souborům od umístění projektu, nikoli od náhodného aktuálního pracovního adresáře. Zajišťuje souborové operace: vytváří chybějící adresář `data/` a chybějící datové soubory podle pravidel v části „Inicializace a práce s JSON“, čte a zapisuje soubory a parsuje JSON na základní datové struktury. Při načítání může předat naparsovaná data `validation.py` ke kontrole, ale samo `storage.py` žádná doménová pravidla neimplementuje. Cesty k datům mají být předatelné jako parametry, aby testy mohly používat dočasné adresáře.

### `add_item.py`

Zajišťuje konzolové zadání položky. Kategorie nenabízí a hodnoty automaticky nedoplňuje. Uživatelka zadává ID kategorie přesně podle `categories.json`. Modul předá vstup validaci, vytvoří nové jedinečné ID pomocí UUID a požádá úložiště o uložení položky. Očekávané chyby převede na srozumitelné zprávy.

### `list_items.py`

Načte kategorie a položky přes úložiště a z kategorií vytvoří mapování `id` na zobrazovaný `name`. Při výpisu zobrazí název kategorie místo samotného ID; pokud by položka odkazovala na neexistující kategorii, validace souboru ji odmítne ještě před výpisem. Filtry aplikuje podle kategorie, barvy a celého názvu. Filtr kategorie přijímá ID z `categories.json`; kombinované filtry znamenají průnik podmínek. Kategorie a barva se porovnávají přesnou shodou; celý název se porovnává přesně bez rozlišení velikosti písmen. Částečný název není platným filtrem.

### Testy

Adresář `tests/` obsahuje testy jednotlivých modulů. Testy nikdy nepoužívají skutečné uživatelské soubory v `data/`.

## Datový model a příklady JSON

### Kategorie

`categories.json` je neprázdné JSON pole objektů. Každý objekt obsahuje jedinečné, neprázdné ID a neprázdný název. Při inicializaci se použije tento počáteční seznam:

```json
[
  {"id": "tops", "name": "Trička a topy"},
  {"id": "blouses", "name": "Halenky"},
  {"id": "shirts", "name": "Košile"},
  {"id": "sweaters", "name": "Svetry a kardigany"},
  {"id": "dresses", "name": "Šaty"},
  {"id": "skirts", "name": "Sukně"},
  {"id": "trousers", "name": "Kalhoty"},
  {"id": "jeans", "name": "Džíny"},
  {"id": "jackets", "name": "Bundy a saka"},
  {"id": "coats", "name": "Kabáty"}
]
```

Existující soubor kategorií obsahující `[]` je neplatný. Aplikace jej nesmí automaticky doplnit ani přepsat.

### Položka

`items.json` je JSON pole objektů. Každá položka má tato pole:

- `id`: jedinečný řetězcový identifikátor, generovaný jako UUID;
- `name`: povinný neprázdný název;
- `category_id`: ID existující kategorie;
- `color`: povinná neprázdná barva;
- `size`: povinná neprázdná velikost;
- `season`: jedna z hodnot `spring`, `summer`, `autumn`, `winter`, `all`;
- `condition`: jedna z hodnot `new`, `good`, `worn`, `damaged`;
- `notes`: volitelný řetězec.

Povinné textové hodnoty musí po odstranění počátečních a koncových mezer obsahovat alespoň jeden znak. Příklad jedné položky:

```json
[
  {
    "id": "5b2c1f17-8c3d-4c54-9f63-a4819f7e52af",
    "name": "Zimní kabát",
    "category_id": "coats",
    "color": "šedá",
    "size": "40",
    "season": "winter",
    "condition": "good",
    "notes": ""
  }
]
```

Při prvním spuštění se do `items.json` nevkládají dokumentační příklady; vytvoří se jako `[]`.

## Spolupráce modulů

### Přidání položky

1. `add_item.py` získá hodnoty od uživatelky.
2. `storage.py` zajistí existenci datových souborů a načte celé kategorie i položky.
3. `validation.py` ověří načtené soubory a nově zadané hodnoty. ID kategorie musí existovat a sezóna i stav musí být povolené.
4. `add_item.py` vytvoří nové UUID a sestaví objekt položky.
5. `storage.py` připojí položku k dosavadnímu seznamu a bezpečně uloží celý seznam.
6. Konzolové rozhraní potvrdí úspěch nebo zobrazí srozumitelnou chybu. Při chybě validace či zápisu nesmí být položka uložena.

### Výpis a filtrování

1. `list_items.py` požádá `storage.py` o validní kategorie a položky.
2. Z kategorií vytvoří mapování ID na zobrazovaný název.
3. Podle předaných filtrů vybere položky splňující všechny podmínky; filtr kategorie porovnává přesné ID.
4. Zobrazí výsledky s názvy kategorií místo jejich ID; při prázdném seznamu nebo výsledku bez shody oznámí odpovídající stav uživatelce.

## Inicializace, načítání a ukládání JSON

Cesty se odvozují od umístění projektu pomocí `pathlib.Path`, ne od aktuálního pracovního adresáře shellu. Pro testování lze úložišti předat kořenovou cestu pod `tmp_path`.

Při inicializaci:

1. Pokud adresář `data/` chybí, aplikace jej vytvoří.
2. Pokud chybí `categories.json`, vytvoří jej s počátečními kategoriemi uvedenými výše.
3. Pokud chybí `items.json`, vytvoří jej jako prázdné pole `[]`.
4. Existující soubory se inicializací nepřepisují.

Před použitím aplikace ověří celý soubor: syntaxi JSON, nejvyšší typ (pro oba soubory pole), strukturu každého záznamu, požadovaná pole a jejich typy, povolené hodnoty, jedinečnost ID a u položek existenci `category_id`. Objekty kategorií mohou obsahovat pouze `id` a `name`; objekty položek pouze pole definovaná datovým modelem, přičemž `notes` lze vynechat. Jakékoli jiné pole způsobí odmítnutí celého příslušného souboru. `categories.json` musí obsahovat alespoň jednu kategorii. Jediný chybný záznam způsobí odmítnutí celého souboru; aplikace nenačte jeho platnou část, data automaticky neopraví a soubor nepřepíše. Uživatelka dostane srozumitelnou chybovou zprávu.

JSON se čte a zapisuje v UTF-8. Při zápisu se zachovají české znaky. Seznam položek se nejprve zapíše do dočasného souboru ve stejném adresáři; původní `items.json` se nahradí až po úspěšném dokončení zápisu, například pomocí `Path.replace()` nebo `os.replace()`. Tím se sníží riziko poškození při přerušení zápisu. Chyby čtení a zápisu se oznámí; široké zachytávání výjimek se nepoužívá.

## Návrh automatických testů

Testy používají `pytest` a vestavěný fixture `tmp_path`. Každý test pracuje s vlastním dočasným adresářem; žádný test nesmí číst ani přepisovat skutečné `data/categories.json` nebo `data/items.json`. Funkce úložiště proto přijímají cestu k datovému adresáři nebo ke kořeni jako parametr.

Doporučené testovací skupiny:

- **Úložiště:** vytvoření chybějícího adresáře a souborů; počáteční kategorie; prázdné `items.json`; zachování existujících dat při inicializaci; UTF-8 a české znaky.
- **Validace:** prázdná povinná pole; neplatná sezóna či stav; neexistující kategorie; prázdné kategorie; neplatná syntaxe JSON; nesprávný kořenový typ; chybějící, nepopsaná nebo nesprávně typovaná pole; duplicitní ID; jeden chybný záznam mezi platnými záznamy; vynechané volitelné `notes`.
- **Přidávání:** uložení platné položky; odmítnutí neplatného vstupu bez změny souboru; vygenerování jedinečného ID; zachování dříve uložených položek; bezpečné chování při chybě zápisu.
- **Výpis a filtrování:** prázdný a neprázdný šatník; zobrazení názvu kategorie podle ID; samostatný filtr kategorie podle ID, barvy a celého názvu; název s odlišnou velikostí písmen; odmítnutí částečné shody; kombinace filtrů; žádné výsledky.
- **Konzolové příkazy:** podle potřeby simulovat vstup pomocí `monkeypatch` a kontrolovat výstup přes `capsys`; příkazy musí používat pouze dočasné datové soubory.

Testy mají ověřovat konkrétní návratové hodnoty, uložený obsah souborů a chování při chybách. Mají být opakovatelné a nezávislé na pořadí spuštění.

## Poznámky a otevřené body

- Specifikace uvádí příkazy `python -m src.wardrobe.add_item` a `python -m src.wardrobe.list_items` spuštěné z kořene projektu. Pro první verzi doporučujeme tento způsob zachovat a přesně jej uvést v `README.md`.
- Minimální podporovaná verze Pythonu není specifikována; určit ji před implementací.
