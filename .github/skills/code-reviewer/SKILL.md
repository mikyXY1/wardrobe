---
name: code-reviewer
description: Kontroluje správnost kódu projektu Wardrobe, bezpečnost dat, udržovatelnost a soulad se specifikací.
---

# Dovednost: Kontrola kódu

Tuto dovednost použijte k nezávislé kontrole změn v kódu.

## Pokyny

1. Před oznámením zjištění si přečtěte související požadavky a prohlédněte změněný kód i související volající části a testy.
2. Nejprve se zaměřte na správnost, ztrátu dat, zpracování neplatných vstupů, výjimky a odchylky od `specification.md`.
3. Ověřte, že zápis JSON nemůže omylem zahodit existující položky ani po chybě zanechat datový soubor zapsaný jen částečně.
4. Ověřte, že se před uložením dat kontrolují odkazy na kategorie a povolené hodnoty.
5. Ověřte, že filtry fungují konzistentně při samostatném i kombinovaném použití.
6. Hledejte křehce sestavené cesty, skryté závislosti na aktuálním pracovním adresáři, problémy s kódováním a nesprávné zpracování českých znaků.
7. Ověřte, že testy oddělují svá data a nemění skutečné soubory šatníku.
8. Každé zjištění uveďte se závažností, souborem a místem, stručným vysvětlením, dopadem a praktickým návrhem opravy.
9. Rozlišujte prokazatelné vady od volitelných stylistických vylepšení; nevydávejte domněnky za fakta.
10. Během kontroly neupravujte soubory, pokud vás uživatel výslovně nepožádá o opravu zjištěných problémů.
