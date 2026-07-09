# -*- coding: utf-8 -*-
"""Generator for T04_08 v2 Part 1."""
from pathlib import Path

from _gen_t04_08_v2_blocks import generate_stage_a, generate_theory_before_b, generate_stage_b
from _gen_t04_08_v2_padding import generate_padding

PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"
OUT = Path(r"b:\school21\temp\AP1OLD\_t04_08_v2_part1.md")

lines: list[str] = []

def add(*parts):
    for p in parts:
        lines.append(p)

def blank(n=1):
    for _ in range(n):
        lines.append("")

def table_goal(goal, time, diff):
    add(
        "| | |",
        "|---|---|",
        f"| **Цель** | {goal} |",
        f"| **Время** | {time} |",
        f"| **Сложность** | {diff} |",
        "",
    )

def theory_paragraphs(texts):
    add("### Теория (прочитай до кода)")
    blank()
    for t in texts:
        add(t)
        blank()

def kartina(texts):
    add("### Картина в голове")
    blank()
    for t in texts:
        add(t)
        blank()

def _detect_lang(code: str) -> str:
    s = code.strip()
    if s.startswith("package") or s.startswith("import org.") or s.startswith("public class"):
        return "java"
    if s.startswith("plugins") or s.startswith("rootProject"):
        return "kotlin"
    if s.startswith("server."):
        return "properties"
    if s.startswith("$") or s.startswith("cd ") or s.startswith(".\\") or s.startswith("Invoke") or s.startswith("Get-Content"):
        return "powershell"
    if s.startswith("export") or s.startswith("./") or s.startswith("GAME_ID") or s.startswith("curl"):
        return "bash"
    return "text"

def micro_step(n, title, dobavlyaem, napishi, razbor_rows):
    add(f"### Микро-шаг {n} — {title}")
    blank()
    add(f"**Добавляем:** {dobavlyaem}")
    blank()
    add("**Напиши:**")
    blank()
    add(f"```{_detect_lang(napishi)}")
    add(napishi.rstrip())
    add("```")
    blank()
    add("**Разбор:**")
    blank()
    add("| Строка / фрагмент | Код | Что делает |")
    add("|-------------------|-----|------------|")
    for row in razbor_rows:
        add(f"| {row[0]} | `{row[1]}` | {row[2]} |")
    blank()

def block_footer(pause_q, ps_check, bash_check, broken, itog, dalshe):
    add("### Сделай паузу")
    blank()
    add(f"**Вопрос:** {pause_q}")
    blank()
    add("### Проверка")
    blank()
    add("**PowerShell (Windows):**")
    blank()
    add("```powershell")
    add(ps_check.rstrip())
    add("```")
    blank()
    add("<details><summary>Bash (macOS / Linux)</summary>")
    blank()
    add("```bash")
    add(bash_check.rstrip())
    add("```")
    blank()
    add("</details>")
    blank()
    add("### Если сломалось")
    blank()
    add(broken)
    blank()
    add("### Микро-итог")
    blank()
    add(itog)
    blank()
    add("### Дальше")
    blank()
    add(dalshe)
    blank()
    add("---")
    blank()

def svodka_file(title, code, lang="java"):
    add(f"### Сверка: файл целиком — `{title}`")
    blank()
    add(f"```{lang}")
    add(code.rstrip())
    add("```")
    blank()

# ===================== HEADER =====================
add("# T04_08 v2 — Часть 1: Пролог + Этап A + Этап B")
blank()
add("> **Самодостаточный мега-туториал (часть 1 из 2).** Пиши код **здесь**, по микро-шагам. Не подглядывай в готовый проект, пока не закроешь блок «Проверка».")
add(f"> **Рабочая папка:** `{PROJECT}`")
add("> **Углубиться в теорию (опционально):** [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md)")
blank()
add("Привет! Ты собираешь **крестики-нолики** как настоящий backend: Spring Boot, PostgreSQL, Basic Auth, PvE с Minimax и PvP с лобби. **Часть 1** доводит тебя от пустой папки до **работающего T03 в памяти** — один эндпоинт `POST /game/{uuid}`, компьютер отвечает умным ходом.")
blank()
add("**Правило одного шага:** не открывай следующий блок, пока текущий не прошёл «Проверку». Сломалось — смотри «Если сломалось», не прыгай через три файла.")
blank()
add("**Формат v2:** в каждом блоке сначала теория, потом картина в голове, потом микро-шаги с **короткими** вставками кода (5–20 строк), и только в конце — **полный файл** для сверки.")
blank()
add("---")
blank()

# ===================== PROLOGUE =====================
add("# Пролог — зачем всё это и куда мы идём")
blank()

theory_paragraphs([
    "**HTTP** — язык, на котором браузер и сервер разговаривают. Клиент шлёт **запрос**: метод (`GET`, `POST`, …), URL (`http://localhost:8080/game/...`), заголовки (`Content-Type: application/json`) и иногда **тело** (body) — текст или байты. Сервер отвечает **статусом** (`200 OK`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`) и своим телом. Ты не «вызываешь функцию» напрямую — ты отправляешь сообщение по сети и ждёшь ответ.",
    "Для backend-разработчика важно различать **идемпотентность** и **безопасность** методов. `GET` должен только читать данные и не менять состояние на сервере. `POST` создаёт или изменяет ресурс — каждый вызов может дать новый результат. В T03 у нас один `POST /game/{uuid}`: клиент присылает **целую доску** после своего хода, сервер валидирует, считает ответ компьютера и возвращает обновлённую игру.",
    "**REST** (Representational State Transfer) — стиль проектирования API поверх HTTP. Ресурс — «игра», «пользователь» — имеет URL. Состояние передаётся **представлением** (representation), чаще всего JSON. Хороший REST предсказуем: коды ответов честные, ошибки в едином формате (`ErrorResponse`), идентификаторы в пути (`/game/{gameId}`) совпадают с телом запроса.",
    "**JSON** (JavaScript Object Notation) — текстовый формат обмена данными. Spring Boot с библиотекой **Jackson** автоматически превращает JSON в Java-объекты (DTO) и обратно. Вложенность в JSON соответствует полям: `board.board` — это поле `board` внутри объекта `board` в `CurrentGameDto`. Пустые конструкторы и геттеры/сеттеры в DTO нужны именно для Jackson.",
    "**Слои архитектуры** защищают проект от хаоса. **web** знает про HTTP и DTO, но не про Minimax и не про SQL. **domain** знает правила игры и интерфейсы сервисов, но не знает про Tomcat. **datasource** реализует хранение и алгоритмы, связывая domain с памятью (позже — с PostgreSQL). **di** (dependency injection) собирает граф объектов: кто кому передаётся в конструктор.",
    "Представь конвейер одного запроса T03: `GameController` принимает JSON → `GameWebMapper` делает `CurrentGame` → `GameService.validateBoard` сверяет с сохранённым → `GameService.getNextMove` запускает Minimax → результат маппится в DTO → Jackson отдаёт JSON клиенту. Параллельно `GameRepository.save` кладёт игру в `GameStorage`. Ни один слой не делает чужую работу.",
    "**Дорожная карта всего T04** (часть 1 покрывает только начало): **Этап A** — JDK, Gradle, первый `bootRun`. **Этап B** — T03 в RAM (~20 блоков). **Этап C** — PostgreSQL + JPA (часть 2). **Этап D** — регистрация и Basic Auth. **Этап E** — PvP, лобби, все эндпоинты. **Этап F** — полные сценарии curl. **Этап G** — браузерный UI. Не торопись: каждый этап — отдельная «версия продукта».",
])

kartina([
    "```",
    "Клиент (curl / браузер)",
    "        |  HTTP + JSON",
    "        v",
    "   [ web: Controller, DTO, Mapper ]",
    "        |  вызовы интерфейсов",
    "        v",
    "   [ domain: GameBoard, GameService ]",
    "        |  реализация",
    "        v",
    "   [ datasource: GameServiceImpl, Repository, Storage ]",
    "        |",
    "        v",
    "   RAM (позже PostgreSQL)",
    "```",
    "Твоя задача в части 1 — пройти путь сверху вниз, пока нижний ящик — это `ConcurrentHashMap`, а не база данных.",
])

add("### Карта архитектуры (mermaid)")
blank()
add("```mermaid")
add("flowchart TB")
add("    subgraph Web[\"web — HTTP\"]")
add("        GC[GameController]")
add("        DTO[DTO + GameWebMapper]")
add("    end")
add("    subgraph Domain[\"domain — правила\"]")
add("        GS[GameService]")
add("        CG[CurrentGame / GameBoard]")
add("    end")
add("    subgraph DS[\"datasource — хранение\"]")
add("        GSI[GameServiceImpl]")
add("        REPO[GameRepository]")
add("        STOR[GameStorage]")
add("    end")
add("    Client((curl / UI)) --> GC")
add("    GC --> GS")
add("    GS --> GSI")
add("    GSI --> REPO")
add("    REPO --> STOR")
add("```")
blank()
add("### Команды по умолчанию")
blank()
add("Перед каждым запуском сервера:")
blank()
add("```powershell")
add(f"cd {PROJECT}")
add('$env:JAVA_HOME = "C:\\Program Files\\Java\\jdk-21"   # путь к твоему JDK 17–21')
add(".\\gradlew.bat bootRun")
add("```")
blank()
add("<details><summary>Bash (macOS / Linux)</summary>")
blank()
add("```bash")
add("cd src/TicTacToe_1.2_sql_auth")
add("export JAVA_HOME=$(/usr/libexec/java_home -v 21)")
add("./gradlew bootRun")
add("```")
blank()
add("</details>")
blank()
add("---")
blank()

# Theory before Stage A
add("# Теория перед Этапом A — JDK, Gradle, Spring Boot")
blank()
theory_paragraphs([
    "**JDK** (Java Development Kit) — компилятор `javac`, runtime `java`, стандартная библиотека. Spring Boot 3 требует **Java 17+**. На School21 часто стоит Java 26 — она слишком новая для Gradle/Spring в этом проекте. Выставляй `JAVA_HOME` на **17 или 21** (Eclipse Temurin — хороший выбор).",
    "**Gradle** — система сборки. Файл `build.gradle.kts` (Kotlin DSL) описывает плагины, зависимости, версию Java. Wrapper (`gradlew.bat` / `gradlew`) фиксирует версию Gradle в проекте — не нужно ставить Gradle глобально. Команды: `bootRun` (запуск), `compileJava` (только компиляция), `dependencies` (дерево библиотек).",
    "**Spring Boot** — надстройка над Spring Framework: встраивает Tomcat, автоконфигурирует Jackson, поднимает контекст приложения. Аннотация `@SpringBootApplication` на `TicTacToeApplication` включает сканирование пакета `tictactoe` и всех вложенных. Точка входа — `main`, который вызывает `SpringApplication.run`.",
    "На этапе A мы подключаем только `spring-boot-starter-web` — без JPA, без Security. Этого достаточно, чтобы Tomcat слушал порт **8080** и отвечал на HTTP. Позже, на этапе C, добавишь `data-jpa` и драйвер PostgreSQL — Gradle подтянет новые jar-файлы после Reload.",
    "Связка **JDK + Gradle + Spring Boot** — фундамент. Если JDK неверный, Gradle даже не стартует. Если `build.gradle.kts` битый — `bootRun` не найдёт плагин. Если нет `@SpringBootApplication` — контекст пустой. Этап A проверяет все три звена по отдельности, чтобы на этапе B ты думал о логике игры, а не о среде.",
])
add("---")
blank()

generate_stage_a(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer)
generate_theory_before_b(add, blank, theory_paragraphs)
generate_stage_b(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer)
generate_padding(add, blank, PROJECT)

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
file_lines = sum(1 for _ in open(OUT, encoding="utf-8"))
print(f"Generated {OUT} — {file_lines} lines ({len(lines)} logical blocks)")
