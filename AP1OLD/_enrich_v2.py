# -*- coding: utf-8 -*-
"""Enrich T04_08 v2: restore verify sections and expand theory from v1 backup."""
import re
from pathlib import Path

OUT = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
BAK = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО_v1_backup.md")

THEORY_EXTRA = {
    "A.4": """
**Spring Boot entry point:** класс с `@SpringBootApplication` + `main` → `SpringApplication.run` поднимает контекст Spring, сканирует пакет `tictactoe` и **все подпакеты**, стартует embedded Tomcat на **8080**.

Без этого класса `bootRun` не знает, что запускать.
""",
    "B.1": """
**Value Object:** объект без идентичности — важно *содержимое* (клетки), не ссылка. Две доски с одинаковыми цифрами — «равны» по смыслу.

**Почему int, а не char X/O:** JSON `[[0,1,0],...]` проще парсить; Minimax считает на числах быстрее.

**Инкапсуляция:** `private final int[][] cells` + `getCells()` с копией — никто снаружи не сделает `board.getCells()[0][0]=9`.
""",
    "B.9": """
**GameServiceImpl** — «мозг» T03. Три кита:

1. **validateBoard** — анти-чит: между сохранённой и присланной доской ровно **одна** новая клетка игрока (1).
2. **evaluate / isDraw** — победа по строкам/столбцам/диагоналям или ничья.
3. **Minimax** — для каждой пустой клетки «проигрывает» партию до конца; выбирает ход с лучшим score.

`findBestMove` → перебор клеток → `minimax` рекурсивно. `isMax=true` — ход компьютера (максимизируем), `false` — ход игрока (минимизируем).
""",
    "D.7": """
**Servlet Filter** — код *до* контроллера. Цепочка: `AuthFilter` → `DispatcherServlet` → `@RestController`.

Если пароль неверный: `setStatus(401)` + **`return`** без `chain.doFilter` — запрос **не доходит** до `GameController`.

`request.setAttribute("currentUserId", uuid)` — «пропуск» с бейджем: контроллер узнаёт, кто ты, без повторного разбора Basic Auth.
""",
    "E.6": """
**makeMove** — единая точка хода:

1. Загрузить игру из БД.
2. Проверить `PLAYER_TURN`, `currentTurnPlayerId`, `validateBoard`.
3. Применить доску игрока.
4. **PvE:** `getNextMove` (Minimax) + `updateGameState`.
5. **PvP:** сменить `currentTurnPlayerId` на соперника + `updateGameState`.

Ошибка «Not your turn» — когда UUID в запросе ≠ `currentTurnPlayerId`.
""",
}

def parse_v1_blocks(text):
    blocks = {}
    for m in re.finditer(r"## (Блок [^\n]+)\r?\n", text):
        title = m.group(1)
        start = m.end()
        nxt = re.search(r"\r?\n## Блок ", text[start:])
        end = start + nxt.start() if nxt else len(text)
        blocks[title] = text[m.start() : end]
    return blocks


def extract_section(block, name):
    m = re.search(rf"### {name}\r?\n+([\s\S]*?)(?=\r?\n### |\r?\n---|\Z)", block)
    return m.group(1).strip() if m else ""


def main():
    v2 = OUT.read_text(encoding="utf-8")
    v1 = BAK.read_text(encoding="utf-8")
    v1blocks = parse_v1_blocks(v1)

    def repl_block(m):
        title = m.group(1)
        body = m.group(2)
        key = re.search(r"Блок ([A-G]\.\d+[a-z]?)", title)
        key = key.group(1) if key else ""

        v1b = v1blocks.get(title, "")
        if v1b:
            z = extract_section(v1b, "Зачем")
            pic = extract_section(v1b, "Перед тем как писать")
            pause = extract_section(v1b, "Сделай паузу")
            verify = extract_section(v1b, "Проверка")
            trouble = extract_section(v1b, "Если сломалось")
            summary = extract_section(v1b, "Микро-итог")

            extra = THEORY_EXTRA.get(key, "")
            theory_parts = [p for p in [extra.strip(), z] if p]
            if theory_parts:
                new_theory = "\n\n".join(theory_parts)
                body = re.sub(
                    r"### Теория \(прочитай до кода\)\r?\n+[\s\S]*?(?=\r?\n### Картина)",
                    lambda _m: "### Теория (прочитай до кода)\n\n" + new_theory + "\n",
                    body,
                    count=1,
                )
            if pic and "Дополняешь проект" in body:
                body = re.sub(
                    r"### Картина в голове\r?\n+[\s\S]*?(?=\r?\n### Микро-шаг)",
                    lambda _m: "### Картина в голове\n\n" + pic + "\n",
                    body,
                    count=1,
                )
            if pause:
                body = re.sub(
                    r"### Сделай паузу\r?\n+[\s\S]*?(?=\r?\n### Проверка)",
                    lambda _m: "### Сделай паузу\n\n" + pause + "\n",
                    body,
                    count=1,
                )
            if verify and len(verify) > 30:
                v = verify
                body = re.sub(
                    r"### Проверка\r?\n+[\s\S]*?(?=\r?\n### Если сломалось)",
                    lambda _m: "### Проверка\n\n" + v + "\n",
                    body,
                    count=1,
                )
            if trouble:
                body = re.sub(
                    r"### Если сломалось\r?\n+[\s\S]*?(?=\r?\n### Микро-итог)",
                    lambda _m: "### Если сломалось\n\n" + trouble + "\n",
                    body,
                    count=1,
                )
            if summary and "Файл готов" in body:
                body = re.sub(
                    r"### Микро-итог\r?\n+[\s\S]*?(?=\r?\n---|\Z)",
                    lambda _m: "### Микро-итог\n\n" + summary + "\n",
                    body,
                    count=1,
                )
        return f"## {title}\n{body}"

    v2 = re.sub(r"## (Блок [^\n]+)\r?\n([\s\S]*?)(?=\r?\n---\r?\n|\Z)", repl_block, v2)
    OUT.write_text(v2, encoding="utf-8")
    print("Enriched", OUT, "lines:", len(v2.splitlines()))


if __name__ == "__main__":
    main()
