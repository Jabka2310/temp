# -*- coding: utf-8 -*-
"""Block definitions for T04_08 v2 Part 1 generator."""
from _gen_t04_08_v2_codes import *

PROJECT = r"B:\school21\Java\Backend\AP1_Jv_T04B.ID_1421426-1\src\TicTacToe_1.2_sql_auth"


def _lang(code: str) -> str:
    s = code.strip()
    if s.startswith("package") or s.startswith("import org.") or s.startswith("public class"):
        return "java"
    if s.startswith("plugins") or s.startswith("rootProject"):
        return "kotlin"
    if s.startswith("$") or s.startswith("cd ") or s.startswith(".\\") or s.startswith("Invoke"):
        return "powershell"
    if s.startswith("export") or s.startswith("./") or s.startswith("GAME_ID"):
        return "bash"
    if s.startswith("server.") or s.startswith("#"):
        return "properties"
    return "text"


def emit_block(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
               block_id, title, goal, time, diff, theory, picture, steps, full_name, full_code, full_lang,
               pause, ps, bash, broken, itog, dalshe, extra_theory=None):
    add(f"## Блок {block_id} — {title}")
    blank()
    table_goal(goal, time, diff)
    theory_paragraphs(theory + (extra_theory or []))
    kartina(picture)
    for i, step in enumerate(steps, 1):
        micro_step(i, step[0], step[1], step[2], step[3])
    lang = full_lang or _lang(full_code)
    svodka_file(full_name, full_code, lang)
    block_footer(pause, ps, bash, broken, itog, dalshe)


def _pad_theory(topic: str, n: int = 4) -> list[str]:
    templates = [
        f"Когда будешь отлаживать **{topic}**, держи в голове один вопрос: «какой слой за это отвечает?» Если ошибка в JSON — смотри web/DTO. Если в логике хода — domain/service. Если «игра не сохранилась» — repository/storage.",
        f"На защите проекта часто спрашивают про **{topic}** не «что написано в коде», а «зачем так». Ответ всегда про разделение ответственности: меньше связей — проще тестировать и менять БД без переписывания контроллера.",
        f"Типичная ловушка с **{topic}**: скопировать готовый файл целиком и не понять половину строк. Формат v2 как раз против этого — сначала 5–20 строк, разбор, потом сверка. Не пропускай микро-шаги даже если «и так понятно».",
        f"Сравни **{topic}** с монолитом «всё в одном Main.java»: там бы HTTP, массив int[][] и SQL в одной куче. Слои дороже по файлам, но дешевле по нервам при T04, когда добавятся Postgres, Security и PvP.",
        f"Если застрял на **{topic}** больше 30 минут — остановись, прочитай «Картину в голове» ещё раз, ответь на вопрос в «Сделай паузу» вслух. Часто проблема не в синтаксисе Java, а в неверном пакете или пропущенном `@Bean`.",
        f"Запиши в тетрадь одну фразу про **{topic}** своими словами. Если не можешь — вернись к теории блока, не к Google. Этот навык важнее, чем идеальная первая компиляция.",
    ]
    return templates[:n]


def generate_stage_a(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer):
    add("# ЭТАП A — Среда и первый запуск")
    blank()
    add("> Цель этапа: JDK на месте, пакеты созданы, Gradle тянет Spring Web, Tomcat слушает 8080. Кода игры пока нет — и это нормально.")
    blank()

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "A.1", "JDK и проверка Java",
        "Убедиться, что Gradle видит JDK 17–21, не 26.",
        "5 мин", "★☆☆",
        [
            "**JDK** (Java Development Kit) — это не только команда `java`, а весь набор: компилятор, runtime, стандартная библиотека. Gradle при сборке вызывает `javac` из `$JAVA_HOME`. Если там Java 26, а Spring Boot 3.2 рассчитан на 17–21, получишь загадочные ошибки плагинов.",
            "Переменная **`JAVA_HOME`** указывает на корень установки JDK (папка с `bin/java`). На Windows в PowerShell её задают на сессию: `$env:JAVA_HOME = \"...\"`. Это не ломает систему навсегда — только текущее окно терминала.",
            "School21 часто ставит несколько JDK. **Правило:** перед `./gradlew bootRun` всегда проверяй `java -version`. Нужно увидеть `17` или `21`. Строка `26` — стоп, смени JDK.",
            "Eclipse Temurin (Adoptium) — удобный бесплатный JDK. IntelliJ тоже может скачать JDK 21 в Settings → Build Tools → Gradle → Gradle JVM.",
        ],
        ["```", "Терминал → JAVA_HOME → java -version → Gradle → Spring Boot", "Если первое звено битое — дальше не едет.", "```"],
        [
            ("Путь к JDK", "Проверь, что папка существует и внутри есть `bin\\java.exe`.",
             f'$env:JAVA_HOME = "C:\\Program Files\\Java\\jdk-21"\nTest-Path "$env:JAVA_HOME\\bin\\java.exe"',
             [("1", "$env:JAVA_HOME", "Путь к корню JDK"), ("2", "Test-Path", "Проверка наличия java.exe")]),
            ("Версия Java", "Запусти java из JAVA_HOME — не из случайного PATH.",
             f'& "$env:JAVA_HOME\\bin\\java.exe" -version',
             [("1", "java.exe -version", "Печатает версию JVM"), ("2", "openjdk 21", "Ожидаемый результат")]),
            ("Gradle JVM", "Gradle должен использовать тот же JDK (позже в IDE).",
             f"cd {PROJECT}\n.\\gradlew.bat -version",
             [("1", "gradlew -version", "Показывает JVM Gradle"), ("2", "Launcher JVM", "Должна совпасть с JAVA_HOME")]),
        ],
        "commands-jdk-check.ps1",
        f'$env:JAVA_HOME = "C:\\Program Files\\Java\\jdk-21"\n& "$env:JAVA_HOME\\bin\\java.exe" -version',
        "powershell",
        "Почему именно JAVA_HOME, а не просто java в PATH?",
        f'$env:JAVA_HOME = "C:\\Program Files\\Java\\jdk-21"\n& "$env:JAVA_HOME\\bin\\java.exe" -version',
        "java -version",
        "Версия 26.x → установи JDK 21, выставь JAVA_HOME. `java` не найден → добавь `%JAVA_HOME%\\bin` в PATH или вызывай полный путь.",
        "Java под контролем — полдела с Gradle.",
        "Блок **A.2** — структура пакетов.",
        _pad_theory("JDK", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "A.2", "Структура пакетов",
        "Создать дерево пакетов до первого `.java`.",
        "10 мин", "★☆☆",
        [
            "В Java **пакет** — это namespace и одновременно папка под `src/main/java`. Класс `tictactoe.domain.model.GameBoard` лежит в `tictactoe/domain/model/GameBoard.java`.",
            "Мы делим код на **слои**: `domain` (правила), `datasource` (хранение и реализация), `web` (HTTP), `di` (сборка Spring-бинов). Это не требование Java — это дисциплина архитектуры.",
            "Spring Boot сканирует компоненты начиная с пакета `@SpringBootApplication` — у нас `tictactoe`. Все подпакеты `tictactoe.*` попадают в контекст. Если положить контроллер в `com.other` без `@ComponentScan` — Spring его не увидит.",
            "Создавай пакеты **до** классов: в IntelliJ ПКМ → New → Package, вводи полное имя `tictactoe.domain.model`.",
        ],
        ["```", "src/main/java/tictactoe/", "  domain/   web/   datasource/   di/", "```"],
        [
            ("Корень", "Пакет приложения — `tictactoe`.",
             "tictactoe",
             [("—", "tictactoe", "Корень; Spring сканирует отсюда")]),
            ("Domain", "Бизнес-модели и интерфейсы сервисов.",
             "tictactoe.domain.model\ntictactoe.domain.service",
             [("—", "domain.model", "GameBoard, CurrentGame"), ("—", "domain.service", "GameService interface")]),
            ("Datasource + Web + DI", "Остальные слои — по одному пакету на роль.",
             "tictactoe.datasource.model\ntictactoe.datasource.repository\ntictactoe.datasource.mapper\ntictactoe.datasource.service\ntictactoe.datasource.storage\ntictactoe.web.controller\ntictactoe.web.model\ntictactoe.web.mapper\ntictactoe.di",
             [("—", "datasource.*", "Entity, repo, storage, impl"), ("—", "web.*", "Controller, DTO"), ("—", "di", "SpringConfig @Bean")]),
        ],
        "структура пакетов", PACKAGES, "text",
        "Зачем `GameBoard` в domain, а не в web?", "# дерево папок как выше", "# ls -R src/main/java/tictactoe",
        "IntelliJ не создаёт вложенные пакеты одним именем — пиши полное имя `tictactoe.domain.model`.",
        "Скелет пакетов готов — наполняем на этапе B.",
        "Блок **A.3** — `build.gradle.kts`.",
        _pad_theory("пакеты", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "A.3", "`build.gradle.kts` (только Web)",
        "Подключить Spring Boot Web для T03.",
        "10 мин", "★★☆",
        [
            "**Gradle** описывает сборку декларативно. Файл `build.gradle.kts` — Kotlin DSL (скобки и строки как в Kotlin). Плагин `org.springframework.boot` добавляет задачу `bootRun` и управление версиями Spring.",
            "`spring-boot-starter-web` — **starter**, набор зависимостей: Spring MVC, embedded Tomcat, Jackson для JSON. Одна строка вместо десяти jar вручную.",
            "`sourceCompatibility = VERSION_17` — bytecode 17. Spring Boot 3 не поддерживает Java 8/11.",
            "После правки — **Gradle Reload** в IDE (иконка слона). Без reload IDE может показывать старые зависимости.",
        ],
        ["```", "build.gradle.kts → plugins → dependencies → bootRun", "```"],
        [
            ("Плагины", "Java + Spring Boot 3.2.0 + dependency-management.",
             'plugins {\n    id("java")\n    id("org.springframework.boot") version "3.2.0"\n    id("io.spring.dependency-management") version "1.1.4"\n}',
             [("1-4", "plugins", "Подключают Java и Spring Boot")]),
            ("Java 17", "Минимальная версия для Boot 3.",
             'java {\n    sourceCompatibility = JavaVersion.VERSION_17\n    targetCompatibility = JavaVersion.VERSION_17\n}',
             [("—", "VERSION_17", "Bytecode 17")]),
            ("Web starter", "HTTP API без БД пока.",
             'dependencies {\n    implementation("org.springframework.boot:spring-boot-starter-web")\n    testImplementation(platform("org.junit:junit-bom:5.10.0"))\n    testImplementation("org.junit.jupiter:junit-jupiter")\n}',
             [("—", "starter-web", "Tomcat + MVC + Jackson")]),
            ("JUnit", "Задача test использует JUnit 5.",
             'tasks.test {\n    useJUnitPlatform()\n}',
             [("—", "useJUnitPlatform", "JUnit 5 для тестов")]),
        ],
        "build.gradle.kts", BUILD_GRADLE, "kotlin",
        "Чем `implementation` отличается от `testImplementation`?",
        f"cd {PROJECT}\n.\\gradlew.bat dependencies --configuration compileClasspath | Select-String spring-web",
        "./gradlew dependencies --configuration compileClasspath | grep spring-web",
        "Gradle sync failed → File → Invalidate Caches. Нет gradlew.bat → скопируй wrapper из соседнего проекта.",
        "Gradle знает про Spring Web.",
        "Блок **A.4** — `TicTacToeApplication`.",
        _pad_theory("Gradle", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "A.4", "`TicTacToeApplication.java`",
        "Точка входа Spring Boot.",
        "5 мин", "★☆☆",
        [
            "`@SpringBootApplication` — мета-аннотация: включает `@Configuration`, `@EnableAutoConfiguration`, `@ComponentScan` для пакета класса и ниже.",
            "`SpringApplication.run` поднимает **ApplicationContext** — контейнер бинов. Tomcat стартует внутри JVM на порту 8080 (если не переопределён).",
            "Класс лежит в `tictactoe` — корне сканирования. Контроллеры и `@Configuration` в подпакетах подхватятся автоматически.",
        ],
        ["```", "main() → SpringApplication.run → Tomcat :8080", "```"],
        [
            ("Package", "Корневой пакет приложения.",
             "package tictactoe;",
             [("1", "package tictactoe", "Корень сканирования")]),
            ("Imports + аннотация", "Spring Boot автоконфигурация.",
             'import org.springframework.boot.SpringApplication;\nimport org.springframework.boot.autoconfigure.SpringBootApplication;\n\n@SpringBootApplication\npublic class TicTacToeApplication {',
             [("—", "@SpringBootApplication", "Auto-config + component scan")]),
            ("main", "Точка входа JVM.",
             "    public static void main(String[] args) {\n        SpringApplication.run(TicTacToeApplication.class, args);\n    }\n}",
             [("—", "SpringApplication.run", "Стартует embedded Tomcat")]),
        ],
        "TicTacToeApplication.java", TICTACTOE_APP, "java",
        "Что если класс в `com.other` без @ComponentScan?",
        f"cd {PROJECT}\n.\\gradlew.bat bootRun\n# В другом окне:\nInvoke-WebRequest http://localhost:8080/ -UseBasicParsing | Select-Object StatusCode",
        "./gradlew bootRun & sleep 8 && curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/",
        "Порт 8080 занят → netstat -ano | findstr 8080. bootRun not found → нет Spring Boot plugin.",
        "Сервер поднимается — этап A закрыт.",
        "Теория перед этапом B, затем блок **B.0**.",
        _pad_theory("Spring Boot entry point", 3),
    )


def generate_theory_before_b(add, blank, theory_paragraphs):
    add("# Теория перед Этапом B — Domain, DTO, Repository, immutability")
    blank()
    theory_paragraphs([
        "**Domain-модель** (`GameBoard`, `CurrentGame`) описывает предметную область: правила игры, не JSON и не таблицы SQL. Она не знает про `@RestController` и `@Entity`. Если завтра API станет XML или gRPC — domain останется тем же.",
        "**DTO** (Data Transfer Object) — форма данных для HTTP. `CurrentGameDto` повторяет поля domain, но с сеттерами для Jackson. DTO может иметь `computerStarts`, которого нет в domain — это флаг протокола, не бизнес-сущность.",
        "**Repository** — абстракция хранения. Интерфейс `GameRepository` в datasource объявляет `save` и `findById`. Domain-сервис и контроллер зависят от интерфейса, не от `ConcurrentHashMap`. На этапе C заменишь `GameRepositoryImpl` на JPA — контроллер не тронешь.",
        "**Immutability (неизменяемость)** — `CurrentGame` с `final` полями: новый ход = новый объект с новой доской (`new CurrentGame(id, board.copy())`). Minimax мутирует **копию** доски, не ту, что лежит в storage. Это защита от «тихих» багов, когда два запроса делят один массив.",
        "**Mapper** (`GameMapper`, `GameWebMapper`) — перевод между слоями без `new` в контроллере на десять строк. Один класс — одно направление: entity↔domain, domain↔dto.",
        "Этап B — ~20 блоков от `settings.gradle.kts` до полного curl-теста. Каждый блок — один файл или логическая часть. Не беги: T03 в памяти — фундамент для Postgres и Auth.",
    ])
    add("---")
    blank()


def generate_stage_b(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer):
    add("# ЭТАП B — T03 в памяти (игрок vs компьютер)")
    blank()
    add("> Игра живёт в RAM (`GameStorage`). API: `POST /game/{uuid}`. После этапа C память заменим на PostgreSQL.")
    blank()

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.0", "`settings.gradle.kts`",
        "Имя корневого Gradle-проекта.",
        "3 мин", "★☆☆",
        ["Файл `settings.gradle.kts` в корне задаёт **имя проекта** для IDE и артефактов. Одна строка — но без неё Gradle всё равно работает с дефолтным именем папки."],
        ["```", "TicTacToe_1.2_sql_auth/settings.gradle.kts", "```"],
        [("Имя проекта", "rootProject.name для Gradle и IntelliJ.",
          SETTINGS_GRADLE, [("1", 'rootProject.name', "Отображаемое имя проекта")])],
        "settings.gradle.kts", SETTINGS_GRADLE, "kotlin",
        "Зачем отдельный файл settings?", f"cd {PROJECT}\nGet-Content settings.gradle.kts", "cat settings.gradle.kts",
        "Файл не там → положи в корень рядом с build.gradle.kts.", "Имя проекта зафиксировано.", "Блок **B.1** — GameBoard.",
        _pad_theory("settings.gradle", 2),
    )

    # B.1 GameBoard - 5 micro steps
    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.1", "`GameBoard.java`",
        "Модель поля 3×3 в domain.",
        "15 мин", "★★☆",
        [
            "Доска — **сердце** T03. Клетки — `int`: 0 пусто, 1 игрок (X), 2 компьютер (O). Числа проще enum для Minimax и JSON.",
            "`getCells()` и `copy()` возвращают **копии** — инкапсуляция. Снаружи нельзя испортить внутренний массив.",
            "Minimax будет вызывать `set` на копии, откатывая клетки в EMPTY после рекурсии.",
        ],
        ["```", "GameBoard: int[3][3], константы, get/set, copy", "```"],
        [
            ("Константы", "SIZE, EMPTY, PLAYER, COMPUTER — контракт всего проекта.",
             "package tictactoe.domain.model;\n\npublic class GameBoard {\n    public static final int SIZE = 3;\n    public static final int EMPTY = 0;\n    public static final int PLAYER = 1;\n    public static final int COMPUTER = 2;",
             [("—", "SIZE = 3", "Поле 3x3"), ("—", "0/1/2", "Пусто / X / O")]),
            ("Поле cells", "Двумерный массив — состояние доски.",
             "    private final int[][] cells;\n\n    public GameBoard() {\n        this.cells = new int[SIZE][SIZE];\n    }",
             [("—", "final int[][]", "Ссылка не меняется, содержимое — да")]),
            ("Копирующий конструктор", "Безопасное клонирование из другого массива.",
             "    public GameBoard(int[][] cells) {\n        this.cells = new int[SIZE][SIZE];\n        for (int i = 0; i < SIZE; i++) {\n            System.arraycopy(cells[i], 0, this.cells[i], 0, SIZE);\n        }\n    }",
             [("—", "arraycopy", "Копия строки массива")]),
            ("get / set", "Доступ к клетке по row, col.",
             "    public int get(int row, int col) {\n        return cells[row][col];\n    }\n\n    public void set(int row, int col, int value) {\n        cells[row][col] = value;\n    }",
             [("—", "get/set", "Minimax мутирует через set")]),
            ("getCells и copy", "Наружу только копии.",
             "    public int[][] getCells() {\n        int[][] copy = new int[SIZE][SIZE];\n        for (int i = 0; i < SIZE; i++) {\n            System.arraycopy(cells[i], 0, copy[i], 0, SIZE);\n        }\n        return copy;\n    }\n\n    public GameBoard copy() {\n        return new GameBoard(cells);\n    }\n}",
             [("—", "getCells()", "Защита инкапсуляции"), ("—", "copy()", "Новая доска для хода")]),
        ],
        "GameBoard.java", GAME_BOARD, "java",
        "Что сломается, если getCells() вернёт cells без копии?",
        "# файл создан — compileJava позже", "# то же",
        "cannot find symbol → проверь package и имя файла.",
        "Есть тип «доска» — можно хранить состояние.",
        "Блок **B.2** — CurrentGame.",
        _pad_theory("GameBoard", 4),
    )

    # Continue with more blocks - I'll add them in the main script via import
    _generate_b2_b20(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer)


def _generate_b2_b20(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer):
    """Remaining Stage B blocks B.2 through B.20."""
    from _gen_t04_08_v2_blocks_rest import generate_b_rest
    generate_b_rest(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer, emit_block, _pad_theory, PROJECT)
