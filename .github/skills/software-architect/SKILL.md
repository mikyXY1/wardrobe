---
name: software-architect
description: Navrhuje jednoduchou a udržovatelnou architekturu aplikace Wardrobe v Pythonu a tok dat ve formátu JSON.
---

# Dovednost: Návrh architektury

Tuto dovednost použijte při plánování modulů, rozhraní, datových struktur nebo uspořádání projektu.

## Pokyny

1. Před návrhem změn si přečtěte schválený soubor `specification.md` a prohlédněte stávající strukturu repozitáře.
2. Upřednostňujte malou architekturu využívající standardní knihovnu Pythonu, pokud další závislost nepřináší jasný přínos.
3. Jasně oddělte konzolovou interakci, validaci vstupů, doménová pravidla a ukládání dat JSON.
4. Definujte datové struktury položek a kategorií v souladu se specifikací; pro odkaz na kategorii použijte `category_id`.
5. Určete způsob řešení cest k souborům tak, aby aplikace fungovala bez ohledu na aktuální pracovní adresář shellu.
6. Popište, jak se bez tichého zahazování dat řeší chybějící soubory, neplatný JSON, chybně utvořená data a chyby při čtení či zápisu.
7. Doporučte bezpečné ukládání, například zápis do dočasného souboru a nahrazení původního souboru až po úspěšném zápisu.
8. Zajistěte, aby bylo možné návrh testovat s dočasnými datovými soubory, aniž by se měnila skutečná uživatelská data šatníku.
9. Vyhněte se zbytečným frameworkům, databázím, grafickým komponentám a funkcím mimo schválenou minimální verzi produktu (MVP).
10. Před implementací představte navržený strom adresářů, odpovědnosti modulů, klíčová rozhraní a dosud nevyřešená rozhodnutí.
