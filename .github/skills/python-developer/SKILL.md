---
name: python-developer
description: Implementuje schválené požadavky projektu Wardrobe v čitelném a odolném kódu Pythonu.
---

# Dovednost: Vývoj v Pythonu

Tuto dovednost použijte při implementaci nebo úpravách kódu aplikace.

## Pokyny

1. Před úpravami si přečtěte `specification.md`, příslušné projektové pokyny a stávající kód související s požadovanou změnou.
2. Zachovávejte užitečnou stávající strukturu a vyhněte se nesouvisejícím refaktoringům nebo přepisování souborů bez důvodu.
3. Implementujte pouze schválené požadavky; nepřidávejte funkce, jako jsou ceny, databáze nebo grafické rozhraní, pokud o ně uživatel nepožádá.
4. Oddělujte odpovědnosti za konzolový vstup a výstup, validaci a ukládání JSON.
5. Pro cesty používejte `pathlib` a při čtení nebo zápisu textu JSON výslovně nastavte UTF-8.
6. Před uložením položky ověřte povinná textová pole, povolené hodnoty sezóny a stavu i existenci vybrané kategorie.
7. Každé nové položce přidělte jedinečné ID a při přidání další položky zachovejte všechny již uložené položky.
8. Očekávané chyby souborů a JSON zpracujte srozumitelnými zprávami; nepoužívejte široké zachytávání výjimek k maskování vad.
9. Při každé změně chování přidejte nebo aktualizujte automatizované testy a pro testovací data používejte dočasné soubory nebo fixture.
10. Na závěr shrňte změněné soubory a uveďte pouze testy a kontroly, které byly skutečně spuštěny; jasně sdělte, pokud některá kontrola nebyla spuštěna nebo selhala.
