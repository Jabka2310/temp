# -*- coding: utf-8 -*-
"""Generator for T04_08 v2 — progressive code + theory."""
from pathlib import Path

OUT = Path(r"b:\school21\temp\AP1OLD\T04_08_РАЗРАБОТКА_ПОСТРОЧНО.md")
PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"

def ms(n, title, add, code, rows, check=""):
    """Micro-step block."""
    table = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows)
    chk = f"\n**Мини-проверка:** {check}\n" if check else ""
    return f"""
### Микро-шаг {n} — {title}

**Добавляем:** {add}

**Напиши:**

```{code.split(chr(10))[0][:3] if code else 'text'}
{code.strip()}
```

**Разбор:**

| Строка / фрагмент | Код | Что происходит |
|------------------|-----|----------------|
{table}
{chk}
"""

def block(title, goal, time, diff, theory, picture, micro_steps, full_code, lang, pause, verify_ps, verify_bash, troubles, summary, nxt):
    steps = "".join(micro_steps)
    return f"""
## {title}

| | |
|---|---|
| **Цель** | {goal} |
| **Время** | {time} |
| **Сложность** | {diff} |

### Теория (прочитай до кода)

{theory}

### Картина в голове

{picture}
{steps}
### Сверка: файл целиком

> Сравни свой результат. Если совпадает — блок закрыт.

```{lang}
{full_code.strip()}
```

### Сделай паузу

{pause}

### Проверка

**PowerShell (Windows):**
```powershell
{verify_ps.strip()}
```

<details><summary>Bash (macOS / Linux)</summary>

```bash
{verify_bash.strip()}
```

</details>

### Если сломалось

{troubles}

### Микро-итог

{summary}

### Дальше

{nxt}

---
"""

parts = []

parts.append(f"""# T04 — Разработка построчно v2: постепенный код + теория

> **Формат v2:** код **наращивается микро-шагами**. Полный файл — только в секции **«Сверка»** в конце блока.  
> **Рабочая папка:** `{PROJECT}`  
> **Не подглядывай** в готовый проект до «Проверки» блока.  
> **Теория глубже:** опционально [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md)

---

## Как читать этот файл (v2)

1. **Теория** — читаешь *до* кода. Это карта местности.
2. **Микро-шаги** — пишешь в IDE **только то, что указано**, сохраняешь, идёшь дальше.
3. **Сверка** — в конце блока сверяешь полный файл.
4. **Проверка** — команда в терминале. Не работает → «Если сломалось».

**Правило:** один микро-шаг = одна маленькая победа. Не перескакивай.

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

## Пролог: что мы строим и как это работает

### Теория — HTTP и REST за 5 минут

**Клиент** (браузер, curl, Postman) шлёт **HTTP-запрос**:
```
POST /game/550e8400-... HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Authorization: Basic YWxpY2U6c2VjcmV0=

{{"board": {{"board": [[0,1,0],[0,0,0],[0,0,0]]}}}}
```

**Сервер** (Spring Boot + Tomcat) отвечает **HTTP-ответом**:
```
HTTP/1.1 200 OK
Content-Type: application/json

{{"id":"550e8400-...","state":"PLAYER_TURN",...}}
```

| Часть запроса | Значение |
|---------------|----------|
| `POST` | метод — «создай / измени» |
| `/game/{uuid}` | путь (URL) — какой ресурс |
| Заголовки | метаданные: тип тела, авторизация |
| Тело | JSON — данные |

**REST** — стиль API: ресурсы (`/game`, `/user`) + HTTP-методы (GET читать, POST создавать/действовать). Не путай с «REST = только JSON» — это про **адреса и глаголы**.

**JSON** — текстовый формат обмена. Java-объект ↔ JSON делает **Jackson** (входит в `spring-boot-starter-web`).

### Теория — зачем три слоя

```mermaid
flowchart LR
    HTTP[HTTP JSON] --> Web
    Web --> Domain
    Domain --> DS[datasource]
    DS --> DB[(PostgreSQL)]
```

| Слой | Знает | Не знает |
|------|-------|----------|
| **web** | HTTP, DTO | SQL, правила победы |
| **domain** | правила игры | PostgreSQL, `@Entity` |
| **datasource** | JPA, маппинг | `@PostMapping` |

Если смешать — через месяц не найдёшь, где баг: в SQL или в Minimax.

### Дорожная карта A → G

| Этап | Что появится | Зачем |
|------|--------------|-------|
| A | Spring Boot стартует | фундамент |
| B | PvE в памяти | логика игры + Minimax |
| C | PostgreSQL | данные переживают рестарт |
| D | Auth | знаем *кто* ходит |
| E | PvP | два человека онлайн |
| F | curl | проверка без UI |
| G | HTML/JS | игра глазами |

---

## Команды (Windows)

```powershell
cd {PROJECT}
java -version   # 17–21, не 26
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
""")

# --- STAGE A THEORY ---
parts.append("""
# ЭТАП A — Среда и первый запуск

## Теория этапа A — JDK, Gradle, Spring Boot

**JDK** (Java Development Kit) — компилятор + runtime. **JRE** — только запуск. Для разработки нужен JDK.

**Gradle** — система сборки. Читает `build.gradle.kts`, скачивает библиотеки (Spring, PostgreSQL…), компилирует, запускает `bootRun`.

**Spring Boot** — «батарейки в комплекте»:
- встроенный **Tomcat** на порту **8080**;
- **autoconfiguration** — видит JPA на classpath → настраивает DataSource;
- `@SpringBootApplication` — точка сканирования компонентов.

**Почему не Java 26?** Gradle/Kotlin DSL Spring Boot 3.2 может падать с `* What went wrong: 26.0.1`. Используй **17–21**.

---
""")

# Block A.1
parts.append(block(
    "Блок A.1 — JDK и рабочая папка",
    "Убедиться, что Java 17–21 и ты в правильной директории.",
    "15 мин", "★☆☆",
    """Перед кодом — **среда**. School21 проверяет проект через Gradle; Gradle вызывает `javac` из `JAVA_HOME`.

Если `java -version` показывает **26** — это часто системная Java, не та, что в IntelliJ. Gradle возьмёт не ту версию → загадочная ошибка.

**IntelliJ:** File → Settings → Build Tools → Gradle → **Gradle JVM = 21**.

Рабочая папка — **`src/TicTacToe_1.2_sql_auth`**, не корень репозитория. Там лежит `gradlew`.""",
    "Ты ещё не пишешь Java. Только проверяешь окружение — как `npm install` перед React.",
    [
        ms(1, "Перейди в проект", "cd в папку с gradlew.",
           "powershell\n# уже в PowerShell",
           [("1", f"cd {PROJECT}", "переход в проект")],
           "`dir gradlew.bat` — файл есть"),
        ms(2, "Проверь Java", "Версия JDK.",
           "powershell\njava -version",
           [("1", "java -version", "должно быть 17.x или 21.x")],
           "Не 26.x"),
    ],
    "# Нет файла — только команды терминала",
    "text",
    "**Вопрос:** Почему `gradlew` запускают из папки проекта, а не из корня git?",
    f"cd {PROJECT}\ndir gradlew.bat\njava -version",
    f"cd {PROJECT} && ls gradlew && java -version",
    "| Симптом | Решение |\n|---------|----------|\n| `gradlew not found` | Неверная папка |\n| `26.0.1` | Gradle JVM → 21 |",
    "- JDK 17–21\n- Правильная папка\n- Gradle wrapper на месте",
    "**Блок A.2** — создадим дерево пакетов."
))

print("Generating...", OUT)
OUT.write_text("".join(parts), encoding="utf-8")
print("Lines:", len(OUT.read_text(encoding='utf-8').splitlines()))
