---
name: test-engineer
description: Navrhuje a spouští testy požadavků, validace, ukládání JSON a filtrování položek v projektu Wardrobe.
---

# Dovednost: Testování

Tuto dovednost použijte při vytváření, kontrole nebo spouštění testů.

## Pokyny

1. Odvozujte testovací případy od souboru `specification.md` a jeho akceptačních kritérií; nepředpokládejte nezdokumentované chování.
2. Pokryjte úspěšné postupy, neplatné vstupy, hraniční případy, prázdná data a očekávané chyby.
3. Testujte chybějící povinná pole, hodnoty obsahující pouze bílé znaky, neznámé kategorie, neplatné sezóny a neplatné hodnoty stavu.
4. Testujte filtrování podle každého podporovaného pole i kombinace filtrů; ověřte, že kombinované filtry vracejí pouze položky splňující všechny zadané podmínky.
5. Testujte vyhledávání názvu bez rozlišení velikosti písmen i odpověď pro případ, kdy nejsou nalezeny žádné výsledky.
6. Pokud je to praktické, testujte chybějící soubory, chybný JSON, neplatné datové struktury a chyby při čtení či zápisu.
7. Pokud je `pytest` dostupný nebo schválený projektem, používejte jej a testy izolujte pomocí dočasných adresářů a souborů.
8. Nikdy nedovolte, aby testy přepsaly skutečné soubory `data/items.json` nebo `data/categories.json`.
9. Ověřujte konkrétní výstupy, uložený obsah a chování při chybách, ne pouze to, že se funkce spustila.
10. Uveďte přesné spuštěné testy, jejich výsledky a nepokrytá akceptační kritéria; nikdy netvrďte, že testy prošly, pokud nebyly spuštěny.
