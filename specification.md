# Specification – Wardrobe

**Projekt:** Evidence dámského šatníku  
**Verze:** 1.0  
**Jazyk implementace:** Python 3  
**Ukládání dat:** JSON soubory  
**Typ aplikace:** Jednoduchá konzolová aplikace

---

## 1. Cíl projektu

Cílem projektu `wardrobe` je vytvořit jednoduchou aplikaci pro evidenci dámského šatníku. Uživatelka bude moci přidávat oblečení, zobrazovat evidované položky a filtrovat je podle zadaných parametrů.

Projekt má sloužit také jako praktické cvičení při vývoji aplikace v Pythonu s podporou GitHub Copilot ve VS Code. Návrh má být jednoduchý, přehledný, testovatelný a snadno rozšiřitelný.

## 2. Rozsah první verze (MVP)

První verze musí umožňovat:

1. načíst seznam kategorií z JSON souboru;
2. načíst evidované položky šatníku z JSON souboru;
3. zadat novou položku;
4. ověřit povinné údaje a platnost kategorie;
5. uložit novou položku do JSON souboru;
6. vypsat všechny položky;
7. filtrovat položky podle jednoho nebo více parametrů;
8. srozumitelně zobrazit chyby při neplatném vstupu nebo problému se souborem.

První verze nebude vyžadovat grafické uživatelské rozhraní, databázi, přihlašování, internetové připojení ani evidenci cen.

## 3. Kategorie šatníku

Kategorie budou uloženy v samostatném souboru `data/categories.json`. Každá kategorie má jedinečný identifikátor a název.

Počáteční seznam kategorií:

| ID | Název |
|---|---|
| `tops` | Trička a topy |
| `blouses` | Halenky |
| `shirts` | Košile |
| `sweaters` | Svetry a kardigany |
| `dresses` | Šaty |
| `skirts` | Sukně |
| `trousers` | Kalhoty |
| `jeans` | Džíny |
| `jackets` | Bundy a saka |
| `coats` | Kabáty |

Kategorie lze v budoucnu rozšířit bez změny struktury položky. Položka musí odkazovat na existující kategorii pomocí jejího ID, nikoli pouze pomocí zobrazovaného názvu.

Příklad `data/categories.json`:

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

## 4. Datový model položky

Každá položka šatníku bude obsahovat tato pole:

| Pole | Typ | Povinné | Význam |
|---|---|---|---|
| `id` | řetězec | Ano | Jedinečný identifikátor položky |
| `name` | řetězec | Ano | Název položky |
| `category_id` | řetězec | Ano | ID kategorie ze souboru kategorií |
| `color` | řetězec | Ano | Barva |
| `size` | řetězec | Ano | Velikost, například M nebo 38 |
| `season` | řetězec | Ano | Sezóna: `spring`, `summer`, `autumn`, `winter` nebo `all` |
| `condition` | řetězec | Ano | Stav: `new`, `good`, `worn` nebo `damaged` |
| `notes` | řetězec | Ne | Volitelná poznámka |

ID musí být jedinečné. Doporučené řešení je UUID uložené jako řetězec. Všechny povinné textové hodnoty musí po odstranění počátečních a koncových mezer obsahovat alespoň jeden znak.

Příklad `data/items.json` s pěti počátečními položkami:

```json
[
  {
    "id": "item-001",
    "name": "Bílé bavlněné tričko",
    "category_id": "tops",
    "color": "bílá",
    "size": "M",
    "season": "all",
    "condition": "good",
    "notes": "Základní kousek"
  },
  {
    "id": "item-002",
    "name": "Modrá halenka",
    "category_id": "blouses",
    "color": "modrá",
    "size": "38",
    "season": "spring",
    "condition": "good",
    "notes": ""
  },
  {
    "id": "item-003",
    "name": "Černé kalhoty",
    "category_id": "trousers",
    "color": "černá",
    "size": "38",
    "season": "all",
    "condition": "good",
    "notes": "Do práce"
  },
  {
    "id": "item-004",
    "name": "Červené šaty",
    "category_id": "dresses",
    "color": "červená",
    "size": "M",
    "season": "summer",
    "condition": "new",
    "notes": "Na společenské příležitosti"
  },
  {
    "id": "item-005",
    "name": "Zimní kabát",
    "category_id": "coats",
    "color": "šedá",
    "size": "40",
    "season": "winter",
    "condition": "worn",
    "notes": ""
  }
]
```

## 5. Funkční požadavky

### FR-01 – Přidání nové položky

Aplikace musí umožnit zadání nové položky prostřednictvím konzolového skriptu.

Uživatel zadá název, ID kategorie, barvu, velikost, sezónu, stav a případnou poznámku. ID kategorie musí zadat přesně podle souboru `categories.json`, například `tops`. Aplikace nenabízí seznam kategorií ani návrhy nebo automatické doplnění hodnot; správné zadání vstupních údajů zajišťuje uživatel. Aplikace:

1. načte kategorie pro ověření zadaného ID;
2. ověří povinné údaje;
3. ověří, že zadané ID kategorie existuje;
4. ověří povolenou hodnotu sezóny a stavu;
5. vygeneruje jedinečné ID;
6. uloží položku do JSON souboru;
7. potvrdí úspěšné uložení.

Při neplatném vstupu, včetně neexistujícího ID kategorie, se položka nesmí uložit. Uživatel musí dostat srozumitelnou chybovou zprávu; aplikace hodnotu sama neopravuje ani nenahrazuje.

### FR-02 – Výpis položek

Aplikace musí umožnit vypsat všechny uložené položky v přehledné podobě. U položky zobrazí minimálně název, kategorii, barvu, velikost, sezónu a stav.

Pokud seznam neobsahuje žádné položky, aplikace zobrazí informaci, že je šatník prázdný.

### FR-03 – Filtrování položek

Uživatel musí moci filtrovat položky podle jednoho nebo více parametrů:

- kategorie;
- barva;
- celý název položky.

Filtry lze kombinovat; výsledkem jsou pouze položky, které splňují všechny zadané podmínky. Kategorie a barva se porovnávají přesnou shodou. Pro filtrování podle názvu musí uživatel zadat celý název položky; porovnání celého názvu je přesné a nerozlišuje velikost písmen. Částečný název není platným filtrem. Pokud uživatel žádný filtr nezadá, skript vypíše všechny položky. Pokud filtrům neodpovídá žádná položka, aplikace zobrazí informaci, že nebyla nalezena žádná shoda.

### FR-04 – Práce se soubory

JSON soubory se načítají z předvídatelného umístění vzhledem ke kořenovému adresáři projektu, nikoli podle aktuálního pracovního adresáře shellu.

Pokud neexistuje adresář `data/`, aplikace jej při inicializaci vytvoří. Pokud `data/categories.json` neexistuje, aplikace jej vytvoří jako validní JSON soubor naplněný počátečními kategoriemi uvedenými v kapitole 3. Pokud `data/items.json` neexistuje, aplikace jej vytvoří jako validní JSON soubor s prázdným polem (`[]`); ukázkové položky z kapitoly 4 jsou pouze příkladem a při inicializaci se do souboru nevkládají. Existující soubory nesmí být při této inicializaci přepsány.

Aplikace musí před použitím ověřit celý obsah obou souborů. Soubor je platný pouze tehdy, pokud obsahuje syntakticky validní JSON správného nejvyššího typu a každý záznam odpovídá datovému modelu: obsahuje povinná pole správných typů a platných hodnot, identifikátory jsou jedinečné a každá položka odkazuje na existující kategorii. Objekty kategorií mohou obsahovat pouze pole `id` a `name`. Objekty položek mohou obsahovat pouze pole uvedená v datovém modelu; volitelné pole `notes` může být vynecháno. Jakékoli další nepopsané pole je chyba. `categories.json` musí obsahovat alespoň jednu kategorii; existující prázdné pole kategorií je neplatné. U kategorií musí být jedinečná ID a vyplněná ID i názvy. Pokud je chybný soubor nebo jediný záznam, aplikace odmítne celý soubor; nesmí načíst jen jeho platnou část, data automaticky opravovat ani soubor přepsat. Uživatel dostane srozumitelnou chybovou zprávu.

Aplikace musí srozumitelně ošetřit také chybu čtení nebo zápisu.

Při ukládání nové položky nesmí dojít ke ztrátě již existujících položek. Zápis musí být bezpečný vůči částečnému přepsání souboru; doporučuje se nejprve zapsat do dočasného souboru a poté jej atomicky nahradit.

## 6. Nefunkční požadavky

- Použít Python 3 a standardní knihovnu, pokud není doložen důvod pro další závislost.
- Zdrojový kód rozdělit do menších modulů s jasnou odpovědností.
- Dodržovat čitelné názvy proměnných a funkcí.
- Oddělit uživatelské rozhraní, validaci a práci s JSON soubory.
- Ošetřovat očekávané chyby; nezakrývat je prázdným obecným `except`.
- Přidat automatické testy pro hlavní funkce.
- Dokumentovat spuštění a příklady použití v `README.md`.
- Uchovávat data v UTF-8 a zachovat české znaky.
- Nepoužívat cenu položky; evidence ceny není součástí této verze.

## 7. Návrh adresářové struktury

```text
wardrobe/
├── .github/
│   ├── agents/
│   │   ├── requirements-analyst.agent.md
│   │   ├── architect.agent.md
│   │   ├── python-developer.agent.md
│   │   ├── test-engineer.agent.md
│   │   ├── code-reviewer.agent.md
│   │   └── documentation-reviewer.agent.md
│   ├── instructions/
│   │   ├── python.instructions.md
│   │   └── tests.instructions.md
│   └── copilot-instructions.md
├── data/
│   ├── categories.json
│   └── items.json
├── src/
│   └── wardrobe/
│       ├── __init__.py
│       ├── storage.py
│       ├── models.py
│       ├── validation.py
│       ├── add_item.py
│       └── list_items.py
├── tests/
│   ├── test_storage.py
│   ├── test_validation.py
│   ├── test_add_item.py
│   └── test_list_items.py
├── specification.md
├── README.md
└── .gitignore
```

Toto je cílový návrh, nikoli tvrzení o aktuálním obsahu checkoutovaného repozitáře. Při implementaci se nejprve zkontroluje stávající struktura a existující soubory se bez důvodu nepřepisují.

### Odpovědnost modulů

- `storage.py` – načítání a bezpečné ukládání JSON dat.
- `models.py` – datová struktura položky a případné pomocné typy.
- `validation.py` – validace povinných polí, sezóny, stavu a kategorie.
- `add_item.py` – konzolové zadání a přidání položky.
- `list_items.py` – výpis a filtrování položek.
- `tests/` – automatické testy jednotlivých funkcí.

Pokud se při kontrole repozitáře ukáže, že již obsahuje vhodnou strukturu, je možné ji upravit místo přesného kopírování tohoto návrhu.

## 8. Návrh rozhraní příkazové řádky

Doporučené příklady použití z kořenového adresáře projektu:

```bash
python -m src.wardrobe.add_item
python -m src.wardrobe.list_items
python -m src.wardrobe.list_items --category tops
python -m src.wardrobe.list_items --color černá
python -m src.wardrobe.list_items --name "Zimní kabát"
python -m src.wardrobe.list_items --category tops --color bílá
python -m src.wardrobe.list_items --category coats --name "Zimní kabát" --color šedá
```

Poznámka k implementaci: příkazy výše definují požadované rozhraní. Pokud se použije balíček `src/wardrobe`, musí být správně připraveno spouštění modulu a importy. Alternativně lze projekt nastavit jako instalovatelný balíček. Vývojář musí zvolit jeden konzistentní způsob a zdokumentovat jej v `README.md`.

## 9. Akceptační kritéria

### Přidání položky

- [ ] Platná položka se uloží do `items.json`.
- [ ] Nově vytvořené ID je jedinečné.
- [ ] Neexistující kategorie je odmítnuta.
- [ ] Prázdný název nebo jiné povinné pole je odmítnuto.
- [ ] Neplatná sezóna nebo stav je odmítnut.
- [ ] Přidání položky zachová všechny dříve uložené položky.
- [ ] Chyba zápisu je oznámena srozumitelně.

### Výpis a filtrování

- [ ] Bez filtru se zobrazí všechny položky.
- [ ] Filtr podle kategorie vrátí pouze položky z této kategorie.
- [ ] Filtr podle barvy vrátí pouze položky s přesně odpovídající barvou.
- [ ] Filtr podle názvu vyžaduje celý název a porovnává jej přesně bez rozlišení velikosti písmen.
- [ ] Částečný název jako filtr nevrátí položku s delším názvem.
- [ ] Kombinace filtrů vrátí pouze položky splňující všechny zadané podmínky.
- [ ] Prázdný výsledek je oznámen uživateli.

### Práce s daty a testy

- [ ] JSON soubory jsou validní a obsahují české znaky správně.
- [ ] Chybějící `categories.json` se vytvoří jako validní JSON soubor obsahující počáteční kategorie z kapitoly 3.
- [ ] Chybějící `items.json` se vytvoří jako validní JSON soubor obsahující prázdné pole; ukázkové položky se do něj automaticky nevkládají.
- [ ] Chybějící adresář `data/` se vytvoří automaticky před vytvořením datových souborů.
- [ ] Při inicializaci se nepřepíší existující datové soubory.
- [ ] Celý soubor se ověří před použitím; neplatný JSON, nesprávný nejvyšší typ nebo jediný chybný záznam způsobí odmítnutí celého souboru.
- [ ] Nepopsané pole v objektu kategorie nebo položky způsobí odmítnutí celého příslušného souboru; vynechání volitelného `notes` je platné.
- [ ] Existující `categories.json` obsahující prázdné pole je odmítnut jako neplatný.
- [ ] Při chybě validace se žádná část souboru nenačte, data se automaticky neopraví a původní soubor se nepřepíše.
- [ ] Testy nepracují s reálnými uživatelskými daty; používají dočasné soubory.
- [ ] Testy pokrývají úspěšné i chybové scénáře.
- [ ] Postup spuštění je popsán v `README.md`.

## 10. Testovací scénáře pro první verzi

| ID | Scénář | Očekávaný výsledek |
|---|---|---|
| TC-01 | Přidání platné položky se zadanými hodnotami | Položka se uloží se zadanými hodnotami všech polí, dostane jedinečné ID a lze ji znovu načíst |
| TC-02 | Přidání položky s prázdným názvem | Validace položku odmítne |
| TC-03 | Přidání položky s neexistující kategorií | Validace položku odmítne |
| TC-04 | Přidání položky s neplatnou sezónou | Validace položku odmítne |
| TC-05 | Výpis neprázdného šatníku | Zobrazí se všechny položky |
| TC-06 | Výpis prázdného šatníku | Zobrazí se informace o prázdném seznamu |
| TC-07 | Filtrování podle kategorie | Zobrazí se pouze odpovídající položky |
| TC-08 | Kombinace kategorie a barvy | Zobrazí se průnik obou filtrů |
| TC-09 | Filtrování podle celého názvu zadaného s jinou velikostí písmen | Odpovídající položka se najde |
| TC-10 | Neplatný JSON soubor | Aplikace ohlásí chybu a nepřepíše data |
| TC-11 | Přidání položky do již existujícího seznamu | Původní položky zůstanou zachovány |
| TC-12 | Filtr bez výsledků | Zobrazí se zpráva o nenalezené shodě |
| TC-13 | Chybějící adresář `data/` a datové soubory | Aplikace vytvoří adresář, `categories.json` s počátečními kategoriemi a `items.json` jako prázdné JSON pole |
| TC-14 | Filtrování podle částečného názvu | Částečný název se nepovažuje za shodu s celým názvem položky |
| TC-15 | Soubor obsahuje platné záznamy a jeden chybný záznam | Aplikace odmítne celý soubor, nenačte jeho platnou část a původní soubor nezmění |
| TC-16 | Soubor má nesprávný nejvyšší JSON typ, chybějící povinné pole, nesprávný typ pole nebo duplicitní ID | Aplikace odmítne celý soubor a oznámí chybu |
| TC-17 | Přidání položky s nepovolenou hodnotou stavu | Validace položku odmítne a soubor s položkami zůstane nezměněn |
| TC-18 | Chyba při zápisu položky | Aplikace oznámí chybu srozumitelně a původní soubor s položkami zůstane nepoškozený |
| TC-19 | Existující `categories.json` obsahuje prázdné pole | Aplikace odmítne celý soubor kategorií, oznámí chybu a soubor nezmění |
| TC-20 | Objekt kategorie nebo položky obsahuje nepopsané pole | Aplikace odmítne celý příslušný soubor; položka bez volitelného pole `notes` zůstává platná |

## 11. Doporučený postup implementace

1. Prohlédnout stávající checkout repozitáře a zachovat užitečné soubory.
2. Zkontrolovat tuto specifikaci agentem pro analýzu požadavků.
3. Vyřešit nejasnosti a schválit datový model.
4. Navrhnout architekturu a potvrdit adresářovou strukturu.
5. Při inicializaci vytvořit `categories.json` s počátečními kategoriemi a `items.json` jako prázdné pole; ukázkové položky použít pouze v dokumentaci nebo izolovaných testech.
6. Implementovat validaci a práci s JSON.
7. Implementovat přidávání položek.
8. Implementovat výpis a filtrování.
9. Doplnit automatické testy a spustit je.
10. Provést kontrolu kódu a dokumentace.
11. Ověřit všechna akceptační kritéria.

Každá fáze má mít konkrétní výstup a kontrolu před pokračováním. Copilot nemá bez potvrzení uživatelky automaticky rozšiřovat rozsah projektu o nové funkce.

## 12. Co není součástí první verze

Následující funkce lze zvážit později, ale nemají být implementovány bez nového požadavku:

- mazání a editace položek;
- fotografie oděvů;
- plánování outfitů;
- statistiky využívání oblečení;
- grafické uživatelské rozhraní;
- databáze;
- import a export do jiných formátů.