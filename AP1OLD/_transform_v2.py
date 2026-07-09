# -*- coding: utf-8 -*-
"""Transform T04_08 v1 -> v2 progressive format."""
import re
from pathlib import Path

SRC = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
BAK = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО_v1_backup.md")
OUT = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"

STAGE_THEORY = {
    "A": """
## Теория этапа A — JDK, Gradle, Spring Boot

**JDK** — компилятор + runtime. **Gradle** читает `build.gradle.kts`, качает Spring, запускает `bootRun`.

**Spring Boot** поднимает **Tomcat :8080**, включает **Jackson** (JSON) и **autoconfiguration**.

Используй **Java 17–21**. Java 26 ломает Gradle с ошибкой `* What went wrong: 26.0.1`.

**IntelliJ:** Gradle JVM = 21 (Settings → Build Tools → Gradle).
""",
    "B": """
## Теория этапа B — Domain, DTO, Repository, Minimax

**Domain-модель** (`GameBoard`, `CurrentGame`) — правила игры. Без `@Entity`, без JSON-аннотаций.

**DTO** (этап B позже) — «форма для HTTP». Клиент шлёт JSON → DTO → domain.

**Repository** — «ящик» для сохранения. В T03 — `ConcurrentHashMap`; в T04 — PostgreSQL.

**validateBoard** — анти-чит: клиент не может переписать старую клетку.

**Minimax** — компьютер перебирает все варианты до конца партии и выбирает оптимальный ход.

```mermaid
flowchart TB
    Client --> Controller
    Controller --> Service
    Service --> Repository
    Repository --> Memory[(GameStorage T03)]
```
""",
    "C": """
## Теория этапа C — SQL, JDBC, JPA, Hibernate

**PostgreSQL** хранит строки в **таблицах**. `games` — одна строка = одна партия.

**JDBC** — низкоуровневый Java→SQL. **JPA** — описываешь классы с `@Entity`, Hibernate генерирует SQL.

| Аннотация | Смысл |
|----------|-------|
| `@Entity` | класс = таблица |
| `@Embeddable` | кусок, встраивается в другую таблицу |
| `@Embedded` | поле-объект → колонки `cell_00`… |

`ddl-auto=update` — Hibernate **сам** создаёт/обновляет таблицы (для учебного проекта OK).

**Удаляем** `GameStorage` и `GameRepositoryImpl` — Spring Data генерирует реализацию интерфейса.
""",
    "D": """
## Теория этапа D — Auth: кто ты?

| Термин | Смысл |
|--------|-------|
| **Идентификация** | кто ты (login) |
| **Аутентификация** | докажи паролем |
| **Авторизация** | что тебе можно |

**Basic Auth (RFC 7617):** заголовок `Authorization: Basic base64(login:password)`.

Пример: `alice:secret` → Base64 → `YWxpY2U6c2VjcmV0`.

**AuthFilter** — страж у двери: нет валидного Basic → **401**, контроллер не вызывается.

**401 vs 403:** 401 = «не представился», 403 = «представился, но нельзя». Мы возвращаем 401.

```mermaid
sequenceDiagram
    participant C as Client
    participant F as AuthFilter
    participant S as AuthService
    C->>F: POST /game + Basic
    F->>S: decode + authenticate
    S-->>F: UUID or null
    alt ok
        F->>C: controller
    else fail
        F->>C: 401
    end
```
""",
    "E": """
## Теория этапа E — State machine и PvP

Игра — **конечный автомат**:

```mermaid
stateDiagram-v2
    [*] --> WAITING_FOR_PLAYERS: create PvP
    WAITING_FOR_PLAYERS --> PLAYER_TURN: join
    [*] --> PLAYER_TURN: create PvE
    PLAYER_TURN --> WIN: 3 в ряд
    PLAYER_TURN --> DRAW: поле полное
```

**Lobby:** `GET /game/available` → игры в `WAITING_FOR_PLAYERS`.

**Turn-based:** `currentTurnPlayerId` — только этот UUID может POST ход.

**PvE vs PvP в makeMove:** если `vsComputer` — после игрока Minimax; иначе — смена очереди.
""",
    "F": """
## Теория этапа F — curl как ручной интеграционный тест

**curl** имитирует HTTP-клиент. Проверяешь API без UI.

| Флаг | Значение |
|------|----------|
| `-X POST` | метод |
| `-H "Authorization: Basic ..."` | auth |
| `-d '{...}'` | тело JSON |
| `-w "%{http_code}"` | только код ответа |

Сценарий = цепочка: register → login → create → move → get.
""",
    "G": """
## Теория этапа G — Static UI + fetch

Spring отдаёт файлы из `src/main/resources/static/` по URL `/`, `/js/...`, `/css/...`.

**sessionStorage** — логин/пароль/`userId` в памяти вкладки.

**fetch + apiFetch** — обёртка добавляет `Authorization: Basic`.

**Optimistic UI** — рисуем X на доске до ответа сервера, откатываем при ошибке.

**Polling (PvP)** — каждые 2 сек `GET /game/{id}` пока ждём соперника.

**CORS** не нужен: UI и API на одном `localhost:8080` (same origin).

Опечатка **`Autorization`** без `h` → вечный 401.
""",
}

BLOCK_THEORY = {
    "GameBoard": "**GameBoard** — value object: доска 3×3. Числа 0/1/2 удобны для JSON `[[0,1,0],...]`. Инкапсуляция: `getCells()` возвращает **копию** — снаружи не испортят массив.",
    "CurrentGame": "**CurrentGame** — aggregate root: id сессии + доска (+ позже игроки). `final` поля → immutable; изменения через **новый** объект.",
    "GameServiceImpl": "**GameServiceImpl** — сердце T03: validateBoard (анти-чит), updateGameState (победа/ничья), Minimax (ход O).",
    "AuthFilter": "**Filter** в servlet-цепочке: до `@RestController`. `chain.doFilter` — пропустить; `return` без chain — стоп.",
    "Minimax": "**Minimax:** MAX (компьютер) хочет +10, MIN (игрок) хочет −10. `depth` — выигрывать быстрее.",
}


def detect_lang(code):
    if code.strip().startswith("package") or "public class" in code[:200]:
        return "java"
    if "plugins {" in code or "fun " in code:
        return "kotlin"
    if code.strip().startswith("<"):
        return "html"
    if "function " in code or "const " in code:
        return "javascript"
    if code.strip().startswith("*") or "body {" in code:
        return "css"
    if "=" in code and "spring." in code:
        return "properties"
    return "text"


def split_code_chunks(code, lang):
    lines = code.split("\n")
    if lang in ("java", "kotlin") and len(lines) >= 8:
        # package + imports
        chunks = []
        i = 0
        header_end = 0
        for j, line in enumerate(lines):
            if line.strip().startswith("public class") or line.strip().startswith("public enum") or line.strip().startswith("public interface"):
                header_end = j
                break
        if header_end > 0:
            chunks.append("\n".join(lines[: header_end + 1]))
            rest = lines[header_end + 1 :]
            # group methods by blank lines or every ~12 lines
            buf, brace = [], 0
            for line in rest:
                buf.append(line)
                brace += line.count("{") - line.count("}")
                if brace == 0 and buf and line.strip() == "}":
                    chunks.append("\n".join(buf))
                    buf = []
            if buf:
                chunks.append("\n".join(buf))
            if len(chunks) >= 2:
                return chunks
    if len(lines) <= 12:
        return [code]
        chunks, current, brace = [], [], 0
        for line in lines:
            current.append(line)
            brace += line.count("{") - line.count("}")
            if brace == 0 and len(current) > 2 and (line.strip() == "}" or line.strip().endswith("}")):
                chunks.append("\n".join(current))
                current = []
        if current:
            if chunks:
                chunks[-1] = chunks[-1] + "\n" + "\n".join(current)
            else:
                chunks = ["\n".join(lines)]
        if len(chunks) >= 2:
            return chunks
    # split by double newline
    parts = re.split(r"\n(?=\n)", code)
    if len(parts) >= 2:
        return [p.strip() for p in parts if p.strip()]
    # split by ~10 lines for progressive feel
    step = 10
    return ["\n".join(lines[i:i+step]) for i in range(0, len(lines), step)]


def chunk_title(i, chunk, lang):
    c = chunk.strip()
    if "package " in c:
        return "package и imports"
    if "public class" in c or "public enum" in c or "public interface" in c:
        return "объявление типа"
    if "public static final" in c:
        return "константы"
    if "private final" in c and "=" not in c.split("private final")[1][:30]:
        return "поля"
    if "public " in c and "(" in c and ")" in c and "{" in c:
        m = re.search(r"public [\w<>\[\],\s]+\s+(\w+)\s*\(", c)
        return f"метод `{m.group(1)}()`" if m else f"метод {i}"
    if "@Override" in c:
        return f"override-метод {i}"
    if lang == "kotlin" and "dependencies" in c:
        return "зависимости Gradle"
    return f"фрагмент {i}"


def make_micro_steps(code, lang):
    chunks = split_code_chunks(code, lang)
    steps = []
    accumulated = []
    for i, ch in enumerate(chunks, 1):
        accumulated.append(ch)
        title = chunk_title(i, ch, lang)
        rows = []
        for j, line in enumerate(ch.split("\n")[:8], 1):
            if line.strip():
                rows.append((str(j), f"`{line.strip()[:60]}`", "см. комментарий в коде"))
        if not rows:
            rows = [("—", "…", "добавь фрагмент")]
        table = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows)
        steps.append(f"""
### Микро-шаг {i} — {title}

**Добавляем:** очередной фрагмент файла (не переписывай уже написанное — **дописываешь**).

**Напиши:**

```{lang}
{ch.strip()}
```

**Разбор:**

| № | Строка | Смысл |
|---|--------|-------|
{table}

""")
    return "".join(steps)


def extract_goal(block_text):
    m = re.search(r"\*\*Цель\*\*\s*\|\s*(.+?)\s*\|", block_text)
    return m.group(1).strip() if m else "См. название блока"


def transform_block(block_text):
    block_text = block_text.lstrip("\r\n")
    title_m = re.match(r"## (Блок .+?)\r?\n", block_text)
    if not title_m:
        return block_text
    title = title_m.group(1)

    # extract goal table row
    goal = extract_goal(block_text)
    time_m = re.search(r"\*\*Время\*\*\s*\|\s*(.+?)\s*\|", block_text)
    diff_m = re.search(r"\*\*Сложность\*\*\s*\|\s*(.+?)\s*\|", block_text)
    time_v = time_m.group(1).strip() if time_m else "20 мин"
    diff_v = diff_m.group(1).strip() if diff_m else "★★☆"

    # theory from Зачем
    z_m = re.search(r"### Зачем\r?\n\r?\n(.+?)(?=\r?\n### )", block_text, re.S)
    zachem = z_m.group(1).strip() if z_m else ""
    extra = ""
    for key, txt in BLOCK_THEORY.items():
        if key in title:
            extra = txt + "\n\n"
            break

    theory = extra + zachem
    if len(theory) < 80:
        theory = extra + "Этот файл — следующий кирпич в слоистой архитектуре. Прочитай **Картину в голове**, потом пиши микро-шаги."

    pic_m = re.search(r"### Перед тем как писать\r?\n+(.+?)(?=\r?\n### Напиши)", block_text, re.S)
    picture = pic_m.group(1).strip() if pic_m else "Дополняешь проект по микро-шагам."

    # main code block under ### Напиши
    code_m = re.search(r"### Напиши[\s\S]*?```(\w*)\r?\n([\s\S]*?)```", block_text)
    if not code_m:
        return block_text  # leave as-is (F blocks etc.)

    lang = code_m.group(1).strip() or detect_lang(code_m.group(2))
    code = code_m.group(2).strip()
    micro = make_micro_steps(code, lang)

    pause_m = re.search(r"### Сделай паузу\r?\n\r?\n(.+?)(?=\r?\n### )", block_text, re.S)
    pause = pause_m.group(1).strip() if pause_m else "**Вопрос:** зачем этот файл в своём слое?"

    verify_m = re.search(r"### Проверка\r?\n\r?\n(.+?)(?=\r?\n### |\r?\n---|\Z)", block_text, re.S)
    verify = verify_m.group(1).strip() if verify_m else "`.\\gradlew.bat compileJava`"

    trouble_m = re.search(r"### Если сломалось\r?\n\r?\n(.+?)(?=\r?\n### )", block_text, re.S)
    trouble = trouble_m.group(1).strip() if trouble_m else "Перечитай разбор микро-шагов."

    summary_m = re.search(r"### Микро-итог\r?\n\r?\n(.+?)(?=\r?\n### |\r?\n---|\Z)", block_text, re.S)
    summary = summary_m.group(1).strip() if summary_m else "- Файл готов\n- Компиляция OK"

    return f"""## {title}

| | |
|---|---|
| **Цель** | {goal} |
| **Время** | {time_v} |
| **Сложность** | {diff_v} |

### Теория (прочитай до кода)

{theory}

### Картина в голове

{picture}

{micro}
### Сверка: файл целиком

> Сравни свой файл с эталоном. Расхождения — только осознанные.

```{lang}
{code}
```

### Сделай паузу

{pause}

### Проверка

{verify}

### Если сломалось

{trouble}

### Микро-итог

{summary}

---
"""


def main():
    text = BAK.read_text(encoding="utf-8") if BAK.exists() else SRC.read_text(encoding="utf-8")

    # New header
    header = f"""# T04 — Разработка построчно v2: постепенный код + теория

> **Формат v2:** код **наращивается микро-шагами**. Полный файл — только в **«Сверка: файл целиком»**.  
> **Рабочая папка:** `{PROJECT}`  
> **Не подглядывай** в готовый проект до «Проверки» блока.  
> **Теория глубже:** [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md)

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

## Пролог: HTTP, REST, JSON, слои

### Теория — что происходит при `POST /game/{{id}}`

Клиент шлёт **HTTP-запрос** (метод + URL + заголовки + тело). Сервер отвечает **статусом** (200, 401…) + JSON.

| Часть | Пример |
|-------|--------|
| Метод | `POST` — действие |
| URL | `/game/uuid` — ресурс |
| `Authorization` | `Basic base64(login:password)` |
| Тело | `{{"board":{{"board":[[0,1,0],...]}}}}` |

**REST** — ресурсы + HTTP-методы. **JSON** — текстовый обмен; Jackson маппит в Java-объекты.

### Теория — три слоя

```mermaid
flowchart TB
    subgraph web [web]
        C[Controllers + DTO]
        F[AuthFilter]
    end
    subgraph domain [domain]
        S[GameService interface]
        M[GameBoard / CurrentGame]
    end
    subgraph ds [datasource]
        I[GameServiceImpl]
        R[Repository + Entity]
    end
    HTTP((HTTP)) --> F --> C --> S --> I --> R --> DB[(PostgreSQL)]
```

**web** не знает SQL. **domain** не знает HTTP. **datasource** — мост к БД.

### Дорожная карта

| Этап | Результат |
|------|-----------|
| A | Spring Boot на :8080 |
| B | PvE + Minimax в памяти |
| C | PostgreSQL |
| D | Basic Auth |
| E | PvP + lobby |
| F | curl-тесты |
| G | UI в браузере |

---

## Команды (Windows)

```powershell
cd {PROJECT}
java -version
.\\gradlew.bat bootRun
```

<details><summary>Bash</summary>

```bash
cd src/TicTacToe_1.2_sql_auth
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
./gradlew bootRun
```

</details>

---

"""

    # Keep diagrams from original between prolog and stage A if present
    diagram_section = ""
    for name in ["Карта архитектуры", "Поток авторизации", "Машина состояний", "Minimax"]:
        m = re.search(rf"## {name}.*?(?=\n---|\n# ЭТАП A)", text, re.S)
        if m:
            diagram_section += m.group(0).strip() + "\n\n---\n\n"

    out_parts = [header, diagram_section]

    # Split by stage
    stage_splits = re.split(r"(# ЭТАП [A-G] —[^\n]+\n)", text)
    # first chunk is old header - skip
    i = 1
    while i < len(stage_splits):
        stage_header = stage_splits[i]
        stage_body = stage_splits[i + 1] if i + 1 < len(stage_splits) else ""
        stage_key = stage_header[8]  # letter after "ЭТАП "
        if stage_key in STAGE_THEORY:
            out_parts.append(STAGE_THEORY[stage_key] + "\n")
        out_parts.append(stage_header)

        # split blocks
        blocks = re.split(r"(?=\n## Блок )", stage_body)
        for b in blocks:
            if b.strip().startswith("## Блок"):
                out_parts.append(transform_block(b))
            elif b.strip():
                out_parts.append(b)
        i += 2

    # Epilog from original
    ep = re.search(r"## Частые ошибки.*", text, re.S)
    if ep:
        out_parts.append("\n" + ep.group(0))

    result = "".join(out_parts)
    # Fix duplicate v1 headers if any
    result = re.sub(r"# T04 — Разработка построчно: от пустой папки.*?(?=## Оглавление|---)", "", result, count=1, flags=re.S)
    OUT.write_text(result, encoding="utf-8")
    print("Written", OUT, "lines:", len(result.splitlines()))


if __name__ == "__main__":
    main()
