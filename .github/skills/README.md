# Dovednosti agentů Copilot pro Wardrobe

Tato složka obsahuje šest opakovaně použitelných souborů `SKILL.md`, jeden pro každou vývojářskou roli projektu Wardrobe.

## Instalace do repozitáře

Zkopírujte šest složek dovedností do kořenového adresáře repozitáře `wardrobe`, aby výsledná struktura vypadala takto:

```text
wardrobe/
└── .github/
    └── skills/
        ├── requirements-analyst/
        │   └── SKILL.md
        ├── software-architect/
        │   └── SKILL.md
        ├── python-developer/
        │   └── SKILL.md
        ├── test-engineer/
        │   └── SKILL.md
        ├── code-reviewer/
        │   └── SKILL.md
        └── documentation-reviewer/
            └── SKILL.md
```

V archivu jsou složky umístěné přímo pod `wardrobe-agent-skills/`. Při kopírování do repozitáře je vložte pod `.github/skills/`.

Dovednost poskytuje opakovaně použitelné pokyny; není to totéž co vlastní agent. Soubory `.agent.md` definují agenty, zatímco soubory `SKILL.md` obsahují pokyny pro konkrétní úlohy. Podle verze a konfigurace VS Code/GitHub Copilot ověřte v oficiální dokumentaci, které umístění pro vyhledávání dovedností agentů je podporováno.
