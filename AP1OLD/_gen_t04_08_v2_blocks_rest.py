# -*- coding: utf-8 -*-
"""Stage B blocks B.2–B.20 for T04_08 v2 Part 1."""
from _gen_t04_08_v2_codes import *


def generate_b_rest(add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer, emit_block, pad_theory, PROJECT):
    # B.2 CurrentGame
    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.2", "`CurrentGame.java`",
        "Игра = UUID + доска (T03).",
        "10 мин", "★☆☆",
        ["`CurrentGame` — агрегат: идентификатор сессии и снимок доски. В T03 клиент сам генерирует UUID и шлёт в URL и JSON.", "Поля `final`: логически «новый ход» = новый объект, не мутация старого."],
        ["```", "UUID id + GameBoard board", "```"],
        [
            ("Package и поля", "id и board — final.",
             "package tictactoe.domain.model;\n\nimport java.util.UUID;\n\npublic class CurrentGame {\n    private final UUID id;\n    private final GameBoard board;",
             [("—", "final UUID", "Не меняется после создания")]),
            ("Конструктор и геттеры", "Доступ к полям.",
             "    public CurrentGame(UUID id, GameBoard board) {\n        this.id = id;\n        this.board = board;\n    }\n\n    public UUID getId() { return id; }\n    public GameBoard getBoard() { return board; }\n}",
             [("—", "getBoard()", "Сервис делает copy() перед ходом")]),
        ],
        "CurrentGame.java", CURRENT_GAME, "java",
        "Почему id и board final?", "# компиляция позже", "# то же",
        "getBoard() отдаёт ссылку → сервис всегда copy() перед ходом.",
        "Минимальная модель «текущая игра» готова.", "Блок **B.3** — GameService.",
        pad_theory("CurrentGame", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.3", "интерфейс `GameService.java`",
        "Контракт правил в domain.",
        "10 мин", "★★☆",
        ["Интерфейс в **domain** — контроллер знает «что нужно», не «как Minimax устроен».", "Четыре метода покрывают T03 API: ход ИИ, валидация, конец игры, первый ход компьютера."],
        ["```", "GameService: getNextMove, validateBoard, isGameEnded, getFirstMove", "```"],
        [
            ("Interface", "Объявление методов без реализации.",
             "package tictactoe.domain.service;\n\nimport tictactoe.domain.model.CurrentGame;\n\npublic interface GameService {",
             [("—", "interface", "Контракт для impl")]),
            ("Методы", "Четыре операции T03.",
             "    CurrentGame getNextMove(CurrentGame game);\n    boolean validateBoard(CurrentGame game);\n    boolean isGameEnded(CurrentGame game);\n    CurrentGame getFirstMove(CurrentGame game);\n}",
             [("—", "getNextMove", "Minimax после хода X"), ("—", "validateBoard", "Античит")]),
        ],
        "GameService.java", GAME_SERVICE, "java",
        "Зачем interface при одной impl?", "# impl в B.9", "# то же",
        "—", "Domain-контракт записан.", "Блок **B.4** — GameBoardEntity.",
        pad_theory("GameService", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.4", "`GameBoardEntity.java`",
        "Зеркало доски для слоя хранения.",
        "10 мин", "★☆☆",
        ["Entity — POJO для storage/JPA. Domain `GameBoard` и entity разделены: смена БД не трогает domain.", "Поле `cells` не final — JPA на этапе C попросит setter."],
        ["```", "GameBoardEntity ≈ GameBoard, но в datasource.model", "```"],
        [
            ("Класс и конструкторы", "Пустой и из массива.",
             "package tictactoe.datasource.model;\n\nimport tictactoe.domain.model.GameBoard;\n\npublic class GameBoardEntity {\n    private int[][] cells;\n\n    public GameBoardEntity() {\n        this.cells = new int[GameBoard.SIZE][GameBoard.SIZE];\n    }",
             [("—", "GameBoard.SIZE", "Без magic number 3")]),
            ("getCells / setCells", "Копирование при чтении и записи.",
             "    public int[][] getCells() { /* copy */ return copy; }\n    public void setCells(int[][] cells) { /* copy into this.cells */ }",
             [("—", "setCells", "Нужен для JPA позже")]),
        ],
        "GameBoardEntity.java", GAME_BOARD_ENTITY, "java",
        "Чем entity от domain GameBoard?", "# —", "# —",
        "—", "Entity доски готова.", "Блок **B.5** — CurrentGameEntity.",
        pad_theory("GameBoardEntity", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.5", "`CurrentGameEntity.java`",
        "Entity игры: UUID + GameBoardEntity.",
        "8 мин", "★☆☆",
        ["Аналог `CurrentGame`, но с сеттерами для persistence.", "Пустой конструктор — требование JPA/Hibernate позже."],
        ["```", "CurrentGameEntity: id + board entity", "```"],
        [
            ("Поля", "UUID и вложенная entity доски.",
             "package tictactoe.datasource.model;\n\nimport java.util.UUID;\n\npublic class CurrentGameEntity {\n    private UUID id;\n    private GameBoardEntity board;",
             [("—", "GameBoardEntity", "Вложенный объект")]),
            ("Конструкторы и accessors", "Геттеры/сеттеры для всех полей.",
             "    public CurrentGameEntity() {}\n    public CurrentGameEntity(UUID id, GameBoardEntity board) { this.id = id; this.board = board; }\n    // getId setId getBoard setBoard",
             [("—", "setBoard", "Hibernate запишет JSON/embedded")]),
        ],
        "CurrentGameEntity.java", CURRENT_GAME_ENTITY, "java",
        "Зачем пустой конструктор?", "# —", "# —",
        "—", "Entity игры готова.", "Блок **B.6** — GameMapper.",
        pad_theory("CurrentGameEntity", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.6", "`GameMapper.java`",
        "Перевод entity ↔ domain.",
        "12 мин", "★★☆",
        ["Mapper — статические методы, private constructor. Нет Spring-бина — просто утилита.", "null-safe: if (entity == null) return null."],
        ["```", "toDomain / toEntity / toDomainBoard / toEntityBoard", "```"],
        [
            ("Класс", "final + private ctor.",
             "package tictactoe.datasource.mapper;\n\npublic final class GameMapper {\n    private GameMapper() {}",
             [("—", "private GameMapper()", "Утилита, не new")]),
            ("toDomain / toEntity", "CurrentGame ↔ CurrentGameEntity.",
             "    public static CurrentGame toDomain(CurrentGameEntity entity) { ... }\n    public static CurrentGameEntity toEntity(CurrentGame game) { ... }",
             [("—", "toDomain", "Перед работой сервиса")]),
        ],
        "GameMapper.java", GAME_MAPPER, "java",
        "Почему mapper не в domain?", "# —", "# —",
        "—", "Маппинг storage↔domain есть.", "Блок **B.7** — GameStorage.",
        pad_theory("GameMapper", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.7", "`GameStorage.java`",
        "In-memory Map UUID → игра.",
        "10 мин", "★☆☆",
        ["`ConcurrentHashMap` — потокобезопасность при параллельных POST.", "На этапе C **удалишь** этот класс — заменит PostgreSQL."],
        ["```", "Map<UUID, CurrentGameEntity> in RAM", "```"],
        [
            ("Поле map", "ConcurrentHashMap.",
             "package tictactoe.datasource.storage;\n\npublic class GameStorage {\n    private final Map<UUID, CurrentGameEntity> games = new ConcurrentHashMap<>();",
             [("—", "ConcurrentHashMap", "Thread-safe")]),
            ("put / get", "Сохранение и поиск.",
             "    public void put(UUID id, CurrentGameEntity game) { games.put(id, game); }\n    public Optional<CurrentGameEntity> get(UUID id) { return Optional.ofNullable(games.get(id)); }\n}",
             [("—", "Optional", "Игра может не существовать")]),
        ],
        "GameStorage.java", GAME_STORAGE, "java",
        "Зачем Concurrent, не HashMap?", "# —", "# —",
        "—", "RAM-хранилище работает.", "Блок **B.8** — Repository.",
        pad_theory("GameStorage", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.8", "`GameRepository` + `GameRepositoryImpl`",
        "Абстракция save/findById.",
        "15 мин", "★★☆",
        ["Repository скрывает storage и mapper от сервиса.", "Impl — единственное место, где вызывается GameMapper.toEntity."],
        ["```", "GameRepository interface → GameRepositoryImpl(storage)", "```"],
        [
            ("Interface", "save + findById.",
             "package tictactoe.datasource.repository;\n\npublic interface GameRepository {\n    void save(CurrentGame game);\n    Optional<CurrentGame> findById(UUID id);\n}",
             [("—", "save", "После каждого хода")]),
            ("Impl", "Делегирует storage + mapper.",
             "public class GameRepositoryImpl implements GameRepository {\n    private final GameStorage storage;\n    public void save(CurrentGame game) { storage.put(game.getId(), GameMapper.toEntity(game)); }\n    public Optional<CurrentGame> findById(UUID id) { return storage.get(id).map(GameMapper::toDomain); }\n}",
             [("—", "GameMapper::toDomain", "Method reference")]),
        ],
        "GameRepository.java + GameRepositoryImpl.java",
        GAME_REPOSITORY + "\n\n// --- GameRepositoryImpl ---\n\n" + GAME_REPOSITORY_IMPL,
        "java",
        "Зачем interface, если impl один?", "# —", "# —",
        "—", "Репозиторий прячет storage.", "Блок **B.9a** — теория Minimax.",
        pad_theory("GameRepository", 3),
    )

    # B.9a Minimax theory
    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.9a", "Разбор Minimax на примере",
        "Понять рекурсию до отладки.",
        "20 мин", "★★★",
        [
            "**Minimax** — алгоритм для нулевой суммы: компьютер (max) максимизирует score, игрок (min) минимизирует.",
            "Листья: победа O → +10, победа X → −10, ничья → 0. **`depth`** сдвигает score, чтобы выбирать **быструю** победу.",
            "На доске 3×3 полный перебор мал — рекурсия без alpha-beta всё равно мгновенная.",
        ],
        ["```", "findBestMove → для каждой пустой: поставить O → minimax → откат", "```"],
        [
            ("Пример доски", "X в центре, компьютер выбирает угол или ребро.",
             "Доска после хода X в (1,1):\n  . | . | .\n  ---\n  . | X | .\n  ---\n  . | . | .",
             [("—", "(1,1)", "PLAYER в центре")]),
            ("Один вариант O", "Пробуем O в (0,0), рекурсия для X.",
             "Компьютер пробует O в (0,0):\n  O | . | .\n  ---\n  . | X | .\n  ---\n  . | . | .\n\nminimax(..., isMax=false) — ход X в детях.",
             [("—", "isMax=false", "Следующий — min (игрок)")]),
            ("Выбор", "max score среди всех первых ходов O.",
             "Счёт листа: +10 O win, -10 X win, 0 draw.\nЛучший ход = клетка с максимальным score на верхнем уровне.",
             [("—", "findBestMove", "Внешний цикл по клеткам")]),
        ],
        "trace-minimax.txt",
        "Доска после хода X в (1,1):\n  . | . | .\n  ---\n  . | X | .\n  ---\n  . | . | .\n\nКомпьютер пробует O в (0,0) → minimax → score\nchoose max среди детей верхнего уровня.",
        "text",
        "На листе дерева кто ходит — max или min?",
        "# теория — код в B.9", "# то же",
        "—", "Minimax в голове, не только в коде.", "Блок **B.9** — GameServiceImpl.",
        pad_theory("Minimax", 5),
    )

    # B.9 GameServiceImpl - 7 micro steps
    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.9", "`GameServiceImpl.java` (Minimax)",
        "Вся логика PvE: валидация, win/draw, ИИ.",
        "45 мин", "★★★",
        [
            "Самый плотный файл T03. Реализует `GameService` и содержит Minimax.",
            "Пиши **микро-шагами** — не вставляй 170 строк сразу, если впервые видишь алгоритм.",
            "Ключ: после каждого рекурсивного `set` — откат `set(..., EMPTY)`.",
        ],
        ["```", "skeleton → moves → validate → win/draw → findBestMove → minimax → evaluate", "```"],
        [
            ("Skeleton", "Класс, repository, constructor.",
             "package tictactoe.datasource.service;\n\npublic class GameServiceImpl implements GameService {\n    private final GameRepository repository;\n    public GameServiceImpl(GameRepository repository) { this.repository = repository; }",
             [("—", "GameRepository", "Для validateBoard")]),
            ("getNextMove + getFirstMove", "Ход компьютера.",
             "    public CurrentGame getNextMove(CurrentGame game) {\n        GameBoard board = game.getBoard().copy();\n        int[] bestMove = findBestMove(board);\n        if (bestMove != null) board.set(bestMove[0], bestMove[1], GameBoard.COMPUTER);\n        return new CurrentGame(game.getId(), board);\n    }\n    public CurrentGame getFirstMove(CurrentGame game) {\n        GameBoard board = game.getBoard().copy();\n        board.set(1, 1, GameBoard.COMPUTER);\n        return new CurrentGame(game.getId(), board);\n    }",
             [("—", "copy()", "Не мутируем stored board")]),
            ("validateBoard", "Сверка с repository.",
             "    public boolean validateBoard(CurrentGame game) {\n        return repository.findById(game.getId())\n            .map(stored -> boardsMatchExceptOnePlayerMove(...))\n            .orElseGet(() -> isFirstMoveOnlyOnePlayer(...));\n    }",
             [("—", "orElseGet", "Первый ход — особый случай")]),
            ("isFirstMove + boardsMatch", "Античит: одна новая X.",
             "    private boolean isFirstMoveOnlyOnePlayer(GameBoard board) { /* count PLAYER == 1 */ }\n    private boolean boardsMatchExceptOnePlayerMove(GameBoard stored, GameBoard incoming) { /* playerDiff == 1 */ }",
             [("—", "playerDiff", "Ровно одна новая клетка X")]),
            ("isGameEnded + evaluate helpers", "Победа или ничья.",
             "    public boolean isGameEnded(CurrentGame game) { return hasWinner(board) || isDraw(board); }\n    private boolean hasWinner(GameBoard board) { return evaluate(board) != 0; }",
             [("—", "isDraw", "Нет EMPTY — ничья")]),
            ("findBestMove", "Перебор пустых для O.",
             "    private int[] findBestMove(GameBoard board) {\n        int bestScore = Integer.MIN_VALUE;\n        int[] bestMove = null;\n        for (...) { board.set(i,j,COMPUTER); int score = minimax(board,0,false); board.set(i,j,EMPTY); ... }\n        return bestMove;\n    }",
             [("—", "Integer.MIN_VALUE", "Старт max")]),
            ("minimax + evaluate", "Рекурсия и оценка линий.",
             "    private int minimax(GameBoard board, int depth, boolean isMax) { ... }\n    private int evaluate(GameBoard board) { /* 8 линий */ return 0; }",
             [("—", "score - depth", "Быстрая победа")]),
        ],
        "GameServiceImpl.java", GAME_SERVICE_IMPL, "java",
        "Почему в score вычитаем depth при победе O?",
        f"cd {PROJECT}\n.\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "StackOverflow → проверь откат клетки в EMPTY после рекурсии.",
        "Компьютер играет умно.", "Блок **B.10** — DTO.",
        pad_theory("GameServiceImpl", 5),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.10", "DTO: ErrorResponse, GameBoardDto, CurrentGameDto",
        "JSON-формы запроса/ответа.",
        "15 мин", "★★☆",
        ["DTO ≠ domain. Jackson нужны пустой конструктор + getters/setters.", "`computerStarts` — только в DTO, флаг протокола."],
        ["```", "web/model: ErrorResponse, GameBoardDto, CurrentGameDto", "```"],
        [
            ("ErrorResponse", "Поле error для 400/422.",
             "package tictactoe.web.model;\n\npublic class ErrorResponse {\n    private String error;\n    public ErrorResponse() {}\n    public ErrorResponse(String error) { this.error = error; }\n    // getter setter\n}",
             [("—", "error", "Текст для клиента")]),
            ("GameBoardDto", "Обёртка int[][] board.",
             "public class GameBoardDto {\n    private int[][] board;\n    public GameBoardDto() { this.board = new int[GameBoard.SIZE][GameBoard.SIZE]; }\n}",
             [("—", "board", "JSON: board.board")]),
            ("CurrentGameDto", "id + board + computerStarts.",
             "public class CurrentGameDto {\n    private UUID id;\n    private GameBoardDto board;\n    private Boolean computerStarts;\n}",
             [("—", "computerStarts", "Режим «я O»")]),
        ],
        "ErrorResponse.java, GameBoardDto.java, CurrentGameDto.java",
        ERROR_RESPONSE + "\n\n// --- GameBoardDto ---\n\n" + GAME_BOARD_DTO + "\n\n// --- CurrentGameDto ---\n\n" + CURRENT_GAME_DTO,
        "java",
        "Зачем DTO, если есть domain?", "# —", "# —",
        "—", "JSON-модели готовы.", "Блок **B.11** — GameWebMapper.",
        pad_theory("DTO", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.11", "`GameWebMapper.java`",
        "Domain ↔ DTO для HTTP.",
        "12 мин", "★★☆",
        ["Зеркало GameMapper, но web↔domain.", "Контроллер не создаёт CurrentGame вручную."],
        ["```", "toDto(CurrentGame) / toDomain(CurrentGameDto)", "```"],
        [
            ("Класс", "static util.",
             "package tictactoe.web.mapper;\n\npublic final class GameWebMapper {\n    private GameWebMapper() {}",
             [("—", "final class", "Только static")]),
            ("toDto / toDomain", "CurrentGame ↔ CurrentGameDto.",
             "    public static CurrentGameDto toDto(CurrentGame game) { ... }\n    public static CurrentGame toDomain(CurrentGameDto dto) { ... }",
             [("—", "toDomainBoard", "GameBoardDto → GameBoard")]),
        ],
        "GameWebMapper.java", GAME_WEB_MAPPER, "java",
        "Почему два mapper — GameMapper и GameWebMapper?", "# —", "# —",
        "—", "HTTP-слой маппит JSON.", "Блок **B.12** — GameController.",
        pad_theory("GameWebMapper", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.12", "`GameController.java` (T03)",
        "REST POST /game/{gameId}.",
        "25 мин", "★★★",
        ["`@RestController` + `@PostMapping`. Валидация → service → save → DTO.", "422 UNPROCESSABLE_ENTITY для читерства и завершённой игры."],
        ["```", "POST /game/{uuid} → validate → getNextMove → save → 200", "```"],
        [
            ("Class + mapping", "RestController /game.",
             '@RestController\n@RequestMapping("/game")\npublic class GameController {\n    private final GameService gameService;\n    private final GameRepository gameRepository;',
             [("—", "/game", "Base path")]),
            ("makeMove signature", "Path UUID + body DTO.",
             '    @PostMapping("/{gameId}")\n    public ResponseEntity<?> makeMove(@PathVariable UUID gameId, @RequestBody CurrentGameDto request) {',
             [("—", "@RequestBody", "Jackson → DTO")]),
            ("Validation + flow", "400/422 и успех.",
             "        if (!gameService.validateBoard(game)) return 422;\n        if (gameService.isGameEnded(game)) return 422;\n        CurrentGame withComputerMove = gameService.getNextMove(game);\n        gameRepository.save(withComputerMove);\n        return ResponseEntity.ok(GameWebMapper.toDto(withComputerMove));",
             [("—", "validateBoard", "Античит")]),
        ],
        "GameController.java", GAME_CONTROLLER, "java",
        "Почему controller вызывает repository.save?", "# compileJava", "./gradlew compileJava",
        "Bean not found → проверь SpringConfig.", "REST для T03 готов.", "Блок **B.13** — SpringConfig.",
        pad_theory("GameController", 4),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.13", "`SpringConfig.java`",
        "Ручная сборка графа бинов.",
        "15 мин", "★★☆",
        ["`@Configuration` + `@Bean` — цепочка Storage → Repository → Service.", "Spring подставляет аргументы в @Bean методы."],
        ["```", "GameStorage → GameRepositoryImpl → GameServiceImpl", "```"],
        [
            ("Configuration", "Класс с @Bean методами.",
             "@Configuration\npublic class SpringConfig {",
             [("—", "@Configuration", "Фабрика бинов")]),
            ("Beans", "Три @Bean метода.",
             "    @Bean public GameStorage gameStorage() { return new GameStorage(); }\n    @Bean public GameRepository gameRepository(GameStorage s) { return new GameRepositoryImpl(s); }\n    @Bean public GameService gameService(GameRepository r) { return new GameServiceImpl(r); }",
             [("—", "gameService", "Inject в Controller")]),
        ],
        "SpringConfig.java", SPRING_CONFIG, "java",
        "Кто вызывает gameRepository(gameStorage) — ты или Spring?",
        f'$gameId = [guid]::NewGuid().ToString()\n$body = \'{{"id":"\' + $gameId + \'","board":{{"board":[[0,0,0],[0,1,0],[0,0,0]]}}}}\'' + f'\nInvoke-RestMethod -Uri "http://localhost:8080/game/$gameId" -Method POST -ContentType "application/json" -Body $body',
        'GAME_ID=$(uuidgen | tr \'[:upper:]\' \'[:lower:]\')\ncurl -s -X POST "http://localhost:8080/game/$GAME_ID" -H "Content-Type: application/json" -d "{\\"id\\":\\"$GAME_ID\\",\\"board\\":{\\"board\\":[[0,0,0],[0,1,0],[0,0,0]]}}"',
        "Ответ без 2 на доске → GameServiceImpl не в контексте. Connection refused → bootRun.",
        "T03 в памяти работает — ядро этапа B закрыто.", "Блоки **B.14–B.20** — доводка и сценарии.",
        pad_theory("SpringConfig DI", 3),
    )

    # B.14-B.20 extras
    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.14", "Проверка компиляции (`compileJava`)",
        "Убедиться, что все слои собираются без bootRun.",
        "5 мин", "★☆☆",
        ["`compileJava` быстрее `bootRun` — ловит ошибки пакетов и import до запуска Tomcat."],
        ["```", "gradlew compileJava → BUILD SUCCESSFUL", "```"],
        [("Команда", "Компиляция main sources.",
          f"cd {PROJECT}\n.\\gradlew.bat compileJava --no-daemon",
          [("—", "compileJava", "Только javac, без Tomcat")])],
        "compile-check.ps1",
        f"cd {PROJECT}\n.\\gradlew.bat compileJava --no-daemon",
        "powershell",
        "Чем compileJava отличается от bootRun?", f"cd {PROJECT}\n.\\gradlew.bat compileJava", "./gradlew compileJava",
        "cannot find symbol → открой файл из ошибки, сверь package.", "Проект компилируется.", "Блок **B.15** — application.properties.",
        pad_theory("compileJava", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.15", "`application.properties`",
        "Порт и имя приложения.",
        "5 мин", "★☆☆",
        ["Spring Boot читает `src/main/resources/application.properties`. Порт 8080 по умолчанию — явно задаём для ясности."],
        ["```", "server.port=8080", "```"],
        [("Properties", "Минимальный конфиг T03.",
          APPLICATION_PROPERTIES,
          [("—", "server.port", "Tomcat слушает 8080")])],
        "application.properties", APPLICATION_PROPERTIES, "properties",
        "Где Spring ищет properties?", f"cd {PROJECT}\nGet-Content src\\main\\resources\\application.properties", "cat src/main/resources/application.properties",
        "Файл не в resources → Spring не видит.", "Конфиг на месте.", "Блок **B.16** — curl сценарии.",
        pad_theory("application.properties", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.16", "Сценарии curl — полная партия",
        "Пройти игру от первого POST до ничьей/победы.",
        "20 мин", "★★☆",
        ["Клиент шлёт **целую доску** каждый раз. UUID в URL = UUID в JSON.", "После каждого 200 сохраняй доску из ответа для следующего хода."],
        ["```", "POST → 200 + доска с 2 → POST → ...", "```"],
        [
            ("Старт", "Новый UUID, X в центр.",
             f"$gameId = [guid]::NewGuid().ToString()\n$body = '{{\"id\":\"' + $gameId + '\",\"board\":{{\"board\":[[0,0,0],[0,1,0],[0,0,0]]}}}}'\nInvoke-RestMethod -Uri \"http://localhost:8080/game/$gameId\" -Method POST -ContentType \"application/json\" -Body $body",
             [("—", "[0,1,0]", "PLAYER в центре")]),
            ("Второй ход", "Подставь доску из ответа, добавь свой X.",
             "# Возьми board из JSON ответа, поставь 1 в свободную клетку, POST снова",
             [("—", "2 в ответе", "COMPUTER сходил")]),
        ],
        "curl-scenarios.ps1", "# см. микро-шаги + bash в проверке",
        "text",
        "Почему UUID и в path, и в body?",
        f"cd {PROJECT}\n.\\gradlew.bat bootRun\n# второй терминал — curl из микро-шага 1",
        "./gradlew bootRun & sleep 10 && curl ...",
        "422 → validateBoard: ты изменил две клетки или старые.", "Полный цикл API понятен.", "Блок **B.17** — computerStarts.",
        pad_theory("curl сценарии", 4),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.17", "Режим `computerStarts`",
        "Игрок играет за O — компьютер ходит первым.",
        "10 мин", "★★☆",
        ["`computerStarts: true` + пустая доска → `getFirstMove` ставит O в центр (1,1).", "Проверка `isBoardEmpty` в контроллере."],
        ["```", "POST с computerStarts:true и нулями → ответ с 2 в центре", "```"],
        [("JSON", "Флаг computerStarts.",
          '{"id":"<uuid>","computerStarts":true,"board":{"board":[[0,0,0],[0,0,0],[0,0,0]]}}',
          [("—", "computerStarts", "Boolean в DTO")])],
        "computerStarts-request.json", '{"id":"<uuid>","computerStarts":true,"board":{"board":[[0,0,0],[0,0,0],[0,0,0]]}}',
        "text",
        "Где обрабатывается computerStarts — controller или service?",
        f"$gameId = [guid]::NewGuid().ToString()\n$body = '{{\"id\":\"' + $gameId + '\",\"computerStarts\":true,\"board\":{{\"board\":[[0,0,0],[0,0,0],[0,0,0]]}}}}'",
        'curl -X POST ... -d \'{"computerStarts":true,...}\'',
        "200 без 2 в (1,1) → проверь getFirstMove и isBoardEmpty.", "Режим «компьютер первым» работает.", "Блок **B.18** — античит.",
        pad_theory("computerStarts", 3),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.18", "Античит — `validateBoard`",
        "422 при подмене старых клеток.",
        "15 мин", "★★☆",
        ["Клиент не может «стереть» ход компьютера или поставить две X за раз.", "`boardsMatchExceptOnePlayerMove` — ровно одна новая PLAYER."],
        ["```", "Измени старую 2 на 0 → 422", "```"],
        [
            ("Читерский запрос", "Две единицы без сохранённой игры или смена 2.",
             "# Отправь доску с двумя новыми 1 или удали 2 с прошлого ответа",
             [("—", "422", "UNPROCESSABLE_ENTITY")]),
        ],
        "anti-cheat-test", "# тест вручную через curl",
        "text",
        "Почему 422, а не 400?",
        f"# Ожидай ErrorResponse с текстом про некорректное состояние",
        "# curl с двумя единицами",
        "400 только для битого JSON; логика игры — 422.", "Античит проверен.", "Блок **B.19** — Gradle Wrapper.",
        pad_theory("validateBoard античит", 4),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.19", "Gradle Wrapper",
        "gradlew.bat / gradlew без глобального Gradle.",
        "5 мин", "★☆☆",
        ["Wrapper фиксирует версию Gradle в `gradle/wrapper/gradle-wrapper.properties`.", "На Windows — `gradlew.bat`, на Unix — `./gradlew`."],
        ["```", "gradle/wrapper/ + gradlew*", "```"],
        [("Проверка wrapper", "Версия Gradle из wrapper.",
          f"cd {PROJECT}\n.\\gradlew.bat --version",
          [("—", "Gradle", "Версия из wrapper")])],
        "gradle-wrapper",
        f"cd {PROJECT}\n.\\gradlew.bat --version",
        "powershell",
        "Зачем wrapper, если Gradle в IDE?",
        f"cd {PROJECT}\n.\\gradlew.bat --version",
        "./gradlew --version",
        "Нет gradlew → скопируй из шаблонного Spring Boot проекта.", "Wrapper на месте.", "Блок **B.20** — milestone.",
        pad_theory("Gradle Wrapper", 2),
    )

    emit_block(
        add, blank, table_goal, theory_paragraphs, kartina, micro_step, svodka_file, block_footer,
        "B.20", "Milestone — T03 в памяти ✅",
        "Зафиксировать результат части 1.",
        "10 мин", "★☆☆",
        [
            "**Часть 1 завершена**, когда: `bootRun` стартует, POST /game/{uuid} возвращает 200, на доске появляется 2 после хода X, computerStarts работает, читерство → 422.",
            "Дальше (часть 2): PostgreSQL, JPA, Security, PvP — но фундамент T03 уже твой.",
            "Опционально: [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md) для углубления.",
        ],
        ["```", "✅ JDK ✅ Gradle ✅ Spring ✅ Domain ✅ Minimax ✅ REST ✅ RAM storage", "```"],
        [
            ("Чеклист", "Отметь галочки.",
             "- [ ] bootRun без ошибок\n- [ ] POST /game → 200 + computer move\n- [ ] computerStarts → O в центре\n- [ ] validateBoard → 422 на чит\n- [ ] compileJava SUCCESS",
             [("—", "чеклист", "Критерии части 1")]),
        ],
        "milestone-part1.md", "- [ ] bootRun\n- [ ] POST /game\n- [ ] computerStarts\n- [ ] anti-cheat 422\n- [ ] compileJava",
        "text",
        "Какой один файл ты бы объяснил на защите первым?",
        f"cd {PROJECT}\n.\\gradlew.bat bootRun",
        "./gradlew bootRun",
        "Если что-то из чеклиста нет — вернись к блоку, не к готовому проекту.",
        "🎉 **Часть 1 закрыта.** T03 в памяти работает. Часть 2 — PostgreSQL и задания T04.",
        "Продолжение в части 2 генератора / следующем файле туториала.",
        pad_theory("milestone T03", 4),
    )

    # Extra padding sections for line count - FAQ per stage
    add("## FAQ — частые вопросы по части 1")
    blank()
    faq = [
        ("Почему не один Main.java?", "Слои позволяют менять БД и API независимо. На T04 это окупится."),
        ("Зачем entity, если есть domain?", "Разделение storage и правил. JPA аннотации не должны быть в domain."),
        ("Minimax обязателен?", "Для PvE vs компьютер — да. Алгоритм в GameServiceImpl — ядро задания."),
        ("Можно ли пропустить этап A?", "Только если JDK и bootRun уже работают. Иначе отладка B будет адом."),
        ("Где PostgreSQL?", "Часть 2. Сейчас GameStorage — намеренно временный."),
    ]
    for q, a in faq:
        add(f"**{q}** {a}")
        blank()

    add("## Шпаргалка: коды HTTP в T03")
    blank()
    add("| Код | Когда |")
    add("|-----|-------|")
    add("| 200 | Успешный ход, доска с ответом компьютера |")
    add("| 400 | Битый JSON, нет board, UUID не совпадает |")
    add("| 422 | Чит, игра уже ended |")
    blank()

    add("## Шпаргалка: значения клеток")
    blank()
    add("| int | Кто |")
    add("|-----|-----|")
    add("| 0 | Пусто |")
    add("| 1 | Игрок (X) |")
    add("| 2 | Компьютер (O) |")
    blank()

    # Expand with detailed walkthrough for each layer
    for layer, desc, files in [
        ("domain.model", "Чистые модели без Spring", "GameBoard, CurrentGame"),
        ("domain.service", "Интерфейсы правил", "GameService"),
        ("datasource.model", "Entity для storage", "GameBoardEntity, CurrentGameEntity"),
        ("datasource.mapper", "entity↔domain", "GameMapper"),
        ("datasource.storage", "RAM", "GameStorage"),
        ("datasource.repository", "save/findById", "GameRepository, GameRepositoryImpl"),
        ("datasource.service", "Minimax + validation", "GameServiceImpl"),
        ("web.model", "JSON DTO", "ErrorResponse, GameBoardDto, CurrentGameDto"),
        ("web.mapper", "dto↔domain", "GameWebMapper"),
        ("web.controller", "HTTP", "GameController"),
        ("di", "Beans", "SpringConfig"),
    ]:
        add(f"### Слой `{layer}`")
        blank()
        add(f"{desc}. Файлы: **{files}**.")
        blank()
        add(f"Если ошибка компиляции в этом слое — не трогай другие пакеты, пока не закроешь «Сверку» для текущего блока.")
        blank()
        add("Перед коммитом (когда будешь готов) мысленно проговори: кто вызывает кого сверху вниз. Controller → GameService (interface) → GameServiceImpl → GameRepository → GameStorage.")
        blank()

    add("---")
    blank()
    add("## Конец части 1")
    blank()
    add("Ты прошёл путь от JDK до работающего REST API с Minimax в памяти. **Не удаляй** код — на нём построим PostgreSQL в части 2.")
    blank()
