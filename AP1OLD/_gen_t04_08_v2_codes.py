# -*- coding: utf-8 -*-
"""Source code snippets for T04_08 v2 Part 1 generator (from T04_01 T03 simplified)."""

SETTINGS_GRADLE = 'rootProject.name = "TicTacToe"'

BUILD_GRADLE = """plugins {
    id("java")
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "org.example"
version = "1.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
}"""

TICTACTOE_APP = """package tictactoe;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TicTacToeApplication {

    public static void main(String[] args) {
        SpringApplication.run(TicTacToeApplication.class, args);
    }
}"""

GAME_BOARD = """package tictactoe.domain.model;

/**
 * Игровое поле 3x3.
 * 0 — пусто, 1 — X (игрок), 2 — O (компьютер).
 */
public class GameBoard {

    public static final int SIZE = 3;
    public static final int EMPTY = 0;
    public static final int PLAYER = 1;    // X
    public static final int COMPUTER = 2;  // O

    private final int[][] cells;

    public GameBoard() {
        this.cells = new int[SIZE][SIZE];
    }

    public GameBoard(int[][] cells) {
        this.cells = new int[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            System.arraycopy(cells[i], 0, this.cells[i], 0, SIZE);
        }
    }

    public int get(int row, int col) {
        return cells[row][col];
    }

    public void set(int row, int col, int value) {
        cells[row][col] = value;
    }

    public int[][] getCells() {
        int[][] copy = new int[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            System.arraycopy(cells[i], 0, copy[i], 0, SIZE);
        }
        return copy;
    }

    public GameBoard copy() {
        return new GameBoard(cells);
    }
}"""

CURRENT_GAME = """package tictactoe.domain.model;

import java.util.UUID;

/**
 * Текущая игра: id + доска.
 */
public class CurrentGame {

    private final UUID id;
    private final GameBoard board;

    public CurrentGame(UUID id, GameBoard board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() {
        return id;
    }

    public GameBoard getBoard() {
        return board;
    }
}"""

GAME_SERVICE = """package tictactoe.domain.service;

import tictactoe.domain.model.CurrentGame;

public interface GameService {

    /** Ход компьютера (Minimax) после хода игрока. */
    CurrentGame getNextMove(CurrentGame game);

    /** Проверка: клиент не изменил старые клетки. */
    boolean validateBoard(CurrentGame game);

    /** Игра завершена (победа или ничья)? */
    boolean isGameEnded(CurrentGame game);

    /** Первый ход компьютера (игрок играет за O). */
    CurrentGame getFirstMove(CurrentGame game);
}"""

GAME_BOARD_ENTITY = """package tictactoe.datasource.model;

import tictactoe.domain.model.GameBoard;

public class GameBoardEntity {

    private int[][] cells;

    public GameBoardEntity() {
        this.cells = new int[GameBoard.SIZE][GameBoard.SIZE];
    }

    public GameBoardEntity(int[][] cells) {
        this.cells = new int[GameBoard.SIZE][GameBoard.SIZE];
        for (int i = 0; i < GameBoard.SIZE; i++) {
            System.arraycopy(cells[i], 0, this.cells[i], 0, GameBoard.SIZE);
        }
    }

    public int[][] getCells() {
        int[][] copy = new int[GameBoard.SIZE][GameBoard.SIZE];
        for (int i = 0; i < GameBoard.SIZE; i++) {
            System.arraycopy(cells[i], 0, copy[i], 0, GameBoard.SIZE);
        }
        return copy;
    }

    public void setCells(int[][] cells) {
        this.cells = new int[GameBoard.SIZE][GameBoard.SIZE];
        for (int i = 0; i < GameBoard.SIZE; i++) {
            System.arraycopy(cells[i], 0, this.cells[i], 0, GameBoard.SIZE);
        }
    }
}"""

CURRENT_GAME_ENTITY = """package tictactoe.datasource.model;

import java.util.UUID;

public class CurrentGameEntity {

    private UUID id;
    private GameBoardEntity board;

    public CurrentGameEntity() {
    }

    public CurrentGameEntity(UUID id, GameBoardEntity board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public GameBoardEntity getBoard() {
        return board;
    }

    public void setBoard(GameBoardEntity board) {
        this.board = board;
    }
}"""

GAME_MAPPER = """package tictactoe.datasource.mapper;

import tictactoe.datasource.model.CurrentGameEntity;
import tictactoe.datasource.model.GameBoardEntity;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;

public final class GameMapper {

    private GameMapper() {
    }

    public static CurrentGame toDomain(CurrentGameEntity entity) {
        if (entity == null) {
            return null;
        }
        GameBoard board = toDomainBoard(entity.getBoard());
        return new CurrentGame(entity.getId(), board);
    }

    public static CurrentGameEntity toEntity(CurrentGame game) {
        if (game == null) {
            return null;
        }
        return new CurrentGameEntity(game.getId(), toEntityBoard(game.getBoard()));
    }

    public static GameBoard toDomainBoard(GameBoardEntity entity) {
        if (entity == null) {
            return null;
        }
        return new GameBoard(entity.getCells());
    }

    public static GameBoardEntity toEntityBoard(GameBoard board) {
        if (board == null) {
            return null;
        }
        return new GameBoardEntity(board.getCells());
    }
}"""

GAME_STORAGE = """package tictactoe.datasource.storage;

import tictactoe.datasource.model.CurrentGameEntity;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * In-memory хранилище. В T04 Задание 1 — УДАЛИШЬ этот класс.
 */
public class GameStorage {

    private final Map<UUID, CurrentGameEntity> games = new ConcurrentHashMap<>();

    public void put(UUID id, CurrentGameEntity game) {
        games.put(id, game);
    }

    public Optional<CurrentGameEntity> get(UUID id) {
        return Optional.ofNullable(games.get(id));
    }
}"""

GAME_REPOSITORY = """package tictactoe.datasource.repository;

import tictactoe.domain.model.CurrentGame;

import java.util.Optional;
import java.util.UUID;

public interface GameRepository {

    void save(CurrentGame game);

    Optional<CurrentGame> findById(UUID id);
}"""

GAME_REPOSITORY_IMPL = """package tictactoe.datasource.repository;

import tictactoe.datasource.mapper.GameMapper;
import tictactoe.datasource.storage.GameStorage;
import tictactoe.domain.model.CurrentGame;

import java.util.Optional;
import java.util.UUID;

public class GameRepositoryImpl implements GameRepository {

    private final GameStorage storage;

    public GameRepositoryImpl(GameStorage storage) {
        this.storage = storage;
    }

    @Override
    public void save(CurrentGame game) {
        storage.put(game.getId(), GameMapper.toEntity(game));
    }

    @Override
    public Optional<CurrentGame> findById(UUID id) {
        return storage.get(id).map(GameMapper::toDomain);
    }
}"""

GAME_SERVICE_IMPL = """package tictactoe.datasource.service;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.service.GameService;
import tictactoe.datasource.repository.GameRepository;

public class GameServiceImpl implements GameService {

    private final GameRepository repository;

    public GameServiceImpl(GameRepository repository) {
        this.repository = repository;
    }

    @Override
    public CurrentGame getNextMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        int[] bestMove = findBestMove(board);
        if (bestMove != null) {
            board.set(bestMove[0], bestMove[1], GameBoard.COMPUTER);
        }
        return new CurrentGame(game.getId(), board);
    }

    @Override
    public CurrentGame getFirstMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        board.set(1, 1, GameBoard.COMPUTER);
        return new CurrentGame(game.getId(), board);
    }

    @Override
    public boolean validateBoard(CurrentGame game) {
        return repository.findById(game.getId())
                .map(stored -> boardsMatchExceptOnePlayerMove(stored.getBoard(), game.getBoard()))
                .orElseGet(() -> isFirstMoveOnlyOnePlayer(game.getBoard()));
    }

    private boolean isFirstMoveOnlyOnePlayer(GameBoard board) {
        int count = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.PLAYER) {
                    count++;
                } else if (board.get(i, j) != GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return count == 1;
    }

    @Override
    public boolean isGameEnded(CurrentGame game) {
        GameBoard board = game.getBoard();
        return hasWinner(board) || isDraw(board);
    }

    private boolean boardsMatchExceptOnePlayerMove(GameBoard stored, GameBoard incoming) {
        int playerDiff = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                int s = stored.get(i, j);
                int inc = incoming.get(i, j);
                if (s != inc) {
                    if (s == GameBoard.EMPTY && inc == GameBoard.PLAYER) {
                        playerDiff++;
                    } else {
                        return false;
                    }
                }
            }
        }
        return playerDiff == 1;
    }

    private boolean hasWinner(GameBoard board) {
        return evaluate(board) != 0;
    }

    private boolean isDraw(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    private int[] findBestMove(GameBoard board) {
        int bestScore = Integer.MIN_VALUE;
        int[] bestMove = null;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    board.set(i, j, GameBoard.COMPUTER);
                    int score = minimax(board, 0, false);
                    board.set(i, j, GameBoard.EMPTY);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = new int[]{i, j};
                    }
                }
            }
        }
        return bestMove;
    }

    private int minimax(GameBoard board, int depth, boolean isMax) {
        int score = evaluate(board);
        if (score == 10) return score - depth;
        if (score == -10) return score + depth;
        if (isDraw(board)) return 0;

        if (isMax) {
            int best = Integer.MIN_VALUE;
            for (int i = 0; i < GameBoard.SIZE; i++) {
                for (int j = 0; j < GameBoard.SIZE; j++) {
                    if (board.get(i, j) == GameBoard.EMPTY) {
                        board.set(i, j, GameBoard.COMPUTER);
                        best = Math.max(best, minimax(board, depth + 1, false));
                        board.set(i, j, GameBoard.EMPTY);
                    }
                }
            }
            return best;
        } else {
            int best = Integer.MAX_VALUE;
            for (int i = 0; i < GameBoard.SIZE; i++) {
                for (int j = 0; j < GameBoard.SIZE; j++) {
                    if (board.get(i, j) == GameBoard.EMPTY) {
                        board.set(i, j, GameBoard.PLAYER);
                        best = Math.min(best, minimax(board, depth + 1, true));
                        board.set(i, j, GameBoard.EMPTY);
                    }
                }
            }
            return best;
        }
    }

    private int evaluate(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            if (board.get(i, 0) == board.get(i, 1) && board.get(i, 1) == board.get(i, 2) && board.get(i, 0) != GameBoard.EMPTY) {
                return board.get(i, 0) == GameBoard.COMPUTER ? 10 : -10;
            }
            if (board.get(0, i) == board.get(1, i) && board.get(1, i) == board.get(2, i) && board.get(0, i) != GameBoard.EMPTY) {
                return board.get(0, i) == GameBoard.COMPUTER ? 10 : -10;
            }
        }
        if (board.get(0, 0) == board.get(1, 1) && board.get(1, 1) == board.get(2, 2) && board.get(0, 0) != GameBoard.EMPTY) {
            return board.get(0, 0) == GameBoard.COMPUTER ? 10 : -10;
        }
        if (board.get(0, 2) == board.get(1, 1) && board.get(1, 1) == board.get(2, 0) && board.get(0, 2) != GameBoard.EMPTY) {
            return board.get(0, 2) == GameBoard.COMPUTER ? 10 : -10;
        }
        return 0;
    }
}"""

ERROR_RESPONSE = """package tictactoe.web.model;

public class ErrorResponse {

    private String error;

    public ErrorResponse() {
    }

    public ErrorResponse(String error) {
        this.error = error;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }
}"""

GAME_BOARD_DTO = """package tictactoe.web.model;

import tictactoe.domain.model.GameBoard;

public class GameBoardDto {

    private int[][] board;

    public GameBoardDto() {
        this.board = new int[GameBoard.SIZE][GameBoard.SIZE];
    }

    public GameBoardDto(int[][] board) {
        this.board = board;
    }

    public int[][] getBoard() {
        return board;
    }

    public void setBoard(int[][] board) {
        this.board = board;
    }
}"""

CURRENT_GAME_DTO = """package tictactoe.web.model;

import java.util.UUID;

public class CurrentGameDto {

    private UUID id;
    private GameBoardDto board;
    private Boolean computerStarts;

    public CurrentGameDto() {
    }

    public CurrentGameDto(UUID id, GameBoardDto board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public GameBoardDto getBoard() {
        return board;
    }

    public void setBoard(GameBoardDto board) {
        this.board = board;
    }

    public Boolean getComputerStarts() {
        return computerStarts;
    }

    public void setComputerStarts(Boolean computerStarts) {
        this.computerStarts = computerStarts;
    }
}"""

GAME_WEB_MAPPER = """package tictactoe.web.mapper;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.GameBoardDto;

public final class GameWebMapper {

    private GameWebMapper() {
    }

    public static CurrentGameDto toDto(CurrentGame game) {
        if (game == null) {
            return null;
        }
        return new CurrentGameDto(game.getId(), toDto(game.getBoard()));
    }

    public static CurrentGame toDomain(CurrentGameDto dto) {
        if (dto == null) {
            return null;
        }
        return new CurrentGame(dto.getId(), toDomainBoard(dto.getBoard()));
    }

    public static GameBoardDto toDto(GameBoard board) {
        if (board == null) {
            return null;
        }
        return new GameBoardDto(board.getCells());
    }

    public static GameBoard toDomainBoard(GameBoardDto dto) {
        if (dto == null || dto.getBoard() == null) {
            return null;
        }
        return new GameBoard(dto.getBoard());
    }
}"""

GAME_CONTROLLER = """package tictactoe.web.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.service.GameService;
import tictactoe.datasource.repository.GameRepository;
import tictactoe.web.mapper.GameWebMapper;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.ErrorResponse;

import java.util.UUID;

@RestController
@RequestMapping("/game")
public class GameController {

    private final GameService gameService;
    private final GameRepository gameRepository;

    public GameController(GameService gameService, GameRepository gameRepository) {
        this.gameService = gameService;
        this.gameRepository = gameRepository;
    }

    @PostMapping("/{gameId}")
    public ResponseEntity<?> makeMove(@PathVariable("gameId") UUID gameId,
                                      @RequestBody CurrentGameDto request) {
        if (request == null || request.getBoard() == null) {
            return ResponseEntity.badRequest()
                    .body(new ErrorResponse("Некорректный запрос: отсутствует игровое поле"));
        }
        if (!gameId.equals(request.getId())) {
            return ResponseEntity.badRequest()
                    .body(new ErrorResponse("UUID в пути и в теле запроса не совпадают"));
        }

        CurrentGame game = GameWebMapper.toDomain(request);
        if (game.getBoard() == null) {
            return ResponseEntity.badRequest()
                    .body(new ErrorResponse("Некорректное игровое поле"));
        }

        if (Boolean.TRUE.equals(request.getComputerStarts()) && isBoardEmpty(game.getBoard())) {
            CurrentGame withFirstMove = gameService.getFirstMove(game);
            gameRepository.save(withFirstMove);
            return ResponseEntity.ok(GameWebMapper.toDto(withFirstMove));
        }

        if (!gameService.validateBoard(game)) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                    .body(new ErrorResponse("Некорректное состояние игры"));
        }

        if (gameService.isGameEnded(game)) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                    .body(new ErrorResponse("Игра уже завершена"));
        }

        CurrentGame withComputerMove = gameService.getNextMove(game);
        gameRepository.save(withComputerMove);

        return ResponseEntity.ok(GameWebMapper.toDto(withComputerMove));
    }

    private static boolean isBoardEmpty(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) != GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }
}"""

SPRING_CONFIG = """package tictactoe.di;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import tictactoe.datasource.repository.GameRepository;
import tictactoe.datasource.repository.GameRepositoryImpl;
import tictactoe.datasource.service.GameServiceImpl;
import tictactoe.datasource.storage.GameStorage;
import tictactoe.domain.service.GameService;

@Configuration
public class SpringConfig {

    @Bean
    public GameStorage gameStorage() {
        return new GameStorage();
    }

    @Bean
    public GameRepository gameRepository(GameStorage gameStorage) {
        return new GameRepositoryImpl(gameStorage);
    }

    @Bean
    public GameService gameService(GameRepository gameRepository) {
        return new GameServiceImpl(gameRepository);
    }
}"""

APPLICATION_PROPERTIES = """server.port=8080
spring.application.name=TicTacToe
# PostgreSQL — добавим на этапе C (часть 2)
# spring.datasource.url=jdbc:postgresql://localhost:5432/tictactoe
"""

PACKAGES = """tictactoe
tictactoe.domain.model
tictactoe.domain.service
tictactoe.datasource.model
tictactoe.datasource.repository
tictactoe.datasource.mapper
tictactoe.datasource.service
tictactoe.datasource.storage
tictactoe.web.controller
tictactoe.web.model
tictactoe.web.mapper
tictactoe.di"""
