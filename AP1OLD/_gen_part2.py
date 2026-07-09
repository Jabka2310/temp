# -*- coding: utf-8 -*-
"""Generator for _t04_08_v2_part2.md"""
from pathlib import Path

OUT = Path(r"b:\school21\temp\AP1OLD\_t04_08_v2_part2.md")
PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"

lines = []

def add(*parts):
    for p in parts:
        if isinstance(p, list):
            lines.extend(p)
        else:
            lines.append(p)

def para_block(text, n=5):
    for t in text.strip().split("\n\n"):
        add(t.strip())
        add("")

def block_header(num, title, goal, time, diff):
    add(f"## Блок {num} — {title}")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| **Цель** | {goal} |")
    add(f"| **Время** | {time} |")
    add(f"| **Сложность** | {diff} |")
    add("")

def micro_step(n, title, adds, code, analysis):
    add(f"### Микро-шаг {n} — {title}")
    add("")
    add(f"**Добавляем:** {adds}")
    add("")
    add("**Напиши:**")
    add("```")
    add(code.rstrip())
    add("```")
    add("")
    add("**Разбор:**")
    add("| Строка | Код | Что делает |")
    add("|--------|-----|------------|")
    for row in analysis:
        add(f"| {row[0]} | `{row[1]}` | {row[2]} |")
    add("")

def block_footer(pause_q, ps_check, bash_check, broken, summary, nxt):
    add("### Сделай паузу")
    add(f"**Вопрос:** {pause_q}")
    add("")
    add("### Проверка")
    add("**PowerShell (Windows):**")
    add("```powershell")
    add(ps_check.rstrip())
    add("```")
    add("")
    add("<details><summary>Bash (macOS / Linux)</summary>")
    add("")
    add("```bash")
    add(bash_check.rstrip())
    add("```")
    add("")
    add("</details>")
    add("")
    add("### Если сломалось")
    add(broken)
    add("")
    add("### Микро-итог")
    add(summary)
    add("")
    add("### Дальше")
    add(nxt)
    add("")
    add("---")
    add("")

# ========== HEADER ==========
add("# T04 — Разработка построчно v2 · Часть 2")
add("")
add("> **Часть 2 из 3:** этапы C, D, E — PostgreSQL, Basic Auth, PvP.  ")
add("> **Часть 1:** этапы A и B (Gradle, T03 в памяти).  ")
add("> **Часть 3:** этапы F и G (curl, браузерный UI).  ")
add(f"> **Рабочая папка:** `{PROJECT}\\`  ")
add("> **Углубиться в теорию (опционально):** [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md)")
add("")
add("Ты закончил этап B: игра в памяти, Minimax, первый `GameController`. Теперь три задания T04: **персистентность**, **авторизация**, **мультиплеер**. Каждый блок — микро-шаги: пишешь 5–20 строк, проверяешь, идёшь дальше. Полный файл — только в **Сверка**.")
add("")
add("**Правило:** не открывай следующий блок, пока текущий не прошёл проверку.")
add("")
add("---")
add("")
add("## Оглавление части 2")
add("")
add("- [ ] **Этап C** — PostgreSQL + JPA (блоки C.1–C.8)")
add("- [ ] **Этап D** — регистрация и Basic Auth (D.1–D.9)")
add("- [ ] **Этап E** — PvP, состояния, все эндпоинты (E.1–E.8)")
add("")
add("---")
add("")

# ========== STAGE C THEORY ==========
add("# ЭТАП C — Задание 1: PostgreSQL + JPA")
add("")
add("> **Стратегия:** файлы из этапа B с пометкой «замени целиком». Удали `GameStorage.java` и `GameRepositoryImpl.java`.")
add("")
add("### Теория (прочитай до кода)")
add("")
para_block("""
**SQL и реляционные БД.** До этапа C игра жила в `HashMap` — при перезапуске JVM всё исчезало. PostgreSQL — реляционная СУБД: данные лежат в **таблицах** (строки и колонки), связи описываются ключами. `CREATE DATABASE tictactoe` создаёт отдельное пространство для нашего проекта. Spring Boot подключается по URL `jdbc:postgresql://localhost:5432/tictactoe`.

**JDBC — мост Java ↔ БД.** JDBC (Java Database Connectivity) — низкоуровневый API: `Connection`, `PreparedStatement`, `ResultSet`. Вручную писать `INSERT INTO games VALUES (?, ?, …)` для каждого поля утомительно и легко ошибиться. Spring Boot скрывает JDBC за абстракциями, но под капотом всё равно открывается соединение из пула (HikariCP).

**JPA — объектно-реляционное отображение.** JPA (Jakarta Persistence API) — спецификация: Java-класс ↔ таблица, поле ↔ колонка. Ты описываешь `@Entity`, а фреймворк генерирует SQL. **Hibernate** — самая популярная реализация JPA в Spring; именно он создаёт таблицы и выполняет `save()`.

**Spring Data JPA.** Интерфейс `GameRepository extends CrudRepository<CurrentGameEntity, UUID>` — Spring **сам** пишет реализацию: `save`, `findById`, `delete`. Метод `findByState(GameState state)` превращается в `SELECT * FROM games WHERE state = ?` по соглашению об именах. Класс `GameRepositoryImpl` из этапа B больше не нужен.

**@Entity vs @Embeddable.** `@Entity` — отдельная таблица (`games`, `users`). `@Embeddable` — «кусок» entity, колонки которого **встраиваются** в таблицу хозяина. Доска 3×3 — не отдельная таблица `boards`, а девять колонок `cell_00`…`cell_22` внутри `games`. JPA плохо маппит `int[][]` напрямую — поэтому раскладываем на поля.

**ddl-auto и схема.** Свойство `spring.jpa.hibernate.ddl-auto=update` говорит Hibernate: при старте **сравни** entity с таблицами и **добавь** недостающие колонки. Удобно для учёбы; в продакшене используют миграции (Flyway/Liquibase). `show-sql=true` печатает SQL в консоль — видишь, что реально уходит в Postgres.

**Слои после этапа C.** `GameServiceImpl` вызывает `gameRepository.save(GameMapper.toEntity(game))`. `GameMapper` переводит `CurrentGame` (domain) ↔ `CurrentGameEntity` (JPA). Domain по-прежнему не знает про `@Column` — чистая архитектура сохраняется.
""", 8)

add("### Картина в голове")
add("")
add("```")
add("GameServiceImpl  →  GameMapper.toEntity()  →  GameRepository.save()")
add("                                                      ↓")
add("                                              Hibernate / JDBC")
add("                                                      ↓")
add("                                              PostgreSQL (таблица games)")
add("```")
add("")
add("---")
add("")

# Import remaining blocks
from _gen_part2_blocks import append_blocks

append_blocks(lines, add, block_header, micro_step, block_footer, para_block)

def write_out():
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} lines to {OUT}")

if __name__ == "__main__":
    write_out()
