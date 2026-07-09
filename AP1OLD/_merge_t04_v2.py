# -*- coding: utf-8 -*-
"""Merge part1 + part2 + F-G tail into unified T04_08 v2."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
PART1 = ROOT / "_t04_08_v2_part1.md"
PART2 = ROOT / "_t04_08_v2_part2.md"
MAIN = ROOT / "T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md"
PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"

HEADER = f"""# T04 — Разработка построчно v2: постепенный код + теория

> **Формат v2:** код **наращивается микро-шагами**. Полный файл — только в **«Сверка: файл целиком»**.  
> **Рабочая папка:** `{PROJECT}`  
> **Не подглядывай** в готовый проект до «Проверки» блока.  
> **Теория глубже (опционально):** [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md)

---

## Как читать v2

1. **Теория** — до кода.  
2. **Микро-шаги** — дописываешь в IDE по одному фрагменту.  
3. **Сверка** — полный файл в конце блока.  
4. **Проверка** — команда в терминале.

---

## Оглавление

- [ ] **Этап A** — Среда, Gradle, первый `bootRun`
- [ ] **Этап B** — T03 в памяти (PvE + Minimax)
- [ ] **Этап C** — PostgreSQL + JPA
- [ ] **Этап D** — Basic Auth
- [ ] **Этап E** — PvP + все эндпоинты
- [ ] **Этап F** — curl-сценарии
- [ ] **Этап G** — Браузерный UI

---

## Команды (Windows)

```powershell
cd {PROJECT}
java -version
.\\gradlew.bat bootRun
```

<details><summary>Bash (macOS / Linux)</summary>

```bash
cd src/TicTacToe_1.2_sql_auth
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
./gradlew bootRun
```

</details>

---

"""


def strip_part_header(text: str, start_marker: str) -> str:
    idx = text.find(start_marker)
    if idx < 0:
        raise ValueError(f"Marker not found: {start_marker!r}")
    return text[idx:].strip()


def clean_part1(text: str) -> str:
    text = strip_part_header(text, "# Пролог —")
    text = re.sub(
        r"\n---\n\n\*Сгенерировано.*?\*\n?",
        "\n",
        text,
        flags=re.DOTALL,
    )
    text = text.replace("**Часть 1** доводит тебя", "**Этапы A–B** доводят тебя")
    text = text.replace(
        "**Дорожная карта всего T04** (часть 1 покрывает только начало):",
        "**Дорожная карта всего T04:**",
    )
    text = re.sub(
        r"\*\*Этап C\*\* — PostgreSQL \+ JPA \(часть 2\)\.",
        "**Этап C** — PostgreSQL + JPA.",
        text,
    )
    return text.strip()


def clean_part2(text: str) -> str:
    return strip_part_header(text, "# ЭТАП C —").strip()


def tail_from_main(text: str) -> str:
    idx = text.find("# Теория перед этапом F")
    if idx < 0:
        idx = text.find("# ЭТАП F")
    if idx < 0:
        raise ValueError("Stage F not found in main file")
    tail = text[idx:].strip()
    tail = re.sub(
        r"## Навигация по v2[\s\S]*$",
        "",
        tail,
    ).strip()
    tail = tail.replace("часть 3", "этап F")
    tail = tail.replace("_t04_08_v2_part1.md", "T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
    tail = tail.replace("_t04_08_v2_part2.md", "T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
    return tail


def main():
    p1 = clean_part1(PART1.read_text(encoding="utf-8"))
    p2 = clean_part2(PART2.read_text(encoding="utf-8"))
    fg = tail_from_main(MAIN.read_text(encoding="utf-8"))

    merged = HEADER + p1 + "\n\n---\n\n" + p2 + "\n\n---\n\n" + fg + "\n"
    MAIN.write_text(merged, encoding="utf-8")
    print(f"Merged {len(merged.splitlines())} lines -> {MAIN}")


if __name__ == "__main__":
    main()
