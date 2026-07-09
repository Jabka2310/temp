# -*- coding: utf-8 -*-
"""Block generators for T04_08 v2 part2 (stages C, D, E)."""

# --- Reference code (exact from TicTacToe_1.2_sql_auth) ---

BUILD_GRADLE = r'''plugins {
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
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security") // включает Spring Security. Без него не будет SecurityFilterChain и фильтров. После добавления все /game/* по умолчанию начнут требовать auth
    runtimeOnly("org.postgresql:postgresql")
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.test {
    useJUnitPlatform()
}

/* добавили две зависимости — data-jpa (Hibernate + репозитории) и драйвер PostgreSQL.
Без них Spring не знает как ходить в БД. После Reload IDE подтянет jakarta.persistence.*/'''

APP_PROPERTIES = r'''spring.datasource.url=jdbc:postgresql://localhost:5432/tictactoe
spring.datasource.username=ТВОЙ_ЛОГИН
spring.datasource.password=ТВОЙ_ПАРОЛЬ

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect'''

GAME_BOARD_ENTITY = r'''package tictactoe.datasource.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import tictactoe.domain.model.GameBoard;

/**
 * Доска 3x3 как встраиваемый объект в таблице games.
 * 9 отдельных колонок: cell_00 ... cell_22
 */
@Embeddable
public class GameBoardEntity {

    @Column(name = "cell_00") private int cell00;
    @Column(name = "cell_01") private int cell01;
    @Column(name = "cell_02") private int cell02;
    @Column(name = "cell_10") private int cell10;
    @Column(name = "cell_11") private int cell11;
    @Column(name = "cell_12") private int cell12;
    @Column(name = "cell_20") private int cell20;
    @Column(name = "cell_21") private int cell21;
    @Column(name = "cell_22") private int cell22;

    public GameBoardEntity() {
    }

    public GameBoardEntity(int[][] cells) {
        cell00 = cells[0][0]; cell01 = cells[0][1]; cell02 = cells[0][2];
        cell10 = cells[1][0]; cell11 = cells[1][1]; cell12 = cells[1][2];
        cell20 = cells[2][0]; cell21 = cells[2][1]; cell22 = cells[2][2];
    }

    public int[][] getCells() {
        return new int[][]{
                {cell00, cell01, cell02},
                {cell10, cell11, cell12},
                {cell20, cell21, cell22}
        };
    }

    public void setFromBoard(int[][] cells) {
        cell00 = cells[0][0]; cell01 = cells[0][1]; cell02 = cells[0][2];
        cell10 = cells[1][0]; cell11 = cells[1][1]; cell12 = cells[1][2];
        cell20 = cells[2][0]; cell21 = cells[2][1]; cell22 = cells[2][2];
    }

    public int get(int row, int col) {
        return getCells()[row][col];
    }

    public void set(int row, int col, int value) {
        switch (row * GameBoard.SIZE + col) {
            case 0 -> cell00 = value;
            case 1 -> cell01 = value;
            case 2 -> cell02 = value;
            case 3 -> cell10 = value;
            case 4 -> cell11 = value;
            case 5 -> cell12 = value;
            case 6 -> cell20 = value;
            case 7 -> cell21 = value;
            case 8 -> cell22 = value;
            default -> throw new IllegalArgumentException("Invalid cell");
        }
    }
}

//Замена двумерных массивов, т.к jpa плохо хранит двумерные массивы
//@Embeddable — «кусок таблицы», не отдельная таблица. Доска ляжет колонками cell_00…cell_22 внутри games.
//setFromBoard нужен мапперу — копирует int[][] в поля.'''

CURRENT_GAME_ENTITY_C = r'''package tictactoe.datasource.model;

import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@Entity
@Table(name = "games")
public class CurrentGameEntity {

    @Id
    private UUID id;

    @Embedded
    private GameBoardEntity board;

    public CurrentGameEntity() {
        this.board = new GameBoardEntity();
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public GameBoardEntity getBoard() { return board; }
    public void setBoard(GameBoardEntity board) { this.board = board; }
}'''

CURRENT_GAME_ENTITY_FULL = r'''package tictactoe.datasource.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;

import java.util.UUID;

@Entity
@Table(name = "games")
public class CurrentGameEntity {

    @Id
    private UUID id;

    @Embedded
    private GameBoardEntity board;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private GameState state;

    @Column(name = "player1_id")
    private UUID player1Id;

    @Column(name = "player2_id")
    private UUID player2Id;

    @Enumerated(EnumType.STRING)
    @Column(name = "player1_symbol")
    private Symbol player1Symbol;

    @Enumerated(EnumType.STRING)
    @Column(name = "player2_symbol")
    private Symbol player2Symbol;

    @Column(name = "current_turn_player_id")
    private UUID currentTurnPlayerId;

    @Column(name = "winner_id")
    private UUID winnerId;

    @Column(name = "vs_computer", nullable = false)
    private boolean vsComputer;

    public CurrentGameEntity() {
        this.board = new GameBoardEntity();
        this.state = GameState.PLAYER_TURN;
        this.vsComputer = false;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public GameBoardEntity getBoard() { return board; }
    public void setBoard(GameBoardEntity board) { this.board = board; }

    public GameState getState() { return state; }
    public void setState(GameState state) { this.state = state; }

    public UUID getPlayer1Id() { return player1Id; }
    public void setPlayer1Id(UUID player1Id) { this.player1Id = player1Id; }

    public UUID getPlayer2Id() { return player2Id; }
    public void setPlayer2Id(UUID player2Id) { this.player2Id = player2Id; }

    public Symbol getPlayer1Symbol() { return player1Symbol; }
    public void setPlayer1Symbol(Symbol player1Symbol) { this.player1Symbol = player1Symbol; }

    public Symbol getPlayer2Symbol() { return player2Symbol; }
    public void setPlayer2Symbol(Symbol player2Symbol) { this.player2Symbol = player2Symbol; }

    public UUID getCurrentTurnPlayerId() { return currentTurnPlayerId; }
    public void setCurrentTurnPlayerId(UUID currentTurnPlayerId) { this.currentTurnPlayerId = currentTurnPlayerId; }

    public UUID getWinnerId() { return winnerId; }
    public void setWinnerId(UUID winnerId) { this.winnerId = winnerId; }

    public boolean isVsComputer() { return vsComputer; }
    public void setVsComputer(boolean vsComputer) { this.vsComputer = vsComputer; }
}

// те же поля, что в domain, но с JPA-колонками. Hibernate добавит колонки в games (или обновит схему).
// @Enumerated(STRING) — в БД хранится WAITING_FOR_PLAYERS, а не число.'''

GAME_REPOSITORY = r'''package tictactoe.datasource.repository;

import org.springframework.data.repository.CrudRepository;
import tictactoe.datasource.model.CurrentGameEntity;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameState;

import java.util.List;
import java.util.UUID;

public interface GameRepository extends CrudRepository<CurrentGameEntity, UUID>{
    List<CurrentGameEntity> findByState(GameState state);
}

//findByState(WAITING_FOR_PLAYERS) — список игр для GET /game/available.
// Spring Data снова генерирует SQL по имени метода.'''

GAME_MAPPER_C = r'''package tictactoe.datasource.mapper;

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
        CurrentGameEntity entity = new CurrentGameEntity();
        entity.setId(game.getId());
        entity.setBoard(toEntityBoard(game.getBoard()));
        return entity;
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
        GameBoardEntity entity = new GameBoardEntity();
        entity.setFromBoard(board.getCells());
        return entity;
    }
}'''

GAME_MAPPER_FULL = r'''package tictactoe.datasource.mapper;

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
        return new CurrentGame(
                entity.getId(),
                board,
                entity.getState(),
                entity.getPlayer1Id(),
                entity.getPlayer2Id(),
                entity.getPlayer1Symbol(),
                entity.getPlayer2Symbol(),
                entity.getCurrentTurnPlayerId(),
                entity.getWinnerId(),
                entity.isVsComputer()
        );
    }

    public static CurrentGameEntity toEntity(CurrentGame game) {
        if (game == null) {
            return null;
        }
        CurrentGameEntity entity = new CurrentGameEntity();
        entity.setId(game.getId());
        entity.setBoard(toEntityBoard(game.getBoard()));
        entity.setState(game.getState());
        entity.setPlayer1Id(game.getPlayer1Id());
        entity.setPlayer2Id(game.getPlayer2Id());
        entity.setPlayer1Symbol(game.getPlayer1Symbol());
        entity.setPlayer2Symbol(game.getPlayer2Symbol());
        entity.setCurrentTurnPlayerId(game.getCurrentTurnPlayerId());
        entity.setWinnerId(game.getWinnerId());
        entity.setVsComputer(game.isVsComputer());
        return entity;
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
        GameBoardEntity entity = new GameBoardEntity();
        entity.setFromBoard(board.getCells());
        return entity;
    }
}

// маппер расширили под новые поля.
// Репозиторий по-прежнему работает только с entity — domain остаётся чистым от @Column.'''

SPRING_CONFIG = r'''package tictactoe.di;

import org.springframework.context.annotation.Configuration;

/**
 * GameServiceImpl и GameRepository — Spring создаёт автоматически
 * (@Service и CrudRepository).
 */
@Configuration
public class SpringConfig {
}'''

USER_ENTITY = r'''package tictactoe.datasource.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    private UUID id;

    @Column(nullable = false, unique = true)
    private String login;

    @Column(nullable = false)
    private String password;

    public UserEntity(){
    }

    public UserEntity(UUID id, String login, String password) {
        this.id = id;
        this.login = login;
        this.password = password;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}

// таблица users — login уникальный, пароль пока plain text
// @Entity + @Table — Hibernate создаст таблицу при старте, как с games.'''

USER_REPOSITORY = r'''package tictactoe.datasource.repository;

import org.springframework.data.repository.CrudRepository;
import tictactoe.datasource.model.UserEntity;

import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends CrudRepository<UserEntity, UUID> {
    Optional<UserEntity> findByLogin(String login);

    boolean existsByLogin(String login);
}

//findByLogin и existsByLogin — Spring Data сам сгенерирует SQL по имени метода.
// Не нужно писать SELECT * FROM users WHERE login = ?.'''

USER_SERVICE = r'''package tictactoe.domain.service;

import java.util.Optional;
import java.util.UUID;

public interface UserService {
    boolean register(String login, String password); // Вернет тру - если успешная авторизация
    Optional<UUID> authenticate(String login, String password); // Вернет айди если авторизация успешна
    Optional<String> findLoginById(UUID id);
}'''

USER_SERVICE_IMPL = r'''package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.datasource.model.UserEntity;
import tictactoe.datasource.repository.UserRepository;
import tictactoe.domain.service.UserService;

import java.util.Optional;
import java.util.UUID;

@Service
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public boolean register(String login, String password) {
        if (login == null || password == null || login.isBlank() || password.isBlank()) return false;
        if (userRepository.existsByLogin(login)) return false;
        UUID id = UUID.randomUUID();
        userRepository.save(new UserEntity(id, login, password));
        return true;
    }

    @Override
    public Optional<UUID> authenticate(String login, String password) {
        return userRepository.findByLogin(login)
                .filter(user -> user.getPassword().equals(password))
                .map(UserEntity::getId);
    }

    @Override
    public Optional<String> findLoginById(UUID id) {
        return userRepository.findById(id).map(UserEntity::getLogin);
    }
}'''

SIGN_UP_REQUEST = r'''package tictactoe.web.model;

public class SignUpRequest {

    private String login;
    private String password;

    public SignUpRequest() {
    }

    public SignUpRequest(String login, String password) {
        this.login = login;
        this.password = password;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}'''

AUTH_SERVICE = r'''package tictactoe.domain.service;

import tictactoe.web.model.SignUpRequest;

import java.util.UUID;

public interface AuthService {

    boolean register(SignUpRequest request);

    /** @return UUID пользователя или null если неверные credentials */
    UUID authorize(String authorizationHeader);
}'''

AUTH_SERVICE_IMPL = r'''package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.domain.service.AuthService;
import tictactoe.domain.service.UserService;
import tictactoe.web.model.SignUpRequest;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.UUID;

@Service
public class AuthServiceImpl implements AuthService {
    private final UserService userService;

    public AuthServiceImpl(UserService userService) {
        this.userService = userService;
    }

    @Override
    public boolean register(SignUpRequest request) {
        if (request == null) return false;
        return userService.register(request.getLogin(), request.getPassword());
    }

    @Override
    public UUID authorize(String authorizationHeader) {
        String[] credentials = parseBasicAuth(authorizationHeader);
        if (credentials == null) {
            return null;
        }
        return userService.authenticate(credentials[0], credentials[1]).orElse(null);
    }

    private String[] parseBasicAuth(String header) {
        if (header == null || !header.startsWith("Basic ")) {
            return null;
        }
        try {
            String base64 = header.substring(6).trim();
            String decoded = new String(Base64.getDecoder().decode(base64), StandardCharsets.UTF_8);
            int colonIndex = decoded.indexOf(':');
            if (colonIndex < 0) {
                return null;
            }
            String login = decoded.substring(0, colonIndex);
            String password = decoded.substring(colonIndex + 1);
            return new String[]{login, password};
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}


//parseBasicAuth — сердце Basic Auth. Берёт заголовок, отрезает "Basic ", декодирует Base64,
// режет по первому :. Если что-то не так — null, фильтр вернёт 401.'''

AUTH_CONTROLLER = r'''package tictactoe.web.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.service.AuthService;
import tictactoe.web.model.ErrorResponse;
import tictactoe.web.model.SignUpRequest;

import java.util.UUID;

@RestController
@RequestMapping("/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody SignUpRequest request) {
        boolean success = authService.register(request);
        if (success) return ResponseEntity.ok().build();
        return ResponseEntity.badRequest()
                .body(new ErrorResponse("Registration failed: login may already exist"));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestHeader(value = "Authorization", required = false) String authHeader) {
        UUID userId = authService.authorize(authHeader);
        if (userId == null) return ResponseEntity.status(401)
                .body(new ErrorResponse("Unauthorized"));
        return ResponseEntity.ok(userId);
    }

}
'''

AUTH_FILTER = r'''package tictactoe.web.filter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.filter.GenericFilterBean;
import tictactoe.domain.service.AuthService;

import java.io.IOException;
import java.util.UUID;

public class AuthFilter extends GenericFilterBean {
    public static final String CURRENT_USER_ID_ATTR = "currentUserId";

    private final AuthService authService;

    public AuthFilter(AuthService authService) {
        this.authService = authService;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String path = httpRequest.getRequestURI();
        if (isPublicPath(path)) {
            chain.doFilter(request, response);
            return;
        }

        String authHeader = httpRequest.getHeader("Authorization");
        UUID userId = authService.authorize(authHeader);

        if (userId == null) {
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return; // НЕ вызываем chain.doFilter — запрос не доходит до контроллера
        }

        httpRequest.setAttribute(CURRENT_USER_ID_ATTR, userId);
        chain.doFilter(request, response);
    }

    private static boolean isPublicPath(String path) {
        if ("/auth/register".equals(path) || "/auth/login".equals(path)) {
            return true;
        }
        if ("/".equals(path) || "/index.html".equals(path) || "/game.html".equals(path)) {
            return true;
        }
        return path.startsWith("/css/") || path.startsWith("/js/")
                || path.endsWith(".txt"); // test.txt при проверке шага 6.1
    }
}

//фильтр стоит до контроллера. Нет auth → 401, запрос не доходит до GameController.
// Есть auth → кладём userId в request attribute — в PvP (Задание 3) оттуда узнаем «кто ходит».'''

SECURITY_CONFIG = r'''package tictactoe.di;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import tictactoe.domain.service.AuthService;
import tictactoe.web.filter.AuthFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public AuthFilter authFilter(AuthService authService) {
        return new AuthFilter(authService);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http, AuthFilter authFilter) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/auth/register", "/auth/login").permitAll()
                        .requestMatchers(
                                "/",
                                "/index.html",
                                "/game.html",
                                "/css/**",
                                "/js/**"
                        ).permitAll()
                        .anyRequest().permitAll()
                )
                .addFilterBefore(authFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
//csrf.disable() — REST API без форм, CSRF не нужен
//permitAll для /auth/register, /auth/login — без Authorization
//anyRequest().permitAll() — Spring Security не дублирует проверку; 401/403 даёт AuthFilter
//addFilterBefore — наш фильтр в цепочке Spring Security
//Spring Security по умолчанию блокирует всё. Мы открываем только register/login, остальное — через наш AuthFilter.
// csrf.disable() — для REST без браузерных форм.

//permitAll — без заголовка Authorization
//game/** API не в списке — ходы по-прежнему только с Basic Auth
//Статику открываем, API — защищаем'''

USER_DTO = r'''package tictactoe.web.model;

import java.util.UUID;

public class UserDto {

    private UUID id;
    private String login;

    public UserDto() {
    }

    public UserDto(UUID id, String login) {
        this.id = id;
        this.login = login;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }
}
'''

USER_CONTROLLER = r'''package tictactoe.web.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.service.UserService;
import tictactoe.web.model.UserDto;

import java.util.UUID;

@RestController
@RequestMapping("/user")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{userId}")
    public ResponseEntity<?> getUser(@PathVariable UUID userId) {
        return userService.findLoginById(userId)
                .map(login -> ResponseEntity.ok(new UserDto(userId, login)))
                .orElse(ResponseEntity.notFound().build());
    }
}
// GET /user/{uuid} — посмотреть login по id (например, узнать ник соперника). Пароль не отдаём — только UserDto.'''

GAME_STATE = r'''package tictactoe.domain.model;

public enum GameState {
    WAITING_FOR_PLAYERS, // ждём второго игрока
    PLAYER_TURN, // ход игрока
    DRAW, // ничья
    WIN //Победа
}'''

SYMBOL = r'''package tictactoe.domain.model;

public enum Symbol {
    X, O;

    public int toBoardValue() {
        return this == X ? 1 : 2;
    }

    public static Symbol fromBoardValue(int value) {
        return value == 1 ? X : O;
    }
}
// Меняем крестики и нолики на 1 и 2 И наоборот'''

CURRENT_GAME_FULL = r'''package tictactoe.domain.model;

import java.util.UUID;

public class CurrentGame {

    private final UUID id;
    private final GameBoard board;
    private final GameState state;
    private final UUID player1Id;
    private final UUID player2Id;           // null если vsComputer или ждём игрока
    private final Symbol player1Symbol;
    private final Symbol player2Symbol;
    private final UUID currentTurnPlayerId; // чей ход (при PLAYER_TURN)
    private final UUID winnerId;            // кто победил (при WIN)
    private final boolean vsComputer;

    public CurrentGame(UUID id, GameBoard board, GameState state,
                       UUID player1Id, UUID player2Id,
                       Symbol player1Symbol, Symbol player2Symbol,
                       UUID currentTurnPlayerId, UUID winnerId,
                       boolean vsComputer) {
        this.id = id;
        this.board = board;
        this.state = state;
        this.player1Id = player1Id;
        this.player2Id = player2Id;
        this.player1Symbol = player1Symbol;
        this.player2Symbol = player2Symbol;
        this.currentTurnPlayerId = currentTurnPlayerId;
        this.winnerId = winnerId;
        this.vsComputer = vsComputer;
    }

    /** Упрощённый конструктор для обратной совместимости (T03) */
    public CurrentGame(UUID id, GameBoard board) {
        this(id, board, GameState.PLAYER_TURN,
                null, null, Symbol.X, Symbol.O,
                null, null, true);
    }

    public UUID getId() { return id; }
    public GameBoard getBoard() { return board; }
    public GameState getState() { return state; }
    public UUID getPlayer1Id() { return player1Id; }
    public UUID getPlayer2Id() { return player2Id; }
    public Symbol getPlayer1Symbol() { return player1Symbol; }
    public Symbol getPlayer2Symbol() { return player2Symbol; }
    public UUID getCurrentTurnPlayerId() { return currentTurnPlayerId; }
    public UUID getWinnerId() { return winnerId; }
    public boolean isVsComputer() { return vsComputer; }

    public CurrentGame withBoard(GameBoard newBoard) {
        return new CurrentGame(id, newBoard, state, player1Id, player2Id,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withState(GameState newState) {
        return new CurrentGame(id, board, newState, player1Id, player2Id,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withCurrentTurn(UUID turnPlayerId) {
        return new CurrentGame(id, board, state, player1Id, player2Id,
                player1Symbol, player2Symbol, turnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withPlayer2(UUID p2) {
        return new CurrentGame(id, board, state, player1Id, p2,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withWinner(UUID winner) {
        return new CurrentGame(id, board, GameState.WIN, player1Id, player2Id,
                player1Symbol, player2Symbol, null, winner, vsComputer);
    }

    public CurrentGame asDraw() {
        return new CurrentGame(id, board, GameState.DRAW, player1Id, player2Id,
                player1Symbol, player2Symbol, null, null, vsComputer);
    }

    /** UUID игрока, у которого symbol X или O */
    public UUID getPlayerIdBySymbol(Symbol symbol) {
        if (symbol == player1Symbol) return player1Id;
        if (symbol == player2Symbol) return player2Id;
        return null;
    }

    public Symbol getSymbolByPlayerId(UUID playerId) {
        if (playerId != null && playerId.equals(player1Id)) return player1Symbol;
        if (playerId != null && playerId.equals(player2Id)) return player2Symbol;
        return null;
    }
}

// раньше игра = id + доска. Теперь ещё игроки, символы, чей ход,
// победитель, PvE или PvP. Методы withBoard, withState… — immutable-стиль:
// не мутируем объект, а создаём копию с изменением (удобно в сервисе).'''

GAME_SERVICE = r'''package tictactoe.domain.service;

import tictactoe.domain.model.CurrentGame;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface GameService {

    CurrentGame createGame(UUID creatorId, boolean vsComputer);

    List<CurrentGame> getAvailableGames();

    CurrentGame joinGame(UUID gameId, UUID playerId);

    Optional<CurrentGame> getGame(UUID gameId);

    CurrentGame makeMove(UUID gameId, CurrentGame incoming, UUID playerId);

    void saveGame(CurrentGame game);

    // --- методы T03 (Minimax PvE) ---
    CurrentGame getNextMove(CurrentGame game);
    CurrentGame getFirstMove(CurrentGame game);
    boolean validateBoard(CurrentGame stored, CurrentGame incoming, UUID playerId);
    CurrentGame updateGameState(CurrentGame game);
}'''

GAME_SERVICE_IMPL = r'''package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;
import tictactoe.domain.service.GameService;
import tictactoe.datasource.mapper.GameMapper;
import tictactoe.datasource.repository.GameRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class GameServiceImpl implements GameService {

    private final GameRepository gameRepository;

    public GameServiceImpl(GameRepository gameRepository) {
        this.gameRepository = gameRepository;
    }

    @Override
    public void saveGame(CurrentGame game) {
        gameRepository.save(GameMapper.toEntity(game));
    }

    @Override
    public CurrentGame createGame(UUID creatorId, boolean vsComputer) {
        UUID gameId = UUID.randomUUID();
        GameBoard emptyBoard = new GameBoard();

        if (vsComputer) {
            return new CurrentGame(
                    gameId, emptyBoard,
                    GameState.PLAYER_TURN,
                    creatorId, null,
                    Symbol.X, Symbol.O,
                    creatorId,
                    null,
                    true
            );
        }

        return new CurrentGame(
                gameId, emptyBoard,
                GameState.WAITING_FOR_PLAYERS,
                creatorId, null,
                Symbol.X, Symbol.O,
                null, null,
                false
        );
    }

    @Override
    public List<CurrentGame> getAvailableGames() {
        return gameRepository.findByState(GameState.WAITING_FOR_PLAYERS)
                .stream()
                .map(GameMapper::toDomain)
                .toList();
    }

    @Override
    public CurrentGame joinGame(UUID gameId, UUID playerId) {
        CurrentGame game = getGame(gameId)
                .orElseThrow(() -> new IllegalArgumentException("Game not found"));

        if (game.getState() != GameState.WAITING_FOR_PLAYERS) {
            throw new IllegalStateException("Game is not waiting for players");
        }
        if (game.getPlayer1Id().equals(playerId)) {
            throw new IllegalStateException("Cannot join your own game");
        }

        return new CurrentGame(
                game.getId(), game.getBoard(),
                GameState.PLAYER_TURN,
                game.getPlayer1Id(), playerId,
                game.getPlayer1Symbol(), Symbol.O,
                game.getPlayer1Id(),
                null,
                false
        );
    }

    @Override
    public Optional<CurrentGame> getGame(UUID gameId) {
        return gameRepository.findById(gameId).map(GameMapper::toDomain);
    }

    @Override
    public CurrentGame makeMove(UUID gameId, CurrentGame incoming, UUID playerId) {
        CurrentGame stored = getGame(gameId)
                .orElseThrow(() -> new IllegalArgumentException("Game not found"));

        if (stored.getState() != GameState.PLAYER_TURN) {
            throw new IllegalStateException("Game is not in progress");
        }
        if (!playerId.equals(stored.getCurrentTurnPlayerId())) {
            throw new IllegalStateException("Not your turn");
        }
        if (!validateBoard(stored, incoming, playerId)) {
            throw new IllegalStateException("Invalid board");
        }

        CurrentGame afterPlayerMove = stored.withBoard(incoming.getBoard());
        CurrentGame afterPlayerMoveChecked = updateGameState(afterPlayerMove);

        if (afterPlayerMoveChecked.getState() == GameState.WIN
                || afterPlayerMoveChecked.getState() == GameState.DRAW) {
            return afterPlayerMoveChecked;
        }

        if (stored.isVsComputer()) {
            CurrentGame afterComputer = getNextMove(afterPlayerMoveChecked);
            return updateGameState(afterComputer);
        }

        UUID nextPlayer = stored.getPlayer1Id().equals(playerId)
                ? stored.getPlayer2Id()
                : stored.getPlayer1Id();

        return updateGameState(afterPlayerMoveChecked.withCurrentTurn(nextPlayer));
    }

    @Override
    public CurrentGame getFirstMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        board.set(1, 1, GameBoard.COMPUTER);
        CurrentGame afterComputer = game.withBoard(board);
        return updateGameState(afterComputer.withCurrentTurn(game.getPlayer1Id()));
    }

    @Override
    public CurrentGame getNextMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        int[] bestMove = findBestMove(board);
        if (bestMove != null) {
            board.set(bestMove[0], bestMove[1], GameBoard.COMPUTER);
        }
        return game.withBoard(board);
    }

    @Override
    public boolean validateBoard(CurrentGame stored, CurrentGame incoming, UUID playerId) {
        Symbol playerSymbol = stored.getSymbolByPlayerId(playerId);
        if (playerSymbol == null) {
            return false;
        }
        int expectedValue = playerSymbol.toBoardValue();
        return boardsMatchExceptOneMove(stored.getBoard(), incoming.getBoard(), expectedValue);
    }

    @Override
    public CurrentGame updateGameState(CurrentGame game) {
        int winnerValue = evaluateWinner(game.getBoard());

        if (winnerValue != 0) {
            Symbol winnerSymbol = Symbol.fromBoardValue(winnerValue);
            UUID winnerId = game.getPlayerIdBySymbol(winnerSymbol);
            if (game.isVsComputer() && winnerSymbol == Symbol.O) {
                winnerId = null; // победа компьютера
            }
            return game.withWinner(winnerId);
        }

        if (isBoardFull(game.getBoard())) {
            return game.asDraw();
        }

        return game.withState(GameState.PLAYER_TURN);
    }

    private boolean boardsMatchExceptOneMove(GameBoard stored, GameBoard incoming, int expectedValue) {
        int diff = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                int s = stored.get(i, j);
                int inc = incoming.get(i, j);
                if (s != inc) {
                    if (s == GameBoard.EMPTY && inc == expectedValue) {
                        diff++;
                    } else {
                        return false;
                    }
                }
            }
        }
        return diff == 1;
    }

    private boolean isBoardFull(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    private int evaluateWinner(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            if (board.get(i, 0) != GameBoard.EMPTY
                    && board.get(i, 0) == board.get(i, 1)
                    && board.get(i, 1) == board.get(i, 2)) {
                return board.get(i, 0);
            }
            if (board.get(0, i) != GameBoard.EMPTY
                    && board.get(0, i) == board.get(1, i)
                    && board.get(1, i) == board.get(2, i)) {
                return board.get(0, i);
            }
        }
        if (board.get(0, 0) != GameBoard.EMPTY
                && board.get(0, 0) == board.get(1, 1)
                && board.get(1, 1) == board.get(2, 2)) {
            return board.get(0, 0);
        }
        if (board.get(0, 2) != GameBoard.EMPTY
                && board.get(0, 2) == board.get(1, 1)
                && board.get(1, 1) == board.get(2, 0)) {
            return board.get(0, 2);
        }
        return 0;
    }

    // --- Minimax (без изменений из T03) ---

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
        int score = evaluateMinimax(board);
        if (score == 10) return score - depth;
        if (score == -10) return score + depth;
        if (isBoardFull(board)) return 0;

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

    private int evaluateMinimax(GameBoard board) {
        int w = evaluateWinner(board);
        if (w == GameBoard.COMPUTER) return 10;
        if (w == GameBoard.PLAYER) return -10;
        return 0;
    }
}'''

CREATE_GAME_REQUEST = r'''package tictactoe.web.model;

public class CreateGameRequest {
    private boolean vsComputer;

    public CreateGameRequest(){}

    public boolean isVsComputer() {
        return vsComputer;
    }

    public void setVsComputer(boolean vsComputer) {
        this.vsComputer = vsComputer;
    }
}'''

CURRENT_GAME_DTO = r'''package tictactoe.web.model;

import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;

import java.util.UUID;

public class CurrentGameDto {

    private UUID id;
    private GameBoardDto board;
    private GameState state;
    private UUID player1Id;
    private UUID player2Id;
    private Symbol player1Symbol;
    private Symbol player2Symbol;
    private UUID currentTurnPlayerId;
    private UUID winnerId;
    private boolean vsComputer;
    private Boolean computerStarts; // legacy для PvE «играю за O»

    public CurrentGameDto() {
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public GameBoardDto getBoard() { return board; }
    public void setBoard(GameBoardDto board) { this.board = board; }

    public GameState getState() { return state; }
    public void setState(GameState state) { this.state = state; }

    public UUID getPlayer1Id() { return player1Id; }
    public void setPlayer1Id(UUID player1Id) { this.player1Id = player1Id; }

    public UUID getPlayer2Id() { return player2Id; }
    public void setPlayer2Id(UUID player2Id) { this.player2Id = player2Id; }

    public Symbol getPlayer1Symbol() { return player1Symbol; }
    public void setPlayer1Symbol(Symbol player1Symbol) { this.player1Symbol = player1Symbol; }

    public Symbol getPlayer2Symbol() { return player2Symbol; }
    public void setPlayer2Symbol(Symbol player2Symbol) { this.player2Symbol = player2Symbol; }

    public UUID getCurrentTurnPlayerId() { return currentTurnPlayerId; }
    public void setCurrentTurnPlayerId(UUID currentTurnPlayerId) { this.currentTurnPlayerId = currentTurnPlayerId; }

    public UUID getWinnerId() { return winnerId; }
    public void setWinnerId(UUID winnerId) { this.winnerId = winnerId; }

    public boolean isVsComputer() { return vsComputer; }
    public void setVsComputer(boolean vsComputer) { this.vsComputer = vsComputer; }

    public Boolean getComputerStarts() { return computerStarts; }
    public void setComputerStarts(Boolean computerStarts) { this.computerStarts = computerStarts; }
}'''

GAME_WEB_MAPPER = r'''package tictactoe.web.mapper;

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
        CurrentGameDto dto = new CurrentGameDto();
        dto.setId(game.getId());
        dto.setBoard(toDto(game.getBoard()));
        dto.setState(game.getState());
        dto.setPlayer1Id(game.getPlayer1Id());
        dto.setPlayer2Id(game.getPlayer2Id());
        dto.setPlayer1Symbol(game.getPlayer1Symbol());
        dto.setPlayer2Symbol(game.getPlayer2Symbol());
        dto.setCurrentTurnPlayerId(game.getCurrentTurnPlayerId());
        dto.setWinnerId(game.getWinnerId());
        dto.setVsComputer(game.isVsComputer());
        return dto;
    }

    public static CurrentGame toDomain(CurrentGameDto dto) {
        if (dto == null) {
            return null;
        }
        GameBoard board = toDomainBoard(dto.getBoard());
        return new CurrentGame(
                dto.getId(),
                board,
                dto.getState() != null ? dto.getState() : tictactoe.domain.model.GameState.PLAYER_TURN,
                dto.getPlayer1Id(),
                dto.getPlayer2Id(),
                dto.getPlayer1Symbol() != null ? dto.getPlayer1Symbol() : tictactoe.domain.model.Symbol.X,
                dto.getPlayer2Symbol() != null ? dto.getPlayer2Symbol() : tictactoe.domain.model.Symbol.O,
                dto.getCurrentTurnPlayerId(),
                dto.getWinnerId(),
                dto.isVsComputer()
        );
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
}

// DTO — то, что уходит/приходит по HTTP. CreateGameRequest — только флаг PvE/PvP.
// CurrentGameDto — полная картина для клиента. GameWebMapper — мост web ↔ domain
// (не путать с GameMapper entity ↔ domain).'''

GAME_CONTROLLER = r'''package tictactoe.web.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.model.GameState;
import tictactoe.domain.service.GameService;
import tictactoe.web.filter.AuthFilter;
import tictactoe.web.mapper.GameWebMapper;
import tictactoe.web.model.CreateGameRequest;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.ErrorResponse;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/game")
public class GameController {

    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @PostMapping
    public ResponseEntity<?> createGame(@RequestBody CreateGameRequest request,
                                        HttpServletRequest httpRequest) {
        UUID userId = currentUserId(httpRequest);
        boolean vsComputer = request != null && request.isVsComputer();
        CurrentGame game = gameService.createGame(userId, vsComputer);
        gameService.saveGame(game);
        return ResponseEntity.ok(GameWebMapper.toDto(game));
    }

    @GetMapping("/available")
    public ResponseEntity<List<CurrentGameDto>> getAvailableGames() {
        List<CurrentGameDto> games = gameService.getAvailableGames()
                .stream()
                .map(GameWebMapper::toDto)
                .toList();
        return ResponseEntity.ok(games);
    }

    @PostMapping("/{gameId}/join")
    public ResponseEntity<?> joinGame(@PathVariable UUID gameId,
                                      HttpServletRequest httpRequest) {
        try {
            UUID userId = currentUserId(httpRequest);
            CurrentGame game = gameService.joinGame(gameId, userId);
            gameService.saveGame(game);
            return ResponseEntity.ok(GameWebMapper.toDto(game));
        } catch (IllegalArgumentException | IllegalStateException e) {
            return ResponseEntity.badRequest().body(new ErrorResponse(e.getMessage()));
        }
    }

    @GetMapping("/{gameId}")
    public ResponseEntity<?> getGame(@PathVariable UUID gameId) {
        return gameService.getGame(gameId)
                .map(g -> ResponseEntity.ok(GameWebMapper.toDto(g)))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{gameId}")
    public ResponseEntity<?> makeMove(@PathVariable UUID gameId,
                                      @RequestBody CurrentGameDto request,
                                      HttpServletRequest httpRequest) {
        if (request == null || request.getBoard() == null) {
            return ResponseEntity.badRequest()
                    .body(new ErrorResponse("Missing board"));
        }
        if (!gameId.equals(request.getId())) {
            return ResponseEntity.badRequest()
                    .body(new ErrorResponse("Game id mismatch"));
        }

        UUID userId = currentUserId(httpRequest);
        CurrentGame incoming = GameWebMapper.toDomain(request);

        if (Boolean.TRUE.equals(request.getComputerStarts()) && isBoardEmpty(incoming.getBoard())) {
            return gameService.getGame(gameId)
                    .map(stored -> {
                        CurrentGame afterFirst = gameService.getFirstMove(stored);
                        gameService.saveGame(afterFirst);
                        return ResponseEntity.ok(GameWebMapper.toDto(afterFirst));
                    })
                    .orElse(ResponseEntity.notFound().build());
        }

        try {
            CurrentGame result = gameService.makeMove(gameId, incoming, userId);
            gameService.saveGame(result);
            return ResponseEntity.ok(GameWebMapper.toDto(result));
        } catch (IllegalStateException e) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                    .body(new ErrorResponse(e.getMessage()));
        }
    }

    private static UUID currentUserId(HttpServletRequest request) {
        return (UUID) request.getAttribute(AuthFilter.CURRENT_USER_ID_ATTR);
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
}

// контроллер достаёт userId из AuthFilter.
// CURRENT_USER_ID_ATTR — без этого не узнаешь,
// кто создаёт игру или ходит. Новые маршруты:
// POST /game, GET /game/available, POST /game/{id}/join, GET /game/{id} плюс старый POST /game/{id} для хода.'''


def _svodka(add, title, code, lang="java"):
    add(f"### Сверка: файл целиком — `{title}`")
    add("")
    add(f"```{lang}")
    add(code.rstrip())
    add("```")
    add("")


def _theory(add, para_block, text):
    add("### Теория (прочитай до кода)")
    add("")
    para_block(text)


def _kartinа(add, lines_text):
    add("### Картина в голове")
    add("")
    for line in lines_text:
        add(line)
    add("")


def append_blocks(lines, add, block_header, micro_step, block_footer, para_block):
    """Append all C.1–C.8, D theory+D.1–D.9, E theory+E.1–E.8 blocks."""

    # ===================== BLOCK C.1 =====================
    block_header("C.1", "Установка PostgreSQL и базы `tictactoe`",
                 "Поднять СУБД локально и создать отдельную базу для проекта.", "20 мин", "★★☆")
    _theory(add, para_block, """
**Зачем отдельная СУБД.** На этапе B игра жила в оперативной памяти JVM — перезапуск Tomcat стирал все партии. PostgreSQL — промышленная реляционная СУБД: данные переживают рестарт сервера, их можно бэкапить и читать SQL-запросами. Для учебного проекта мы поднимаем один инстанс Postgres на `localhost:5432`.

**Установка.** Скачай установщик с [postgresql.org](https://www.postgresql.org/download/). На Windows запомни пароль суперпользователя `postgres` — он понадобится при первом входе. Служба `postgresql-x64-16` должна стартовать автоматически; проверь в `services.msc`, если `psql` отвечает `Connection refused`.

**База `tictactoe`.** Одна инстанция Postgres может держать много баз. `CREATE DATABASE tictactoe` выделяет изолированное пространство: таблицы `games` и `users` не смешаются с чужими проектами. URL в `application.properties` указывает именно на эту базу: `jdbc:postgresql://localhost:5432/tictactoe`.

**Порт 5432.** Это стандартный порт Postgres. `localhost` означает «этот компьютер»; в Docker или на удалённом сервере хост будет другим. Пока всё локально — не меняй порт без необходимости.

**Связь с Spring.** Spring Boot не создаёт базу сам — только таблицы внутри уже существующей БД. Если `tictactoe` не создана, при `bootRun` увидишь `FATAL: database "tictactoe" does not exist`. Создай базу один раз — дальше Hibernate займётся таблицами.
""")
    _kartinа(add, [
        "```",
        "PostgreSQL (localhost:5432)",
        "    └── database: tictactoe",
        "            └── (позже) tables: games, users",
        "```",
    ])
    micro_step(1, "Создать базу данных", "SQL-команду в psql или pgAdmin",
               "CREATE DATABASE tictactoe;",
               [("1", "CREATE DATABASE", "Создаёт пустую БД с именем tictactoe")])
    micro_step(2, "Проверить подключение", "Команду psql из терминала",
               'psql -U postgres -c "SELECT 1;"',
               [("1", "psql -U postgres", "Клиент PostgreSQL под пользователем postgres"),
                ("1", "SELECT 1", "Простейший запрос — если вернул 1, сервер жив")])
    _svodka(add, "CREATE DATABASE tictactoe", "CREATE DATABASE tictactoe;", "sql")
    block_footer(
        "Чем `localhost:5432` в URL отличается от имени базы `tictactoe`?",
        'psql -U postgres -c "SELECT 1;"\n# или\n& "C:\\Program Files\\PostgreSQL\\16\\bin\\psql.exe" -U postgres -c "SELECT 1;"',
        "psql -U postgres -c 'SELECT 1;'",
        "Connection refused → служба PostgreSQL не запущена. Database does not exist → выполни `CREATE DATABASE tictactoe`.",
        "Postgres слушает порт 5432, база `tictactoe` готова принять таблицы Spring.",
        "Блок **C.2** — добавим JPA и драйвер в `build.gradle.kts`.",
    )

    # ===================== BLOCK C.2 =====================
    block_header("C.2", "`build.gradle.kts` — JPA, Security, PostgreSQL",
                 "Заменить файл целиком: подключить Spring Data JPA, Security и JDBC-драйвер.", "10 мин", "★★☆")
    _theory(add, para_block, """
**Gradle как менеджер зависимостей.** Файл `build.gradle.kts` описывает, какие библиотеки попадут в classpath при компиляции и запуске. Spring Boot plugin подтягивает совместимые версии через BOM (Bill of Materials) — тебе не нужно вручную согласовывать Hibernate и Spring.

**spring-boot-starter-data-jpa.** Это «стартер»: одна строка тянет Hibernate, Spring Data JPA, транзакции, пул соединений HikariCP. После Reload IDE появятся аннотации `jakarta.persistence.*` и интерфейс `CrudRepository`.

**postgresql runtimeOnly.** JDBC-драйвер нужен только в runtime — при компиляции твой код не ссылается на классы драйвера напрямую. `runtimeOnly` кладёт jar в classpath `bootRun`, но не в compile classpath — чище и быстрее сборка.

**spring-boot-starter-security.** Понадобится уже на этапе D: без него нет `SecurityFilterChain` и цепочки фильтров. Добавляем сейчас, чтобы не пересобирать проект дважды. После добавления Spring Security по умолчанию блокирует все URL — на этапе D настроим исключения.

**Версия Java 17.** Spring Boot 3.x требует минимум Java 17. Блок `java { sourceCompatibility … }` гарантирует, что компилятор и bytecode согласованы с JDK на машине.
""")
    _kartinа(add, [
        "```",
        "build.gradle.kts",
        "  ├── starter-web        (Tomcat, Jackson, MVC)",
        "  ├── starter-data-jpa   (Hibernate, репозитории)",
        "  ├── starter-security   (фильтры, SecurityFilterChain)",
        "  └── postgresql         (JDBC-драйвер, runtime)",
        "```",
    ])
    micro_step(1, "Секция plugins", "Три плагина: java, spring-boot, dependency-management",
               'plugins {\n    id("java")\n    id("org.springframework.boot") version "3.2.0"\n    id("io.spring.dependency-management") version "1.1.4"\n}',
               [("2", "org.springframework.boot", "Плагин Spring Boot + управление версиями"),
                ("3", "dependency-management", "BOM для совместимых зависимостей")])
    micro_step(2, "Java 17", "Блок совместимости bytecode",
               "java {\n    sourceCompatibility = JavaVersion.VERSION_17\n    targetCompatibility = JavaVersion.VERSION_17\n}",
               [("2", "VERSION_17", "Минимум для Spring Boot 3.x")])
    micro_step(3, "Зависимости JPA и Postgres", "implementation data-jpa + runtimeOnly postgresql",
               'dependencies {\n    implementation("org.springframework.boot:spring-boot-starter-web")\n    implementation("org.springframework.boot:spring-boot-starter-data-jpa")\n    runtimeOnly("org.postgresql:postgresql")\n}',
               [("2", "starter-data-jpa", "Hibernate + Spring Data"),
                ("3", "runtimeOnly postgresql", "Драйвер только при запуске")])
    micro_step(4, "Spring Security", "Строку starter-security",
               '    implementation("org.springframework.boot:spring-boot-starter-security")',
               [("1", "starter-security", "Фильтры и SecurityFilterChain для этапа D")])
    _svodka(add, "build.gradle.kts", BUILD_GRADLE, "kotlin")
    block_footer(
        "Почему драйвер PostgreSQL — `runtimeOnly`, а не `implementation`?",
        ".\\gradlew.bat dependencies --configuration runtimeClasspath | Select-String postgresql",
        "./gradlew dependencies --configuration runtimeClasspath | grep postgresql",
        "Unresolved dependency → проверь интернет и `mavenCentral()`. Ошибка Java version → JDK 17+.",
        "Gradle тянет JPA, Security и драйвер Postgres.",
        "Блок **C.3** — `application.properties` с плейсхолдерами **ТВОЙ_ЛОГИН** / **ТВОЙ_ПАРОЛЬ**.",
    )

    # ===================== BLOCK C.3 =====================
    block_header("C.3", "`application.properties`",
                 "Настроить JDBC-подключение к Postgres (плейсхолдеры вместо реальных секретов).", "5 мин", "★☆☆")
    _theory(add, para_block, """
**application.properties — конфиг Spring Boot.** Файл лежит в `src/main/resources/` и попадает в jar без перекомпиляции. Свойства `spring.datasource.*` читает автоконфигурация DataSource: Spring создаёт пул HikariCP с указанным URL, логином и паролем.

**Плейсхолдеры ТВОЙ_ЛОГИН и ТВОЙ_ПАРОЛЬ.** Никогда не коммить реальный пароль Postgres в публичный репозиторий. В туториале пишем явные плейсхолдеры — замени их на свои credentials локально. Для school21 часто логин совпадает с ником в системе.

**ddl-auto=update.** Hibernate при старте сравнивает `@Entity` с реальными таблицами и добавляет недостающие колонки. Удобно для учёбы; в продакшене используют Flyway/Liquibase. Значение `create` пересоздаёт таблицы и **стирает данные** — не ставь его случайно.

**show-sql=true.** В консоли `bootRun` увидишь `Hibernate: insert into games …` — это помогает понять, что реально уходит в БД. На проде отключают — лишний шум и утечка структуры.

**Диалект PostgreSQL.** `hibernate.dialect=PostgreSQLDialect` подсказывает Hibernate генерировать SQL с синтаксисом Postgres (типы UUID, boolean и т.д.). Без диалекта Hibernate пытается угадать — на Postgres обычно угадывает, но явное указание надёжнее.
""")
    _kartinа(add, [
        "```",
        "application.properties  →  DataSource (HikariCP)  →  PostgreSQL",
        "spring.jpa.*            →  Hibernate (DDL, SQL-лог)",
        "```",
    ])
    micro_step(1, "Datasource URL и credentials", "Три строки spring.datasource.*",
               "spring.datasource.url=jdbc:postgresql://localhost:5432/tictactoe\nspring.datasource.username=ТВОЙ_ЛОГИН\nspring.datasource.password=ТВОЙ_ПАРОЛЬ",
               [("1", "jdbc:postgresql://…", "JDBC URL: хост, порт, имя базы"),
                ("2", "ТВОЙ_ЛОГИН", "Замени на своего пользователя Postgres")])
    micro_step(2, "JPA / Hibernate", "ddl-auto, show-sql, dialect",
               "spring.jpa.hibernate.ddl-auto=update\nspring.jpa.show-sql=true\nspring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect",
               [("1", "ddl-auto=update", "Авто-миграция схемы при старте"),
                ("2", "show-sql=true", "Печать SQL в консоль")])
    _svodka(add, "application.properties", APP_PROPERTIES, "properties")
    block_footer(
        "Что произойдёт с таблицей `games`, если добавить новое поле в entity при `ddl-auto=update`?",
        ".\\gradlew.bat bootRun\n# В логах ищи: HikariPool-1 - Start completed",
        "./gradlew bootRun",
        "FATAL: password authentication failed → проверь ТВОЙ_ЛОГИН/ТВОЙ_ПАРОЛЬ. database does not exist → CREATE DATABASE tictactoe.",
        "Spring видит Postgres; credentials — твои локальные.",
        "Блок **C.4** — `GameBoardEntity` с девятью колонками cell_XY.",
    )

    # ===================== BLOCK C.4 =====================
    block_header("C.4", "`GameBoardEntity.java` (JPA Embeddable)",
                 "Заменить целиком: доска 3×3 как встраиваемый объект с 9 колонками.", "20 мин", "★★★")
    _theory(add, para_block, """
**Проблема int[][] в JPA.** Hibernate умеет маппить примитивы и простые типы в колонки, но двумерный массив `int[][]` не ложится на реляционную модель напрямую. Варианты: JSON-колонка, отдельная таблица `cells`, или — наш путь — девять скалярных полей.

**@Embeddable vs @Entity.** `@Entity` создаёт отдельную таблицу. `@Embeddable` — «кусок» другой entity: колонки `cell_00`…`cell_22` физически лежат в таблице `games`, без JOIN. Это композиция, не агрегация с внешним ключом.

**Имена колонок @Column(name=…).** В Java поле `cell00`, в SQL — `cell_00`. Подчёркивание в имени колонки — читаемость в pgAdmin. Hibernate при `ddl-auto=update` создаст все девять колонок при первом старте.

**Метод set(row, col, value).** Switch по линейному индексу `row * SIZE + col` — единая точка записи в нужное поле. Маппер вызывает `setFromBoard(int[][])` для массового копирования из domain `GameBoard`.

**Связь с domain.** `GameBoardEntity` живёт в слое datasource; domain `GameBoard` по-прежнему использует `int[][]`. `GameMapper` переводит между ними — domain не знает про JPA.
""")
    _kartinа(add, [
        "```",
        "games (таблица)",
        "  id UUID",
        "  cell_00 … cell_22   ← @Embedded GameBoardEntity",
        "```",
    ])
    micro_step(1, "Аннотации и поля cell_*", "@Embeddable + 9 полей с @Column",
               '@Embeddable\npublic class GameBoardEntity {\n    @Column(name = "cell_00") private int cell00;\n    @Column(name = "cell_01") private int cell01;\n    // … cell_02 … cell_22',
               [("1", "@Embeddable", "Не отдельная таблица — часть games"),
                ("3", "@Column(name=\"cell_00\")", "Имя колонки в SQL")])
    micro_step(2, "Конструкторы и getCells", "Пустой конструктор + копирование из int[][]",
               "    public GameBoardEntity() {\n    }\n\n    public int[][] getCells() {\n        return new int[][]{\n                {cell00, cell01, cell02},\n                {cell10, cell11, cell12},\n                {cell20, cell21, cell22}\n        };\n    }",
               [("1", "GameBoardEntity()", "Нужен JPA/Hibernate"),
                ("4", "getCells()", "Собирает int[][] для domain")])
    micro_step(3, "setFromBoard и set(row,col)", "Массовое и точечное обновление ячеек",
               "    public void setFromBoard(int[][] cells) {\n        cell00 = cells[0][0]; cell01 = cells[0][1]; /* … */\n    }\n\n    public void set(int row, int col, int value) {\n        switch (row * GameBoard.SIZE + col) {\n            case 0 -> cell00 = value;\n            /* … */\n        }\n    }",
               [("1", "setFromBoard", "Маппер копирует доску целиком"),
                ("5", "switch", "Запись в одну ячейку по координатам")])
    _svodka(add, "GameBoardEntity.java", GAME_BOARD_ENTITY)
    block_footer(
        "Почему `@Embeddable`, а не отдельная `@Entity` для доски?",
        "# Компиляция после сохранения файла\n.\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "cannot find symbol GameBoard → проверь import domain.model.GameBoard.",
        "Доска маппится в 9 колонок таблицы games.",
        "Блок **C.5** — `CurrentGameEntity` (пока только id + board).",
    )

    # ===================== BLOCK C.5 =====================
    block_header("C.5", "`CurrentGameEntity.java` (JPA Entity, этап C)",
                 "Таблица games: UUID первичный ключ и вложенная доска.", "15 мин", "★★☆")
    _theory(add, para_block, """
**@Entity — строка таблицы games.** Каждый экземпляр `CurrentGameEntity` соответствует одной строке в PostgreSQL. Первичный ключ — `UUID id`, тот же идентификатор, что клиент видит в URL `/game/{uuid}`.

**@Embedded board.** Поле типа `GameBoardEntity` встраивает девять колонок `cell_*` в ту же строку. Hibernate не создаёт таблицу `game_board_entity` — только расширяет `games`.

**Минимальная версия на этапе C.** Пока храним только `id` и `board` — этого достаточно, чтобы T03-подобный PvE переживал рестарт. Поля PvP (`player1Id`, `state`, …) добавим на этапе E; Hibernate потом сделает `ALTER TABLE` благодаря `ddl-auto=update`.

**Пустой конструктор.** JPA требует no-arg constructor для создания прокси и десериализации из ResultSet. В конструкторе инициализируем `board = new GameBoardEntity()`, чтобы не получить NPE при первом save.

**Геттеры/сеттеры.** Hibernate читает и пишет поля через рефлексию; публичные accessor'ы — стандартный стиль и удобство для маппера.
""")
    _kartinа(add, [
        "```",
        "CurrentGameEntity",
        "  @Id UUID id",
        "  @Embedded GameBoardEntity board  →  cell_00…cell_22",
        "```",
    ])
    micro_step(1, "Аннотации класса", "@Entity, @Table(name=\"games\")",
               '@Entity\n@Table(name = "games")\npublic class CurrentGameEntity {',
               [("1", "@Entity", "JPA-сущность — строка в БД"),
                ("2", "@Table(name=\"games\")", "Имя таблицы в Postgres")])
    micro_step(2, "Поля id и board", "@Id UUID + @Embedded доска",
               "    @Id\n    private UUID id;\n\n    @Embedded\n    private GameBoardEntity board;",
               [("2", "@Id", "Первичный ключ"),
                ("5", "@Embedded", "Встроенная доска — 9 колонок")])
    micro_step(3, "Конструктор и accessors", "Инициализация board, геттеры/сеттеры",
               "    public CurrentGameEntity() {\n        this.board = new GameBoardEntity();\n    }\n\n    public UUID getId() { return id; }\n    public void setId(UUID id) { this.id = id; }",
               [("2", "new GameBoardEntity()", "Пустая доска по умолчанию"),
                ("6", "getId/setId", "Доступ для маппера и Hibernate")])
    _svodka(add, "CurrentGameEntity.java (этап C)", CURRENT_GAME_ENTITY_C)
    block_footer(
        "Где физически лежат колонки cell_00 — в отдельной таблице или внутри games?",
        ".\\gradlew.bat bootRun\n# В логах Hibernate: create table games (...)",
        "./gradlew bootRun",
        "Table doesn't exist после первого старта → проверь ddl-auto=update и подключение к БД.",
        "Entity games с id и вложенной доской готова.",
        "Блок **C.6** — `GameRepository` на Spring Data JPA.",
    )

    # ===================== BLOCK C.6 =====================
    block_header("C.6", "`GameRepository.java` (Spring Data)",
                 "Заменить интерфейс: CrudRepository вместо ручного GameRepositoryImpl.", "10 мин", "★★☆")
    _theory(add, para_block, """
**Паттерн Repository.** Слой datasource скрывает детали хранения от `GameServiceImpl`. На этапе B ты писал `GameRepositoryImpl` с `HashMap`. Теперь Spring Data JPA генерирует реализацию в runtime — писать SQL вручную не нужно.

**CrudRepository<Entity, Id>.** Интерфейс из Spring Data даёт `save`, `findById`, `findAll`, `deleteById` без единой строки кода. Типы `CurrentGameEntity` и `UUID` говорят фреймворку, с какой таблицей и ключом работать.

**Query methods по имени.** `findByState(GameState state)` превращается в `SELECT * FROM games WHERE state = ?`. Правило: `findBy` + имя поля entity в camelCase. Метод понадобится на этапе E для лобби `GET /game/available`.

**Удали GameRepositoryImpl.** Два бина репозитория вызовут конфликт. После удаления impl убедись, что `GameServiceImpl` инжектит интерфейс `GameRepository` — Spring подставит прокси JPA.

**Транзакции.** `save()` в Spring Data JPA по умолчанию `@Transactional` — одна операция INSERT/UPDATE в рамках транзакции. Для учебного проекта этого достаточно.
""")
    _kartinа(add, [
        "```",
        "GameServiceImpl  →  GameRepository (интерфейс)",
        "                         ↓",
        "              Spring Data JPA (прокси)  →  SQL  →  games",
        "```",
    ])
    micro_step(1, "Объявление интерфейса", "extends CrudRepository",
               "public interface GameRepository extends CrudRepository<CurrentGameEntity, UUID>{",
               [("1", "CrudRepository<…>", "CRUD из коробки"),
                ("1", "CurrentGameEntity, UUID", "Тип entity и тип @Id")])
    micro_step(2, "Метод findByState", "Query method для лобби (этап E)",
               "    List<CurrentGameEntity> findByState(GameState state);",
               [("1", "findByState", "Spring генерирует WHERE state = ?")])
    micro_step(3, "Удалить impl", "Файл GameRepositoryImpl.java — в корзину",
               "# Удали src/.../GameRepositoryImpl.java\n# Оставь только интерфейс GameRepository.java",
               [("1", "удалить impl", "Один бин репозитория — только JPA")])
    _svodka(add, "GameRepository.java", GAME_REPOSITORY)
    block_footer(
        "Кто теперь создаёт реализацию GameRepository — ты или Spring?",
        "# Убедись, что GameRepositoryImpl удалён\n.\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "BeanDefinitionOverrideException → где-то остался старый @Repository impl.",
        "JPA-репозиторий объявлен; impl из этапа B больше не нужен.",
        "Блок **C.7** — обновить `GameMapper` под Embeddable.",
    )

    # ===================== BLOCK C.7 =====================
    block_header("C.7", "`GameMapper.java` — под Embeddable",
                 "Заменить целиком: маппинг через setFromBoard и entity-сеттеры.", "10 мин", "★★☆")
    _theory(add, para_block, """
**Два мира: domain и entity.** `CurrentGame` в domain — чистая Java-модель без JPA. `CurrentGameEntity` — то же для Hibernate. `GameMapper` — единственный мост между ними в слое datasource. Web-слой использует отдельный `GameWebMapper` (этап E).

**toEntity: сеттеры вместо конструктора.** JPA entity часто требует пустой конструктор; поэтому создаём `new CurrentGameEntity()` и вызываем `setId`, `setBoard`. Так Hibernate может подгрузить объект из БД и заполнить поля.

**toEntityBoard и setFromBoard.** `GameBoard` domain хранит `int[][]`; entity — девять int-полей. `entity.setFromBoard(board.getCells())` копирует массив в колонки. Обратно — `new GameBoard(entity.getCells())`.

**Упрощённый toDomain на этапе C.** Пока в entity только id и board — `new CurrentGame(entity.getId(), board)` вызывает совместимый конструктор T03. На этапе E расширим маппер под все поля PvP.

**Статический utility-класс.** `private GameMapper() {}` — запрет инстанцирования. Все методы static — вызываем `GameMapper.toEntity(game)` без бина Spring.
""")
    _kartinа(add, [
        "```",
        "CurrentGame (domain)  ←→  GameMapper  ←→  CurrentGameEntity (JPA)",
        "GameBoard             ←→  toEntityBoard / toDomainBoard",
        "```",
    ])
    micro_step(1, "toDomain", "entity → domain через toDomainBoard",
               "    public static CurrentGame toDomain(CurrentGameEntity entity) {\n        if (entity == null) return null;\n        GameBoard board = toDomainBoard(entity.getBoard());\n        return new CurrentGame(entity.getId(), board);\n    }",
               [("3", "toDomainBoard", "GameBoardEntity → GameBoard"),
                ("4", "new CurrentGame(id, board)", "Конструктор T03-совместимости")])
    micro_step(2, "toEntity", "domain → entity, setter-стиль",
               "    public static CurrentGameEntity toEntity(CurrentGame game) {\n        if (game == null) return null;\n        CurrentGameEntity entity = new CurrentGameEntity();\n        entity.setId(game.getId());\n        entity.setBoard(toEntityBoard(game.getBoard()));\n        return entity;\n    }",
               [("3", "new CurrentGameEntity()", "Пустой entity для JPA"),
                ("5", "setBoard(toEntityBoard(...))", "Вложенная доска")])
    micro_step(3, "toEntityBoard", "setFromBoard из int[][]",
               "    public static GameBoardEntity toEntityBoard(GameBoard board) {\n        if (board == null) return null;\n        GameBoardEntity entity = new GameBoardEntity();\n        entity.setFromBoard(board.getCells());\n        return entity;\n    }",
               [("3", "setFromBoard", "Копия ячеек в cell_*")])
    _svodka(add, "GameMapper.java (этап C)", GAME_MAPPER_C)
    block_footer(
        "Почему в toEntity используем сеттеры, а не один большой конструктор?",
        ".\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "NullPointerException в маппере → проверь null-check в начале каждого метода.",
        "Маппер совместим с Embeddable-доской.",
        "Блок **C.8** — удалить memory-слой и упростить SpringConfig.",
    )

    # ===================== BLOCK C.8 =====================
    block_header("C.8", "Удалить memory-слой, упростить SpringConfig",
                 "GameStorage и GameRepositoryImpl — удалить; бины через @Service и Spring Data.", "10 мин", "★☆☆")
    _theory(add, para_block, """
**Конец эпохи HashMap.** `GameStorage` и `GameRepositoryImpl` из этапа B хранили игры в `ConcurrentHashMap`. После перехода на JPA они не только лишние — их наличие создаст дублирующие бины и путаницу, куда реально пишутся данные.

**Автоконфигурация Spring Boot.** `@Service` на `GameServiceImpl` и интерфейс `GameRepository extends CrudRepository` регистрируются component-scan'ом. Явный `@Bean GameRepository` в `SpringConfig` больше не нужен — как и `@Bean GameService`.

**Пустой SpringConfig.** Класс с `@Configuration` можно оставить пустым «на вырост» или для будущих `@Bean`. Главное — убрать ручную сборку графа, которую Spring Data уже делает сам.

**Проверка персистентности.** Сыграй партию T03, перезапусти `bootRun`, сделай ход с тем же UUID — игра должна подгрузиться из Postgres. Если после рестарта 404 — save идёт не в JPA.

**GameServiceImpl @Service.** Убедись, что на классе есть `@Service` (добавится явно на этапе E, если ещё нет). Без аннотации Spring не создаст бин сервиса.
""")
    _kartinа(add, [
        "```",
        "УДАЛИТЬ: GameStorage.java, GameRepositoryImpl.java",
        "ОСТАВИТЬ: SpringConfig { }  — пустая @Configuration",
        "GameServiceImpl @Service  +  GameRepository (JPA)",
        "```",
    ])
    micro_step(1, "Удалить файлы памяти", "GameStorage.java, GameRepositoryImpl.java",
               "# Удали:\n#   datasource/storage/GameStorage.java\n#   datasource/repository/GameRepositoryImpl.java",
               [("1", "GameStorage", "In-memory больше не используется")])
    micro_step(2, "Упростить SpringConfig", "Пустой @Configuration",
               '@Configuration\npublic class SpringConfig {\n}',
               [("1", "@Configuration", "Класс конфигурации остаётся"),
                ("2", "пустое тело", "Бины — автоматически")])
    micro_step(3, "Проверка save через JPA", "GameServiceImpl должен вызывать repository.save",
               "    public void saveGame(CurrentGame game) {\n        gameRepository.save(GameMapper.toEntity(game));\n    }",
               [("2", "repository.save", "Персистентность в Postgres")])
    _svodka(add, "SpringConfig.java", SPRING_CONFIG)
    block_footer(
        "Кто теперь создаёт бин GameRepository?",
        "# Удали memory-файлы, затем:\n.\\gradlew.bat bootRun\n# Сыграй ход, рестарт, тот же UUID — игра жива",
        "./gradlew bootRun",
        "Table doesn't exist → ddl-auto=update. No qualifying bean → проверь @Service и CrudRepository.",
        "**Этап C выполнен:** данные в PostgreSQL.",
        "Переходи к **этапу D** — пользователи и Basic Auth.",
    )

    # ===================== STAGE D THEORY =====================
    add("")
    add("# ЭТАП D — Задание 2: пользователи и Basic Auth")
    add("")
    add("> После этого этапа `POST /game` без заголовка `Authorization` → **401**. Регистрация и логин — публичные.")
    add("")
    _theory(add, para_block, """
**Идентификация, аутентификация, авторизация — три разных вопроса.** Идентификация: «кто ты?» — логин `alice`. Аутентификация: «докажи» — пароль `secret` или заголовок Basic Auth. Авторизация: «что тебе можно?» — например, ходить только в свою очередь. В T04 этап D закрывает первые два; проверка «твой ход» — на этапе E в `GameServiceImpl`.

**RFC 7617 — HTTP Basic Authentication.** Клиент шлёт заголовок `Authorization: Basic <base64>`, где base64 — это `логин:пароль` в UTF-8. Пример: `alice:secret` → байты → Base64 → `YWxpY2U6c2VjcmV0` → полный заголовок `Authorization: Basic YWxpY2U6c2VjcmV0`. Base64 — **не шифрование**, любой декодирует за секунду. В продакшене Basic Auth только поверх HTTPS.

**Цепочка фильтров (filter chain).** Запрос Tomcat проходит цепочку `Filter` до `DispatcherServlet` и контроллера. Наш `AuthFilter` стоит **до** контроллера: нет валидного auth → `401` и `return` без `chain.doFilter`. Есть auth → кладём `userId` в `request.setAttribute` и пускаем дальше. `GameController` читает этот attribute — «кто создаёт игру».

**401 Unauthorized vs 403 Forbidden.** **401** — «не представился или неверный пароль»: нет заголовка, опечатка `Autorization`, неверный Base64. **403** — «личность известна, но доступ запрещён»: типичная ошибка — поставить `anyRequest().authenticated()` в Spring Security без настройки SecurityContext: Spring видит «не аутентифицирован» и даёт 403 даже с правильным Basic Auth. У нас проверку делает **наш** AuthFilter; в SecurityConfig — `permitAll()` + `addFilterBefore`.

**Таблица users и plain text пароль.** Учебный проект хранит пароль как строку без bcrypt. В реальности — хеш + salt. `UserEntity` в datasource; domain знает только `UserService.register/authenticate`. Пароль никогда не попадает в `UserDto` для клиента.

**Публичные пути isPublicPath.** `/auth/register`, `/auth/login`, статика `/css/**`, `/js/**` проходят без Authorization. Дублируем логику в `SecurityConfig.requestMatchers().permitAll()` **и** в `AuthFilter.isPublicPath` — иначе один слой заблокирует то, что другой открыл.
""")
    _kartinа(add, [
        "```",
        "HTTP Request",
        "    → Spring Security (permitAll / csrf off)",
        "    → AuthFilter (401 или userId в attribute)",
        "    → GameController / AuthController",
        "```",
        "",
        "**Base64 пример:** `alice:secret` → `YWxpY2U6c2VjcmV0`",
    ])
    add("---")
    add("")

    # ===================== BLOCK D.1 =====================
    block_header("D.1", "`UserEntity.java`",
                 "JPA-сущность пользователя: login уникален, пароль в колонке password.", "15 мин", "★★☆")
    _theory(add, para_block, """
**Пользователь как отдельная таблица.** `users` не связана внешним ключом с `games` на уровне JPA — мы храним `UUID player1Id` в игре как скаляр. Это гибче: один пользователь — много игр.

**@Column(unique = true) на login.** База данных гарантирует уникальность: второй `register` с тем же логином получит ошибку на уровне `existsByLogin` в сервисе. Два пользователя с логином `alice` невозможны.

**UUID как @Id.** Как и у игры — случайный UUID при регистрации. Клиент после login получает UUID в теле ответа и использует его в логике игры; в заголовках по-прежнему login:password.

**Пароль в datasource, не в web DTO.** `UserDto` на этапе D.9 отдаёт только id и login. Утечка пароля через API исключена архитектурно.

**Hibernate создаёт таблицу.** При первом `bootRun` после добавления entity увидишь `create table users` в логах — аналогично `games` на этапе C.
""")
    _kartinа(add, ["```", "users", "  id UUID PK", "  login VARCHAR UNIQUE", "  password VARCHAR", "```"])
    micro_step(1, "Аннотации и поля", "@Entity, @Table(users), id, login, password",
               '@Entity\n@Table(name = "users")\npublic class UserEntity {\n    @Id\n    private UUID id;\n    @Column(nullable = false, unique = true)\n    private String login;\n    @Column(nullable = false)\n    private String password;',
               [("2", "@Table(users)", "Отдельная таблица"),
                ("5", "unique = true", "Уникальный логин")])
    micro_step(2, "Конструкторы и accessors", "no-arg + (id, login, password)",
               "    public UserEntity(UUID id, String login, String password) {\n        this.id = id;\n        this.login = login;\n        this.password = password;\n    }",
               [("1", "UserEntity(...)", "Удобно при register в сервисе")])
    _svodka(add, "UserEntity.java", USER_ENTITY)
    block_footer(
        "Почему пароль хранится в entity datasource, а не в domain CurrentGame?",
        ".\\gradlew.bat bootRun\n# Ищи: create table users",
        "./gradlew bootRun",
        "unique constraint violation при register → логин уже занят.",
        "Таблица users готова к регистрации.",
        "Блок **D.2** — `UserRepository`.",
    )

    # ===================== BLOCK D.2 =====================
    block_header("D.2", "`UserRepository.java`",
                 "Spring Data: findByLogin и existsByLogin.", "10 мин", "★☆☆")
    _theory(add, para_block, """
**Симметрия с GameRepository.** Тот же паттерн: интерфейс, Spring генерирует SQL. Для пользователей нужны не только CRUD, но и поиск по логину — имя метода описывает запрос.

**Optional<UserEntity> findByLogin.** Если логин не найден — `Optional.empty()`, без null и NPE. `authenticate` в сервисе делает `.filter(user -> password.equals(...))`.

**boolean existsByLogin.** Быстрая проверка перед insert при register. Возвращает true/false без загрузки всей entity — Spring Data оптимизирует в `SELECT EXISTS` или `COUNT`.

**Никакого UserRepositoryImpl.** Как и с играми — одна декларация интерфейса. Ошибка «expected single matching bean» означает, что где-то осталась ручная реализация.

**Пакет datasource.repository.** Web-слой не импортирует репозиторий напрямую — только через `UserService` / `UserServiceImpl`.
""")
    _kartinа(add, ["```", "UserServiceImpl → UserRepository → users (SQL)", "```"])
    micro_step(1, "Интерфейс CrudRepository", "extends CrudRepository<UserEntity, UUID>",
               "public interface UserRepository extends CrudRepository<UserEntity, UUID> {",
               [("1", "CrudRepository", "save, findById из коробки")])
    micro_step(2, "Query methods", "findByLogin + existsByLogin",
               "    Optional<UserEntity> findByLogin(String login);\n    boolean existsByLogin(String login);",
               [("1", "findByLogin", "SELECT по login"),
                ("2", "existsByLogin", "Проверка занятости логина")])
    _svodka(add, "UserRepository.java", USER_REPOSITORY)
    block_footer(
        "Как Spring узнаёт SQL для findByLogin без @Query?",
        ".\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "—",
        "Репозиторий пользователей объявлен.",
        "Блок **D.3** — `UserService` + `UserServiceImpl`.",
    )

    # ===================== BLOCK D.3 =====================
    block_header("D.3", "`UserService` + `UserServiceImpl`",
                 "Регистрация, аутентификация, поиск login по id.", "20 мин", "★★☆")
    _theory(add, para_block, """
**Интерфейс в domain, реализация в datasource.** `UserService` — контракт для web и auth слоёв. `UserServiceImpl` — `@Service`, знает про `UserRepository` и `UserEntity`. Domain не импортирует JPA.

**register возвращает boolean.** true — пользователь создан; false — пустые поля или логин занят. Контроллер маппит false в 400 Bad Request. Не бросаем исключения на «бизнес-отказ» — проще для REST.

**authenticate → Optional<UUID>.** Успех — UUID пользователя; неудача — empty. `AuthServiceImpl` превратит empty в null для фильтра. Сравнение пароля — plain `equals` (учебный проект).

**findLoginById для UserController.** GET `/user/{uuid}` отдаёт ник соперника в PvP без пароля. Optional цепочка в контроллере → 404 если id не найден.

**Валидация null и blank.** `login.isBlank()` отсекает пробелы. Защита от мусорных запросов до обращения к БД.
""")
    _kartinа(add, ["```", "AuthController → AuthService → UserService → UserRepository", "```"])
    micro_step(1, "Интерфейс UserService", "Три метода в domain/service",
               "public interface UserService {\n    boolean register(String login, String password);\n    Optional<UUID> authenticate(String login, String password);\n    Optional<String> findLoginById(UUID id);\n}",
               [("2", "register", "Создание пользователя"),
                ("3", "authenticate", "Проверка credentials")])
    micro_step(2, "register в impl", "@Service, existsByLogin, save",
               "    public boolean register(String login, String password) {\n        if (login == null || password == null || login.isBlank() || password.isBlank()) return false;\n        if (userRepository.existsByLogin(login)) return false;\n        UUID id = UUID.randomUUID();\n        userRepository.save(new UserEntity(id, login, password));\n        return true;\n    }",
               [("2", "existsByLogin", "Дубликат логина"),
                ("4", "save(new UserEntity(...))", "INSERT в users")])
    micro_step(3, "authenticate", "findByLogin + filter password",
               "    public Optional<UUID> authenticate(String login, String password) {\n        return userRepository.findByLogin(login)\n                .filter(user -> user.getPassword().equals(password))\n                .map(UserEntity::getId);\n    }",
               [("2", "filter(password)", "Неверный пароль → empty")])
    _svodka(add, "UserService.java + UserServiceImpl.java", USER_SERVICE + "\n\n" + USER_SERVICE_IMPL)
    block_footer(
        "Почему authenticate возвращает Optional<UUID>, а не boolean?",
        ".\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "Bean not found UserService → проверь @Service на UserServiceImpl.",
        "Бизнес-логика пользователей в сервисе.",
        "Блок **D.4** — DTO `SignUpRequest`.",
    )

    # ===================== BLOCK D.4 =====================
    block_header("D.4", "`SignUpRequest.java`",
                 "JSON-тело для POST /auth/register.", "10 мин", "★☆☆")
    _theory(add, para_block, """
**DTO для входящего JSON.** Клиент шлёт `{"login":"alice","password":"secret"}`. Jackson маппит на `SignUpRequest` благодаря пустому конструктору и геттерам/сеттерам.

**Почему не Map<String,String>.** Типизированный класс — автодополнение в IDE, валидация на уровне компиляции, явный контракт API. Один файл — одна ответственность.

**Пакет web.model.** SignUpRequest — HTTP-слой; domain `UserService.register` принимает две строки — AuthService разбирает DTO.

**Без аннотаций валидации.** В учебном проекте проверка в сервисе. В продакшене добавили бы `@NotBlank` + `@Valid` в контроллере.

**Симметрия с UserDto.** Request — вход регистрации; Dto — выход профиля без пароля.
""")
    _kartinа(add, ["```", "JSON body → SignUpRequest → AuthService.register", "```"])
    micro_step(1, "Поля и конструкторы", "login, password, no-arg",
               "public class SignUpRequest {\n    private String login;\n    private String password;\n    public SignUpRequest() {\n    }",
               [("2", "login, password", "Поля JSON"),
                ("4", "SignUpRequest()", "Для Jackson")])
    micro_step(2, "Геттеры и сеттеры", "Стандартный JavaBean",
               "    public String getLogin() { return login; }\n    public void setLogin(String login) { this.login = login; }",
               [("1", "get/set", "Jackson читает и пишет поля")])
    _svodka(add, "SignUpRequest.java", SIGN_UP_REQUEST)
    block_footer(
        "Зачем пустой конструктор, если есть конструктор (login, password)?",
        ".\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "—",
        "DTO регистрации готов.",
        "Блок **D.5** — `AuthService` + `AuthServiceImpl` (parseBasicAuth).",
    )

    # ===================== BLOCK D.5 =====================
    block_header("D.5", "`AuthService` + `AuthServiceImpl`",
                 "Регистрация через UserService; разбор RFC 7617 Basic Auth.", "25 мин", "★★★")
    _theory(add, para_block, """
**AuthService — фасад для web.** Контроллеры не вызывают UserRepository напрямую. `register(SignUpRequest)` делегирует в `UserService`. `authorize(header)` — единая точка проверки заголовка для login и AuthFilter.

**Алгоритм parseBasicAuth.** (1) header == null или не начинается с `Basic ` → null. (2) Отрезать 6 символов `Basic `. (3) Base64 decode в UTF-8. (4) Найти первый `:`, слева login, справа password (пароль может содержать `:` — RFC допускает, мы режем по первому). (5) IllegalArgumentException при битом Base64 → null.

**Пример alice:secret.** Строка `alice:secret` → Base64 `YWxpY2U6c2VjcmV0`. В Postman/curl: `-H "Authorization: Basic YWxpY2U6c2VjcmV0"`. Проверь на [base64encode.org](https://www.base64encode.org/) для своих credentials.

**authorize возвращает UUID или null.** null — фильтр ставит 401. Не бросаем исключения наружу — фильтр ожидает простую проверку.

**Разделение register и authorize.** Register — тело JSON, публичный путь. Authorize — только заголовок, используется и в POST /auth/login, и в каждом защищённом запросе.
""")
    _kartinа(add, [
        "```",
        "Authorization: Basic YWxpY2U6c2VjcmV0",
        "    → parseBasicAuth → [alice, secret]",
        "    → userService.authenticate → UUID",
        "```",
    ])
    micro_step(1, "Интерфейс AuthService", "register + authorize",
               "public interface AuthService {\n    boolean register(SignUpRequest request);\n    UUID authorize(String authorizationHeader);\n}",
               [("2", "authorize", "null если невалидный auth")])
    micro_step(2, "register", "Делегирование в UserService",
               "    public boolean register(SignUpRequest request) {\n        if (request == null) return false;\n        return userService.register(request.getLogin(), request.getPassword());\n    }",
               [("2", "userService.register", "Бизнес-логика в UserService")])
    micro_step(3, "authorize", "parseBasicAuth + authenticate",
               "    public UUID authorize(String authorizationHeader) {\n        String[] credentials = parseBasicAuth(authorizationHeader);\n        if (credentials == null) return null;\n        return userService.authenticate(credentials[0], credentials[1]).orElse(null);\n    }",
               [("2", "parseBasicAuth", "Декодирование заголовка"),
                ("4", "orElse(null)", "Неудача → null")])
    micro_step(4, "parseBasicAuth", "Basic prefix, Base64, split по :",
               '    private String[] parseBasicAuth(String header) {\n        if (header == null || !header.startsWith("Basic ")) return null;\n        String base64 = header.substring(6).trim();\n        String decoded = new String(Base64.getDecoder().decode(base64), StandardCharsets.UTF_8);\n        int colonIndex = decoded.indexOf(\':\');\n        if (colonIndex < 0) return null;\n        return new String[]{decoded.substring(0, colonIndex), decoded.substring(colonIndex + 1)};\n    }',
               [("2", "startsWith(\"Basic \")", "Только схема Basic"),
                ("4", "Base64.getDecoder()", "RFC 7617")])
    _svodka(add, "AuthService.java + AuthServiceImpl.java", AUTH_SERVICE + "\n\n" + AUTH_SERVICE_IMPL)
    block_footer(
        "Чему равен Base64 для `alice:secret`?",
        ".\\gradlew.bat compileJava",
        "./gradlew compileJava",
        "IllegalArgumentException в decode → клиент прислал не Base64.",
        "parseBasicAuth — сердце Basic Auth.",
        "Блок **D.6** — `AuthController`.",
    )

    # ===================== BLOCK D.6 =====================
    block_header("D.6", "`AuthController.java`",
                 "POST /auth/register и POST /auth/login.", "15 мин", "★★☆")
    _theory(add, para_block, """
**Публичные эндпоинты /auth/**.** Не требуют Authorization (прописано в AuthFilter.isPublicPath и SecurityConfig). Register создаёт пользователя; login **проверяет** credentials и возвращает UUID — полезно для клиента, но защита API идёт через заголовок на каждом запросе.

**POST /auth/register.** Тело `SignUpRequest`. Успех — 200 пустое тело. Неудача — 400 + `ErrorResponse` с текстом. Не раскрываем, занят логин или пустой пароль — достаточно общего сообщения.

**POST /auth/login.** Читает `@RequestHeader Authorization` (required=false). Успех — 200 + UUID в JSON. Неудача — **401** + ErrorResponse. Это единственный login-эндпоинт, который явно возвращает 401 при неверном пароле.

**@RestController + @RequestMapping(\"/auth\").** Классический Spring MVC. ResponseEntity<?> — гибкие коды ответа.

**ErrorResponse.** Единый формат ошибок T04 — поле message в JSON. Клиент и curl всегда знают, что парсить.
""")
    _kartinа(add, ["```", "POST /auth/register  {login, password}", "POST /auth/login     Authorization: Basic …", "```"])
    micro_step(1, "Класс и register", "@RestController, POST /register",
               '@RestController\n@RequestMapping("/auth")\npublic class AuthController {\n    @PostMapping("/register")\n    public ResponseEntity<?> register(@RequestBody SignUpRequest request) {\n        boolean success = authService.register(request);\n        if (success) return ResponseEntity.ok().build();\n        return ResponseEntity.badRequest().body(new ErrorResponse("Registration failed: login may already exist"));\n    }',
               [("3", "@PostMapping(\"/register\")", "Публичная регистрация"),
                ("6", "badRequest", "400 при неудаче")])
    micro_step(2, "login", "Authorization header → authorize",
               '    @PostMapping("/login")\n    public ResponseEntity<?> login(@RequestHeader(value = "Authorization", required = false) String authHeader) {\n        UUID userId = authService.authorize(authHeader);\n        if (userId == null) return ResponseEntity.status(401).body(new ErrorResponse("Unauthorized"));\n        return ResponseEntity.ok(userId);\n    }',
               [("3", "authorize(authHeader)", "Тот же код, что в фильтре"),
                ("4", "status(401)", "Неверные credentials")])
    _svodka(add, "AuthController.java", AUTH_CONTROLLER)
    block_footer(
        "Почему login читает Authorization, а register — тело JSON?",
        ".\\gradlew.bat bootRun\n# curl register + login — см. этап F",
        "./gradlew bootRun",
        "403 на register → проверь permitAll и isPublicPath для /auth/register.",
        "Публичные auth-эндпоинты работают.",
        "Блок **D.7** — `AuthFilter` (микро-шаги).",
    )

    # ===================== BLOCK D.7 =====================
    block_header("D.7", "`AuthFilter.java`",
                 "Фильтр до контроллера: 401 без auth, userId в request attribute.", "30 мин", "★★★")
    _theory(add, para_block, """
**GenericFilterBean в Spring.** Наследуем `GenericFilterBean` — интеграция с Spring lifecycle. `doFilter` вызывается для каждого HTTP-запроса до servlet/controller.

**Критично: не вызывать chain при 401.** `return` после `setStatus(401)` — запрос **не доходит** до GameController. Иначе получишь и 401, и обработку в контроллере — двойное поведение.

**CURRENT_USER_ID_ATTR.** Строковый ключ `"currentUserId"` в `request.setAttribute`. `GameController.currentUserId(httpRequest)` читает UUID — кто создаёт игру, кто ходит. Без фильтра attribute null → NPE или чужие ходы.

**isPublicPath — белый список.** Точное совпадение `/auth/register`, `/auth/login`; статика `/css/`, `/js/`; корень и html. Всё остальное — включая `/game/**` — требует Basic Auth.

**Дублирование с SecurityConfig.** `permitAll` в Spring Security не отменяет наш фильтр. Оба слоя должны согласованно открывать публичные URL. Иначе Spring пустит, а AuthFilter вернёт 401 на `/index.html`.

**SC_UNAUTHORIZED = 401.** Константа из `HttpServletResponse`. Тело ответа пустое — для API достаточно кода; клиент знает: нужен заголовок Authorization.
""")
    _kartinа(add, [
        "```",
        "Request → isPublicPath? → да → chain",
        "         → нет → authorize → null? → 401 STOP",
        "                         → UUID → setAttribute → chain",
        "```",
    ])
    micro_step(1, "Класс и константа", "extends GenericFilterBean, CURRENT_USER_ID_ATTR",
               'public class AuthFilter extends GenericFilterBean {\n    public static final String CURRENT_USER_ID_ATTR = "currentUserId";\n    private final AuthService authService;\n    public AuthFilter(AuthService authService) { this.authService = authService; }',
               [("2", "CURRENT_USER_ID_ATTR", "Ключ для GameController"),
                ("4", "AuthService", "Проверка credentials")])
    micro_step(2, "doFilter: cast и path", "HttpServletRequest/Response, getRequestURI",
               "        HttpServletRequest httpRequest = (HttpServletRequest) request;\n        HttpServletResponse httpResponse = (HttpServletResponse) response;\n        String path = httpRequest.getRequestURI();",
               [("1", "HttpServletRequest", "Доступ к URI и заголовкам")])
    micro_step(3, "Публичные пути", "isPublicPath → chain.doFilter return",
               "        if (isPublicPath(path)) {\n            chain.doFilter(request, response);\n            return;\n        }",
               [("1", "isPublicPath", "Белый список без auth")])
    micro_step(4, "Проверка Authorization", "authorize → 401 или attribute",
               '        String authHeader = httpRequest.getHeader("Authorization");\n        UUID userId = authService.authorize(authHeader);\n        if (userId == null) {\n            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);\n            return;\n        }\n        httpRequest.setAttribute(CURRENT_USER_ID_ATTR, userId);\n        chain.doFilter(request, response);',
               [("2", "authorize", "Тот же AuthServiceImpl"),
                ("4", "return без chain", "401 — стоп"),
                ("7", "setAttribute", "userId для контроллера")])
    micro_step(5, "isPublicPath", "register, login, static",
               '    private static boolean isPublicPath(String path) {\n        if ("/auth/register".equals(path) || "/auth/login".equals(path)) return true;\n        if ("/".equals(path) || "/index.html".equals(path) || "/game.html".equals(path)) return true;\n        return path.startsWith("/css/") || path.startsWith("/js/") || path.endsWith(".txt");\n    }',
               [("2", "/auth/register", "Публичная регистрация"),
                ("4", "startsWith(\"/css/\")", "Статика")])
    _svodka(add, "AuthFilter.java", AUTH_FILTER)
    block_footer(
        "Что случится, если при userId==null всё равно вызвать chain.doFilter?",
        ".\\gradlew.bat bootRun\n# POST /game без Authorization → ожидай 401",
        "./gradlew bootRun",
        "401 на /auth/register → добавь путь в isPublicPath.",
        "Фильтр режет неавторизованные запросы.",
        "Блок **D.8** — `SecurityConfig` (микро-шаги).",
    )

    # ===================== BLOCK D.8 =====================
    block_header("D.8", "`SecurityConfig.java`",
                 "SecurityFilterChain: csrf off, permitAll, AuthFilter в цепочке.", "25 мин", "★★★")
    _theory(add, para_block, """
**@EnableWebSecurity.** Включает Spring Security filter chain. Без этой аннотации `@Bean SecurityFilterChain` может не подхватиться.

**csrf.disable().** CSRF защищает браузерные формы с cookie-сессией. REST API с Basic Auth на каждый запрос CSRF не требует — отключаем, иначе POST /game получит 403 Forbidden от Spring.

**permitAll для auth и статики.** `requestMatchers("/auth/register", "/auth/login").permitAll()` — Spring Security не требует своей аутентификации. Статика `/css/**`, `/js/**` — то же. Иначе браузер не загрузит CSS без пароля.

**anyRequest().permitAll() — осознанный выбор.** Мы **не** используем `authenticated()` Spring Security — проверку делает AuthFilter. Если поставить `authenticated()` без SecurityContext, получишь **403** даже с верным Basic Auth. Комментарий в коде: 401/403 даёт наш фильтр.

**addFilterBefore(authFilter, UsernamePasswordAuthenticationFilter.class).** Вставляем кастомный фильтр в цепочку Spring Security **перед** стандартным username/password. Порядок фильтров критичен.

**@Bean AuthFilter.** Spring создаёт фильтр с инжектом AuthService. Один экземпляр на приложение.
""")
    _kartinа(add, [
        "```",
        "SecurityFilterChain:",
        "  csrf OFF → authorizeHttpRequests (permitAll) → AuthFilter BEFORE UsernamePassword…",
        "```",
    ])
    micro_step(1, "Аннотации класса", "@Configuration @EnableWebSecurity",
               "@Configuration\n@EnableWebSecurity\npublic class SecurityConfig {",
               [("2", "@EnableWebSecurity", "Включает security filter chain")])
    micro_step(2, "Bean AuthFilter", "Фабрика фильтра",
               "    @Bean\n    public AuthFilter authFilter(AuthService authService) {\n        return new AuthFilter(authService);\n    }",
               [("2", "@Bean authFilter", "Spring управляет жизненным циклом")])
    micro_step(3, "csrf disable", "Первая настройка HttpSecurity",
               "        http.csrf(csrf -> csrf.disable())",
               [("1", "csrf.disable", "REST без CSRF-токена")])
    micro_step(4, "authorizeHttpRequests", "permitAll для auth и static",
               "                .authorizeHttpRequests(auth -> auth\n                        .requestMatchers(\"/auth/register\", \"/auth/login\").permitAll()\n                        .requestMatchers(\"/\", \"/index.html\", \"/game.html\", \"/css/**\", \"/js/**\").permitAll()\n                        .anyRequest().permitAll())",
               [("2", "permitAll /auth/*", "Регистрация без пароля"),
                ("4", "anyRequest().permitAll()", "401 — задаёт AuthFilter, не Spring")])
    micro_step(5, "addFilterBefore", "AuthFilter в цепочку",
               "                .addFilterBefore(authFilter, UsernamePasswordAuthenticationFilter.class);\n        return http.build();",
               [("1", "addFilterBefore", "Наш фильтр до стандартного auth")])
    _svodka(add, "SecurityConfig.java", SECURITY_CONFIG)
    block_footer(
        "Почему anyRequest().permitAll(), а не authenticated()?",
        ".\\gradlew.bat bootRun\n# Статика /css/app.css без 401",
        "./gradlew bootRun",
        "403 на /game с правильным Basic Auth → убери authenticated(), оставь permitAll + AuthFilter.",
        "Spring Security и AuthFilter согласованы.",
        "Блок **D.9** — `UserDto` + `UserController`.",
    )

    # ===================== BLOCK D.9 =====================
    block_header("D.9", "`UserDto` + `UserController`",
                 "GET /user/{userId} — login по UUID без пароля.", "15 мин", "★☆☆")
    _theory(add, para_block, """
**Профиль без секретов.** `UserDto` содержит только `id` и `login`. Пароль никогда не сериализуется в JSON — даже случайно через Jackson.

**GET /user/{userId}.** Публичный в смысле «не меняет состояние», но **требует Basic Auth** (не в isPublicPath). В PvP второй игрок узнаёт ник соперника по UUID из `player1Id` / `player2Id` в игре.

**Optional → ResponseEntity.** `findLoginById` → map в UserDto → 200, или `notFound()` → 404. Честные HTTP-коды.

**Разделение Auth и User контроллеров.** `/auth` — register/login. `/user` — чтение профиля. Single Responsibility на уровне URL.

**Завершение этапа D.** После этого блока любой `/game/*` без заголовка Authorization получает 401 от AuthFilter. Register/login работают без заголовка.
""")
    _kartinа(add, ["```", "GET /user/{uuid} + Basic Auth → {id, login}", "```"])
    micro_step(1, "UserDto", "id + login, конструкторы",
               "public class UserDto {\n    private UUID id;\n    private String login;\n    public UserDto(UUID id, String login) { this.id = id; this.login = login; }",
               [("2", "login без password", "Безопасный ответ API")])
    micro_step(2, "UserController", "GET /{userId}",
               '    @GetMapping("/{userId}")\n    public ResponseEntity<?> getUser(@PathVariable UUID userId) {\n        return userService.findLoginById(userId)\n                .map(login -> ResponseEntity.ok(new UserDto(userId, login)))\n                .orElse(ResponseEntity.notFound().build());\n    }',
               [("2", "findLoginById", "Опциональный login из БД"),
                ("3", "orElse(notFound())", "404 если нет пользователя")])
    _svodka(add, "UserDto.java + UserController.java", USER_DTO + "\n\n" + USER_CONTROLLER)
    block_footer(
        "Почему UserDto не содержит поле password?",
        ".\\gradlew.bat bootRun\n# GET /user/{uuid} с Basic Auth",
        "./gradlew bootRun",
        "404 → неверный UUID. 401 → нет Authorization.",
        "**Этап D выполнен:** Basic Auth защищает API.",
        "Переходи к **этапу E** — PvP и полная модель игры.",
    )

    # ===================== STAGE E THEORY =====================
    add("")
    add("# ЭТАП E — Задание 3: PvP и полная модель игры")
    add("")
    add("> **Замени целиком:** `CurrentGame`, `GameState`, `Symbol`, `GameService`, `GameServiceImpl`, `CurrentGameEntity`, `GameMapper`, `GameRepository`, `GameWebMapper`, `CurrentGameDto`, `CreateGameRequest`, `GameController`.")
    add("")
    _theory(add, para_block, """
**Машина состояний (state machine).** Игра — не просто доска, а состояние из enum `GameState`: `WAITING_FOR_PLAYERS` (лобби PvP), `PLAYER_TURN` (ход человека), `WIN`, `DRAW`. Переходы только через `GameServiceImpl`: join меняет WAITING→TURN, makeMove может привести к WIN/DRAW или смене `currentTurnPlayerId`. Недопустимый переход — `IllegalStateException` → 422 в контроллере.

**Паттерн лобби (lobby).** Создатель PvP-игры получает `WAITING_FOR_PLAYERS` и `player2Id=null`. `GET /game/available` возвращает список таких игр. Второй игрок `POST /game/{id}/join` — становится player2, state→`PLAYER_TURN`, ход у player1 (X). Это классический matchmaking без WebSocket: клиент опрашивает available или знает uuid по ссылке.

**PvE vs PvP.** Флаг `vsComputer` в `CreateGameRequest`. PvE: сразу `PLAYER_TURN`, player1 против Minimax, после хода человека `getNextMove`. PvP: после join ходы чередуются по `currentTurnPlayerId`; Minimax не вызывается. Один `GameServiceImpl` обслуживает оба режима — ветка `if (stored.isVsComputer())` в `makeMove`.

**Immutable CurrentGame.** Методы `withBoard`, `withState`, `withCurrentTurn`, `withWinner`, `asDraw` создают **новый** объект вместо мутации. Упрощает reasoning: после `makeMove` старая ссылка на игру не «портится» случайно. Сервис всегда возвращает свежий `CurrentGame` и сохраняет через `saveGame`.

**Полная entity и мапперы.** `CurrentGameEntity` получает все колонки PvP; `GameMapper` и `GameWebMapper` синхронно расширяются. DTO `CurrentGameDto` отдаёт клиенту state, player ids, symbols, чей ход — фронт рисует UI без угадывания.

**GameController и userId из фильтра.** `currentUserId(httpRequest)` читает `AuthFilter.CURRENT_USER_ID_ATTR`. Создание игры привязывает `player1Id`; ход проверяет `currentTurnPlayerId` в сервисе. Без этапа D attribute был бы null.
""")
    _kartinа(add, [
        "```",
        "WAITING_FOR_PLAYERS  --join-->  PLAYER_TURN  --move-->  WIN | DRAW | PLAYER_TURN",
        "     ^ PvP lobby              ^ PvE: + Minimax после хода",
        "```",
        "",
        "**Эндпоинты:** `POST /game`, `GET /game/available`, `POST /game/{id}/join`, `GET /game/{id}`, `POST /game/{id}` (ход).",
    ])
    add("---")
    add("")

    # ===================== BLOCK E.1 =====================
    block_header("E.1", "`GameState.java` и `Symbol.java`",
                 "Enum состояний игры и символов X/O с маппингом на 1/2.", "10 мин", "★☆☆")
    _theory(add, para_block, """
**GameState — четыре значения.** Соответствуют диаграмме из задания T04. `WAITING_FOR_PLAYERS` только для PvP до join. `PLAYER_TURN` — активная партия. Терминальные: `WIN`, `DRAW` — повторные ходы запрещены в `makeMove`.

**Symbol vs int на доске.** На `GameBoard` по-прежнему 0/1/2 (EMPTY/PLAYER/COMPUTER в PvE). `Symbol.X` → 1, `Symbol.O` → 2 через `toBoardValue()`. Enum даёт типобезопасность в domain; доска остаётся int[][] для Minimax из T03.

**@Enumerated(STRING) в entity.** В Postgres колонка `state` хранит `WAITING_FOR_PLAYERS`, не `0`. Читаемо в SQL и устойчиво к перестановке ordinal.

**fromBoardValue.** Обратный маппинг при определении победителя: линия из троек 1 → Symbol.X → player1Id или player2Id через `getPlayerIdBySymbol`.

**Два файла в одном блоке.** Оба enum в `domain/model` — нулевые зависимости от Spring и JPA.
""")
    _kartinа(add, ["```", "GameState: WAITING | PLAYER_TURN | WIN | DRAW", "Symbol: X (1), O (2)", "```"])
    micro_step(1, "GameState enum", "Четыре константы",
               "public enum GameState {\n    WAITING_FOR_PLAYERS,\n    PLAYER_TURN,\n    DRAW,\n    WIN\n}",
               [("2", "WAITING_FOR_PLAYERS", "Лобби PvP")])
    micro_step(2, "Symbol + toBoardValue", "X→1, O→2",
               "public enum Symbol {\n    X, O;\n    public int toBoardValue() { return this == X ? 1 : 2; }\n    public static Symbol fromBoardValue(int value) { return value == 1 ? X : O; }\n}",
               [("3", "toBoardValue", "Связь enum ↔ доска")])
    _svodka(add, "GameState.java + Symbol.java", GAME_STATE + "\n\n" + SYMBOL)
    block_footer("Зачем Symbol, если на доске уже 1 и 2?", ".\\gradlew.bat compileJava", "./gradlew compileJava", "—",
        "Типы состояний и символов готовы.", "Блок **E.2** — полный `CurrentGame.java`.")

    # ===================== BLOCK E.2 =====================
    block_header("E.2", "`CurrentGame.java` (полная версия)",
                 "Игроки, символы, чей ход, победитель, PvE/PvP; immutable with*-методы.", "30 мин", "★★★")
    _theory(add, para_block, """
**Расширение модели.** Помимо `id` и `board` — `player1Id`, `player2Id` (null в PvE или до join), `player1Symbol`/`player2Symbol`, `currentTurnPlayerId`, `winnerId`, `vsComputer`. Все поля `final` — immutability.

**Конструктор T03-совместимости.** `CurrentGame(UUID id, GameBoard board)` делегирует в полный с PvE по умолчанию: `PLAYER_TURN`, vsComputer=true, X/O. Старый код T03 компилируется.

**with*-методы.** Каждый возвращает новый `CurrentGame` с одним изменённым полем. `withWinner` фиксирует `GameState.WIN` и обнуляет `currentTurnPlayerId`. `asDraw` — терминальная ничья.

**getPlayerIdBySymbol / getSymbolByPlayerId.** Связь «кто играет X» с UUID для валидации хода и отображения победителя. `validateBoard` в сервисе берёт symbol игрока по `playerId`.

**player2Id null.** Означает «ждём второго» или «против компьютера». Не путать с «пустая клетка» на доске — там 0.
""")
    _kartinа(add, ["```", "CurrentGame (immutable)", "  id, board, state, players, symbols, turn, winner, vsComputer", "```"])
    micro_step(1, "Поля и полный конструктор", "Все final поля",
               "    private final UUID id;\n    private final GameBoard board;\n    private final GameState state;\n    private final UUID player1Id;\n    private final UUID player2Id;",
               [("2", "final", "Иммутабельность")])
    micro_step(2, "Конструктор T03", "CurrentGame(id, board)",
               "    public CurrentGame(UUID id, GameBoard board) {\n        this(id, board, GameState.PLAYER_TURN, null, null, Symbol.X, Symbol.O, null, null, true);\n    }",
               [("2", "vsComputer true", "Обратная совместимость PvE")])
    micro_step(3, "withBoard, withState, withCurrentTurn", "Копии с изменением",
               "    public CurrentGame withBoard(GameBoard newBoard) {\n        return new CurrentGame(id, newBoard, state, player1Id, player2Id,\n                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);\n    }",
               [("1", "withBoard", "Новая доска — новый объект")])
    micro_step(4, "withWinner, asDraw, getPlayerIdBySymbol", "Терминальные и хелперы",
               "    public CurrentGame withWinner(UUID winner) {\n        return new CurrentGame(id, board, GameState.WIN, player1Id, player2Id,\n                player1Symbol, player2Symbol, null, winner, vsComputer);\n    }",
               [("1", "withWinner", "Победа + state WIN")])
    _svodka(add, "CurrentGame.java", CURRENT_GAME_FULL)
    block_footer("Почему withBoard создаёт новый объект?", ".\\gradlew.bat compileJava", "./gradlew compileJava", "—",
        "Domain-модель игры полная.", "Блок **E.3** — интерфейс `GameService`.")

    # ===================== BLOCK E.3 =====================
    block_header("E.3", "`GameService.java` (интерфейс T04)",
                 "create, join, available, makeMove, save + методы T03 Minimax.", "15 мин", "★★☆")
    _theory(add, para_block, """
**Контракт domain для web.** `GameController` зависит только от интерфейса. Реализация `GameServiceImpl` в datasource — можно подменить на mock в тестах.

**Новые методы T04.** `createGame(creatorId, vsComputer)`, `getAvailableGames()`, `joinGame(gameId, playerId)`, `getGame`, `makeMove` с `playerId`, `saveGame`. creatorId/playerId приходят из AuthFilter.

**Наследие T03.** `getNextMove`, `getFirstMove`, `validateBoard`, `updateGameState` — Minimax и проверка одного хода. Сигнатура `validateBoard` расширена `UUID playerId` — чей символ на доске ожидаем.

**saveGame явный.** Контроллер после каждой мутации вызывает save — персистентность не спрятана внутри makeMove. Прозрачно для отладки SQL.

**List vs Optional.** Список лобби всегда возвращает массив (возможно пустой). Одна игра — Optional для 404 в GET.
""")
    _kartinа(add, ["```", "GameController → GameService (interface) → GameServiceImpl", "```"])
    micro_step(1, "Методы T04", "create, available, join, get, makeMove, save",
               "    CurrentGame createGame(UUID creatorId, boolean vsComputer);\n    List<CurrentGame> getAvailableGames();\n    CurrentGame joinGame(UUID gameId, UUID playerId);",
               [("1", "createGame", "PvE или лобби PvP")])
    micro_step(2, "Методы T03", "Minimax и валидация",
               "    CurrentGame getNextMove(CurrentGame game);\n    boolean validateBoard(CurrentGame stored, CurrentGame incoming, UUID playerId);\n    CurrentGame updateGameState(CurrentGame game);",
               [("2", "validateBoard + playerId", "Символ ходящего")])
    _svodka(add, "GameService.java", GAME_SERVICE)
    block_footer("Кто передаёт creatorId в createGame?", ".\\gradlew.bat compileJava", "./gradlew compileJava", "—",
        "Интерфейс сервиса T04 объявлен.", "Блок **E.4** — полный `CurrentGameEntity`.")

    # ===================== BLOCK E.4 =====================
    block_header("E.4", "`CurrentGameEntity.java` (все колонки)",
                 "Заменить упрощённую версию C.5 на полную JPA entity с PvP полями.", "20 мин", "★★☆")
    _theory(add, para_block, """
**Миграция схемы ddl-auto=update.** Hibernate добавит колонки `state`, `player1_id`, … к существующей таблице `games`. Старые строки получат default из конструктора entity при следующем save.

**@Enumerated(STRING) для state и symbols.** В БД текст `PLAYER_TURN`, не ordinal 1. Устойчиво при добавлении новых enum значений в будущем.

**vsComputer boolean.** `nullable = false` — каждая игра либо PvE, либо PvP. Default `false` в no-arg конструкторе; createGame в сервисе выставляет явно.

**Имена колонок snake_case.** `player1_id` в SQL, `player1Id` в Java — `@Column(name = \"player1_id\")` маппинг.

**Симметрия с CurrentGame.** Поля entity 1:1 с domain — маппер тривиален, без потери данных при round-trip save/load.
""")
    _kartinа(add, ["```", "games: id, cell_*, state, player1_id, player2_id, symbols, turn, winner, vs_computer", "```"])
    micro_step(1, "state и vsComputer", "Enum + boolean колонки",
               "    @Enumerated(EnumType.STRING)\n    @Column(nullable = false)\n    private GameState state;",
               [("2", "EnumType.STRING", "Текст в Postgres")])
    micro_step(2, "Игроки и символы", "UUID + Symbol поля",
               "    @Column(name = \"player1_id\") private UUID player1Id;\n    @Column(name = \"player2_id\") private UUID player2Id;",
               [("1", "player1_id", "Создатель лобби")])
    micro_step(3, "Ход и победитель", "currentTurnPlayerId, winnerId",
               "    @Column(name = \"current_turn_player_id\") private UUID currentTurnPlayerId;\n    @Column(name = \"winner_id\") private UUID winnerId;",
               [("1", "current_turn_player_id", "Чей ход в PvP")])
    _svodka(add, "CurrentGameEntity.java (полная)", CURRENT_GAME_ENTITY_FULL)
    block_footer("Что сделает Hibernate со старой таблицей games?", ".\\gradlew.bat bootRun", "./gradlew bootRun", "—",
        "Entity синхронна с domain CurrentGame.", "Блок **E.5** — финальные `GameRepository` + `GameMapper`.")

    # ===================== BLOCK E.5 =====================
    block_header("E.5", "`GameRepository` + `GameMapper` (финал)",
                 "findByState для лобби; маппер со всеми полями PvP.", "15 мин", "★★☆")
    _theory(add, para_block, """
**GameRepository без изменений интерфейса.** `findByState(WAITING_FOR_PLAYERS)` уже объявлен на этапе C — теперь реально используется в `getAvailableGames`. Spring Data SQL не менялся — менилась только наполненность entity.

**GameMapper toDomain полный.** Все десять аргументов конструктора `CurrentGame`. Null entity → null domain — защита от NPE в цепочках Optional.

**GameMapper toEntity.** Каждый getter domain → setter entity. Порядок не важен; важно не забыть `vsComputer` и `state` — иначе после load игра «сбросится» в default.

**Два маппера не смешивать.** `GameMapper` — entity↔domain. `GameWebMapper` — DTO↔domain. Entity никогда не уходит в JSON напрямую — только через domain и DTO.

**Round-trip тест мысленно.** save(load(game)) должно восстановить идентичную логическую игру. Если player2Id теряется — баг в маппере.
""")
    _kartinа(add, ["```", "Entity ←GameMapper→ Domain ←GameWebMapper→ DTO", "```"])
    micro_step(1, "toDomain все поля", "Полный конструктор CurrentGame",
               "        return new CurrentGame(\n                entity.getId(), board, entity.getState(),\n                entity.getPlayer1Id(), entity.getPlayer2Id(),\n                entity.getPlayer1Symbol(), entity.getPlayer2Symbol(),\n                entity.getCurrentTurnPlayerId(), entity.getWinnerId(),\n                entity.isVsComputer());",
               [("2", "entity.getState()", "Состояние из БД")])
    micro_step(2, "toEntity все сеттеры", "Копия каждого поля",
               "        entity.setState(game.getState());\n        entity.setPlayer1Id(game.getPlayer1Id());\n        entity.setVsComputer(game.isVsComputer());",
               [("1", "setState", "Персистентность state")])
    _svodka(add, "GameRepository.java + GameMapper.java", GAME_REPOSITORY + "\n\n" + GAME_MAPPER_FULL)
    block_footer("Чем GameMapper отличается от GameWebMapper?", ".\\gradlew.bat compileJava", "./gradlew compileJava", "—",
        "Персистентность и маппинг PvP полей готовы.", "Блок **E.6** — `GameServiceImpl` (микро-шаги).")

    # ===================== BLOCK E.6 =====================
    block_header("E.6", "`GameServiceImpl.java` (финал)",
                 "create/join/available, makeMove PvP/PvE, Minimax, updateGameState.", "45 мин", "★★★★")
    _theory(add, para_block, """
**@Service и инжект GameRepository.** Spring создаёт один бин `GameServiceImpl` на приложение. Все операции с играми проходят через `gameRepository.save(GameMapper.toEntity(...))` в `saveGame` — вызывается из контроллера после каждой мутации.

**createGame — ветка PvE и PvP.** `vsComputer=true` → сразу `PLAYER_TURN`, `currentTurnPlayerId=creatorId`, player2 null. `vsComputer=false` → `WAITING_FOR_PLAYERS`, ход ещё не назначен — ждём join.

**joinGame — правила лобби.** Игра должна быть в WAITING; нельзя join к себе; player2 получает Symbol.O; первый ход у player1 (X). Исключения — IllegalArgumentException/IllegalStateException.

**makeMove — ядро.** Проверки: state PLAYER_TURN, currentTurnPlayerId == playerId, validateBoard (ровно одна новая клетка символа игрока). После хода — updateGameState. Если не конец и PvE — getNextMove (Minimax) + снова updateGameState. Если PvP — смена currentTurnPlayerId на соперника.

**updateGameState и победа компьютера.** Если winnerSymbol O в PvE — winnerId=null (победа компьютера, не пользователя). Линии проверяет evaluateWinner как в T03.

**Minimax без изменений.** findBestMove, minimax, evaluateMinimax — перенос из этапа B. COMPUTER=2, PLAYER=1 на доске.
""")
    _kartinа(add, [
        "```",
        "makeMove: validate → updateState → [PvE: getNextMove] → updateState → return",
        "createGame: vsComputer? PLAYER_TURN : WAITING_FOR_PLAYERS",
        "```",
    ])
    micro_step(1, "Класс, saveGame, createGame PvE", "@Service, repository, ветка vsComputer",
               "@Service\npublic class GameServiceImpl implements GameService {\n    public void saveGame(CurrentGame game) {\n        gameRepository.save(GameMapper.toEntity(game));\n    }\n    // createGame: if (vsComputer) return new CurrentGame(..., PLAYER_TURN, creatorId, ..., true);",
               [("1", "@Service", "Бин Spring"),
                ("3", "saveGame", "INSERT/UPDATE в games")])
    micro_step(2, "createGame PvP и getAvailableGames", "WAITING_FOR_PLAYERS + findByState",
               "        return new CurrentGame(gameId, emptyBoard, GameState.WAITING_FOR_PLAYERS, creatorId, null, Symbol.X, Symbol.O, null, null, false);\n    }\n    public List<CurrentGame> getAvailableGames() {\n        return gameRepository.findByState(GameState.WAITING_FOR_PLAYERS).stream().map(GameMapper::toDomain).toList();\n    }",
               [("1", "WAITING_FOR_PLAYERS", "Лобби"),
                ("4", "findByState", "SQL для available")])
    micro_step(3, "joinGame", "Проверки и назначение player2",
               "        if (game.getState() != GameState.WAITING_FOR_PLAYERS) throw new IllegalStateException(\"Game is not waiting for players\");\n        return new CurrentGame(game.getId(), game.getBoard(), GameState.PLAYER_TURN, game.getPlayer1Id(), playerId, game.getPlayer1Symbol(), Symbol.O, game.getPlayer1Id(), null, false);",
               [("1", "WAITING check", "Только лобби"),
                ("2", "Symbol.O player2", "Второй игрок — нолики")])
    micro_step(4, "makeMove — проверки", "state, turn, validateBoard",
               "        if (stored.getState() != GameState.PLAYER_TURN) throw new IllegalStateException(\"Game is not in progress\");\n        if (!playerId.equals(stored.getCurrentTurnPlayerId())) throw new IllegalStateException(\"Not your turn\");\n        if (!validateBoard(stored, incoming, playerId)) throw new IllegalStateException(\"Invalid board\");",
               [("1", "PLAYER_TURN", "Игра идёт"),
                ("2", "Not your turn", "PvP очередь")])
    micro_step(5, "makeMove — PvE Minimax и PvP смена хода", "getNextMove или withCurrentTurn",
               "        if (stored.isVsComputer()) {\n            CurrentGame afterComputer = getNextMove(afterPlayerMoveChecked);\n            return updateGameState(afterComputer);\n        }\n        UUID nextPlayer = stored.getPlayer1Id().equals(playerId) ? stored.getPlayer2Id() : stored.getPlayer1Id();\n        return updateGameState(afterPlayerMoveChecked.withCurrentTurn(nextPlayer));",
               [("1", "isVsComputer", "Ветка PvE"),
                ("5", "withCurrentTurn", "Смена хода PvP")])
    micro_step(6, "validateBoard и updateGameState", "symbol по playerId, победа/ничья",
               "        Symbol playerSymbol = stored.getSymbolByPlayerId(playerId);\n        int expectedValue = playerSymbol.toBoardValue();\n        return boardsMatchExceptOneMove(...);\n    // updateGameState: evaluateWinner → withWinner или asDraw",
               [("1", "getSymbolByPlayerId", "Чей символ на доске"),
                ("4", "withWinner", "Терминальное WIN")])
    micro_step(7, "Minimax findBestMove", "Без изменений из T03",
               "    private int[] findBestMove(GameBoard board) {\n        // перебор пустых клеток, minimax, лучший score\n    }",
               [("1", "findBestMove", "Ход компьютера")])
    _svodka(add, "GameServiceImpl.java", GAME_SERVICE_IMPL)
    block_footer("Что вернёт makeMove в PvP после первого хода player1?", ".\\gradlew.bat compileJava", "./gradlew compileJava",
        "Not your turn при PvP → проверь currentTurnPlayerId после join.",
        "Сервис обслуживает PvE и PvP.", "Блок **E.7** — DTO и `GameWebMapper`.")

    # ===================== BLOCK E.7 =====================
    block_header("E.7", "`CreateGameRequest`, `CurrentGameDto`, `GameWebMapper`",
                 "HTTP-модели и маппер web ↔ domain.", "25 мин", "★★☆")
    _theory(add, para_block, """
**CreateGameRequest — один флаг.** `vsComputer` в JSON `{"vsComputer":true}` для PvE. Jackson требует пустой конструктор и getter/setter. POST /game без тела трактует как PvP (false).

**CurrentGameDto — полная картина для клиента.** id, board (GameBoardDto), state, player ids, symbols, currentTurnPlayerId, winnerId, vsComputer. Плюс `computerStarts` — legacy для сценария «играю за O, компьютер ходит первым» в PvE.

**GameBoardDto без изменений.** Вложенный `int[][] board` — как в T03. CurrentGameDto.board — объект GameBoardDto.

**GameWebMapper.toDto / toDomain.** Симметричный маппинг всех полей. В toDomain дефолты: state PLAYER_TURN, symbols X/O если null — защита от неполного JSON.

**Разделение GameMapper и GameWebMapper.** Entity не знает про DTO. Контроллер: DTO → domain (web mapper) → service → domain → entity (game mapper) → DB.
""")
    _kartinа(add, ["```", "JSON ↔ CurrentGameDto ↔ GameWebMapper ↔ CurrentGame ↔ GameService", "```"])
    micro_step(1, "CreateGameRequest", "boolean vsComputer",
               "public class CreateGameRequest {\n    private boolean vsComputer;\n    public boolean isVsComputer() { return vsComputer; }\n}",
               [("2", "vsComputer", "PvE vs PvP")])
    micro_step(2, "CurrentGameDto поля", "Все поля + computerStarts",
               "    private UUID id;\n    private GameBoardDto board;\n    private GameState state;\n    private UUID player1Id;\n    private Boolean computerStarts;",
               [("3", "state", "Для UI лобби/ход"),
                ("5", "computerStarts", "PvE первый ход AI")])
    micro_step(3, "GameWebMapper toDto", "Заполнение DTO из domain",
               "        dto.setState(game.getState());\n        dto.setPlayer1Id(game.getPlayer1Id());\n        dto.setCurrentTurnPlayerId(game.getCurrentTurnPlayerId());",
               [("1", "setState", "Состояние в JSON")])
    micro_step(4, "GameWebMapper toDomain", "Обратный маппинг с дефолтами",
               "        return new CurrentGame(dto.getId(), board, dto.getState() != null ? dto.getState() : GameState.PLAYER_TURN, ...);",
               [("1", "new CurrentGame", "Полный конструктор")])
    _svodka(add, "CreateGameRequest + CurrentGameDto + GameWebMapper",
              CREATE_GAME_REQUEST + "\n\n" + CURRENT_GAME_DTO + "\n\n" + GAME_WEB_MAPPER)
    block_footer("Зачем computerStarts в DTO, если есть vsComputer?", ".\\gradlew.bat compileJava", "./gradlew compileJava", "—",
        "Web-слой готов к полному API.", "Блок **E.8** — `GameController` (все эндпоинты).")

    # ===================== BLOCK E.8 =====================
    block_header("E.8", "`GameController.java` (все эндпоинты)",
                 "POST /game, available, join, GET, POST ход; userId из AuthFilter.", "35 мин", "★★★★")
    _theory(add, para_block, """
**Пять операций API.** `POST /game` — создать. `GET /game/available` — лобби. `POST /game/{id}/join` — войти в PvP. `GET /game/{id}` — состояние. `POST /game/{id}` — ход (и computerStarts для PvE).

**currentUserId из request attribute.** `AuthFilter` положил UUID; контроллер не парсит Basic Auth сам — DRY с фильтром. Если attribute null при защищённом пути — значит фильтр сломан, не контроллер.

**computerStarts ветка.** Если флаг true и доска пустая — `getFirstMove` (компьютер в центр), save, вернуть DTO. Отдельно от обычного makeMove.

**Коды ошибок.** 400 — join/bad body. 404 — игра не найдена. 422 — IllegalStateException (не твой ход, игра окончена). 401 — только фильтр, не контроллер.

**save после каждой мутации.** create, join, makeMove, computerStarts — везде `gameService.saveGame` перед ответом. Забыл save — после рестарта откат.

**Завершение части 2.** После E.8 backend T04 полный: Postgres, auth, PvP/PvE. Часть 3 (F, G) — curl-сценарии и браузерный UI.
""")
    _kartinа(add, [
        "```",
        "POST /game          → create + save",
        "GET  /game/available",
        "POST /game/{id}/join",
        "GET  /game/{id}",
        "POST /game/{id}     → makeMove | computerStarts",
        "```",
    ])
    micro_step(1, "createGame", "POST /game, userId, vsComputer",
               "    @PostMapping\n    public ResponseEntity<?> createGame(@RequestBody CreateGameRequest request, HttpServletRequest httpRequest) {\n        UUID userId = currentUserId(httpRequest);\n        CurrentGame game = gameService.createGame(userId, request != null && request.isVsComputer());\n        gameService.saveGame(game);\n        return ResponseEntity.ok(GameWebMapper.toDto(game));\n    }",
               [("3", "currentUserId", "Из AuthFilter"),
                ("5", "saveGame", "Персистентность")])
    micro_step(2, "available и join", "GET list, POST join",
               "    @GetMapping(\"/available\")\n    public ResponseEntity<List<CurrentGameDto>> getAvailableGames() { ... }\n    @PostMapping(\"/{gameId}/join\")\n    public ResponseEntity<?> joinGame(@PathVariable UUID gameId, HttpServletRequest httpRequest) { ... }",
               [("1", "/available", "Лобби PvP"),
                ("3", "/join", "Второй игрок")])
    micro_step(3, "getGame", "GET по uuid",
               "    @GetMapping(\"/{gameId}\")\n    public ResponseEntity<?> getGame(@PathVariable UUID gameId) {\n        return gameService.getGame(gameId).map(g -> ResponseEntity.ok(GameWebMapper.toDto(g))).orElse(ResponseEntity.notFound().build());\n    }",
               [("2", "orElse notFound", "404")])
    micro_step(4, "makeMove — валидация тела", "id match, board present",
               "        if (request == null || request.getBoard() == null) return ResponseEntity.badRequest().body(new ErrorResponse(\"Missing board\"));\n        if (!gameId.equals(request.getId())) return ResponseEntity.badRequest().body(new ErrorResponse(\"Game id mismatch\"));",
               [("1", "Missing board", "400"),
                ("2", "id mismatch", "Честный контракт")])
    micro_step(5, "computerStarts", "Пустая доска + флаг",
               "        if (Boolean.TRUE.equals(request.getComputerStarts()) && isBoardEmpty(incoming.getBoard())) {\n            return gameService.getGame(gameId).map(stored -> {\n                CurrentGame afterFirst = gameService.getFirstMove(stored);\n                gameService.saveGame(afterFirst);\n                return ResponseEntity.ok(GameWebMapper.toDto(afterFirst));\n            }).orElse(ResponseEntity.notFound().build());\n        }",
               [("1", "computerStarts", "PvE: AI ходит первым")])
    micro_step(6, "makeMove — try/catch 422", "IllegalStateException → UNPROCESSABLE_ENTITY",
               "        try {\n            CurrentGame result = gameService.makeMove(gameId, incoming, userId);\n            gameService.saveGame(result);\n            return ResponseEntity.ok(GameWebMapper.toDto(result));\n        } catch (IllegalStateException e) {\n            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(new ErrorResponse(e.getMessage()));\n        }",
               [("4", "422", "Не твой ход / игра окончена")])
    micro_step(7, "currentUserId helper", "Чтение attribute",
               "    private static UUID currentUserId(HttpServletRequest request) {\n        return (UUID) request.getAttribute(AuthFilter.CURRENT_USER_ID_ATTR);\n    }",
               [("2", "CURRENT_USER_ID_ATTR", "Связь с AuthFilter")])
    _svodka(add, "GameController.java", GAME_CONTROLLER)
    block_footer(
        "Какой эндпоинт вернёт 422 при ходе не в свою очередь?",
        ".\\gradlew.bat bootRun\n# Полный цикл PvE/PvP — см. часть 3 (этап F)",
        "./gradlew bootRun",
        "401 на /game → Authorization header. 500 NPE на userId → AuthFilter не в цепочке.",
        "**Этап E выполнен.** Часть 2 закончена — переходи к **части 3** (этапы F и G).",
        "Открой файл части 3, когда будешь готов к curl и браузерному UI.",
    )

    # ===================== APPENDIX: depth + troubleshooting =====================
    add("")
    add("---")
    add("")
    add("## Приложение — расширенная диагностика по блокам")
    add("")
    para_block("""
**Как пользоваться приложением.** Если блок прошёл «Проверку», но что-то ведёт себя странно на следующем этапе — найди номер блока ниже. Каждый подраздел — типичные симптомы, причина и точечный фикс. Не перечитывай всю часть 2: начни с последнего закрытого блока и иди назад.

**Связь с теорией.** В [`T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md`](T04_07_ТЕОРИЯ_ПОЛНОСТЬЮ.md) те же темы разобраны глубже: JDBC, JPA, Basic Auth, state machine. Здесь — только практическая диагностика при разработке.

**Логи bootRun.** Держи консоль видимой: `Hibernate:` — SQL, `HikariPool` — пул соединений, stack trace — строка в **твоём** коде (не в spring-*.jar). Первый кадр в `tictactoe.*` — где чинить.
""", 3)

    _BLOCK_DIAG = [
        ("C.1", "PostgreSQL", "Connection refused", "Служба Postgres не запущена. Windows: services.msc → postgresql. Linux: `sudo systemctl start postgresql`."),
        ("C.1", "PostgreSQL", "database tictactoe does not exist", "Выполни `CREATE DATABASE tictactoe;` в psql **до** bootRun."),
        ("C.2", "Gradle", "Cannot resolve postgresql", "Проверь интернет, `mavenCentral()`, Reload Gradle Project."),
        ("C.2", "Gradle", "package jakarta.persistence does not exist", "Не подтянулся starter-data-jpa — исправь build.gradle.kts и Reload."),
        ("C.3", "properties", "password authentication failed", "Замени ТВОЙ_ЛОГИН/ТВОЙ_ПАРОЛЬ на реальные. Проверь pg_hba.conf если удалённый хост."),
        ("C.3", "properties", "Нет SQL в консоли", "Добавь `spring.jpa.show-sql=true`."),
        ("C.4", "GameBoardEntity", "cannot find symbol GameBoard", "import tictactoe.domain.model.GameBoard — domain из этапа B."),
        ("C.4", "GameBoardEntity", "Invalid cell в set()", "row/col вне 0..2 — проверь вызов из теста."),
        ("C.5", "CurrentGameEntity", "Таблица без cell_*", "Забыли @Embedded на board или GameBoardEntity не @Embeddable."),
        ("C.6", "GameRepository", "Bean conflict GameRepository", "Удали GameRepositoryImpl из этапа B."),
        ("C.6", "GameRepository", "findByState не компилируется", "Импорт GameState из domain.model."),
        ("C.7", "GameMapper", "Потерялись ходы после рестарта", "GameServiceImpl не вызывает repository.save — проверь saveGame."),
        ("C.8", "SpringConfig", "No qualifying bean GameService", "Добавь @Service на GameServiceImpl."),
        ("C.8", "memory", "Данные не пережили рестарт", "save идёт в HashMap — удали GameStorage, проверь JPA save."),
        ("D.1", "UserEntity", "Нет таблицы users", "bootRun с ddl-auto=update после добавления entity."),
        ("D.2", "UserRepository", "Duplicate bean", "Только интерфейс, без impl."),
        ("D.3", "UserServiceImpl", "register всегда false", "login blank или existsByLogin — попробуй другой логин."),
        ("D.4", "SignUpRequest", "400 с пустым телом", "Content-Type: application/json обязателен."),
        ("D.5", "AuthServiceImpl", "authorize всегда null", "Заголовок должен быть `Basic ` + Base64(`login:password`)."),
        ("D.5", "Basic Auth", "alice:secret не работает", "Base64 именно `YWxpY2U6c2VjcmV0`, без переноса строки."),
        ("D.6", "AuthController", "403 на /auth/register", "SecurityConfig permitAll + AuthFilter isPublicPath для /auth/register."),
        ("D.7", "AuthFilter", "401 на статику", "Добавь /css/, /js/ в isPublicPath."),
        ("D.7", "AuthFilter", "Контроллер вызывается без auth", "При userId==null нельзя вызывать chain.doFilter."),
        ("D.8", "SecurityConfig", "403 с правильным Basic", "Убери anyRequest().authenticated() — только permitAll + AuthFilter."),
        ("D.8", "SecurityConfig", "CSRF 403 на POST", "csrf.disable() для REST."),
        ("D.9", "UserController", "404 на существующего user", "Неверный UUID — сверь с ответом /auth/login."),
        ("E.1", "GameState", "Illegal enum в JSON", "Клиент шлёт строку WAITING_FOR_PLAYERS, не число."),
        ("E.2", "CurrentGame", "NPE в withBoard", "Передаёшь null board — используй copy() из GameBoard."),
        ("E.3", "GameService", "Метод не реализован", "GameServiceImpl должен implements все методы интерфейса."),
        ("E.4", "CurrentGameEntity", "Колонка не добавилась", "ddl-auto=update; перезапусти bootRun; смотри ALTER в логах."),
        ("E.5", "GameMapper", "player2Id null после load", "Забыли setPlayer2Id в toEntity."),
        ("E.6", "GameServiceImpl", "Not your turn в PvP", "join должен выставить currentTurnPlayerId=player1Id."),
        ("E.6", "GameServiceImpl", "Компьютер не ходит", "vsComputer true и makeMove вызывает getNextMove."),
        ("E.6", "Minimax", "Слабый AI", "Проверь evaluateMinimax и глубину — код из T03 без изменений."),
        ("E.7", "CurrentGameDto", "Пустой state в JSON", "GameWebMapper.toDto должен setState."),
        ("E.7", "computerStarts", "Центр не занят", "getFirstMove ставит (1,1) COMPUTER."),
        ("E.8", "GameController", "NPE currentUserId", "AuthFilter не в цепочке или путь публичный по ошибке."),
        ("E.8", "GameController", "422 Not your turn", "Ожидаемо — ходит другой playerId; сверь currentTurnPlayerId в DTO."),
        ("E.8", "GameController", "Game id mismatch", "UUID в URL и в теле JSON должны совпадать."),
        ("C", "JPA", "LazyInitializationException", "В учебном проекте редко; если появился — не трогай entity вне транзакции."),
        ("D", "Auth", "Opечатка Autorization", "Строго `Authorization` — иначе null в authorize."),
        ("E", "PvP", "join к своей игре", "IllegalStateException — нельзя join самому себе."),
        ("E", "PvE", "computerStarts не срабатывает", "Доска должна быть пустой и флаг true в JSON."),
    ]

    for blk, comp, symptom, fix in _BLOCK_DIAG:
        add(f"### {blk} — {comp}: {symptom}")
        add("")
        add(f"**Симптом:** {symptom}.")
        add("")
        add(f"**Что проверить:** {fix}")
        add("")
        add(f"**Связанные файлы:** см. блок {blk} выше и сверку полного файла.")
        add("")

    add("---")
    add("")
    add("## Контрольные вопросы (закрой глаза и ответь)")
    add("")
    _QA = [
        ("C", "Чем @Embeddable отличается от @Entity для доски?"),
        ("C", "Кто генерирует SQL для findByState — ты или Spring Data?"),
        ("C", "Почему GameRepositoryImpl нужно удалить?"),
        ("D", "Чему равен Base64 для `bob:pass`? (посчитай вручную или в консоли)"),
        ("D", "Разница 401 и 403 в нашем проекте?"),
        ("D", "Зачем CURRENT_USER_ID_ATTR в request?"),
        ("D", "Почему permitAll и isPublicPath нужны оба?"),
        ("E", "Какие state у игры в лобби PvP до join?"),
        ("E", "Кто ходит первым после join — player1 или player2?"),
        ("E", "Когда makeMove вызывает Minimax?"),
        ("E", "Зачем immutable withBoard вместо board.set?"),
        ("E", "Перечисли все пять эндпоинтов GameController."),
        ("C", "Зачем runtimeOnly для PostgreSQL драйвера?"),
        ("C", "Что покажет show-sql=true при первом save игры?"),
        ("D", "Где хранится пароль пользователя и почему не в UserDto?"),
        ("E", "Что возвращает winnerId при победе компьютера в PvE?"),
    ]
    for stage, q in _QA:
        add(f"- **[{stage}]** {q}")
        add("")
        add("  <details><summary>Ответ (открой после своего ответа)</summary>")
        add("")
        if stage == "C" and "Embeddable" in q:
            add("  @Embeddable встраивает колонки в таблицу games; @Entity создала бы отдельную таблицу с FK.")
        elif stage == "C" and "findByState" in q:
            add("  Spring Data JPA по соглашению об имени метода — реализацию пишет фреймворк.")
        elif stage == "C" and "RepositoryImpl" in q:
            add("  Два бина репозитория; JPA заменяет in-memory impl.")
        elif stage == "D" and "Base64" in q:
            add("  `Ym9iOnBhc3M=` — посчитай: echo -n 'bob:pass' | base64.")
        elif stage == "D" and "401" in q:
            add("  401 — AuthFilter: нет/неверный Basic Auth. 403 — Spring Security authenticated без контекста.")
        elif stage == "D" and "CURRENT_USER" in q:
            add("  Чтобы GameController знал UUID игрока без повторного parse Basic Auth.")
        elif stage == "D" and "permitAll" in q:
            add("  Spring Security и AuthFilter — разные слои; каждый может заблокировать запрос.")
        elif stage == "E" and "лобби" in q:
            add("  WAITING_FOR_PLAYERS.")
        elif stage == "E" and "первым" in q:
            add("  player1 (создатель, Symbol.X) — currentTurnPlayerId = player1Id после join.")
        elif stage == "E" and "Minimax" in q:
            add("  После хода человека, если vsComputer и игра не закончилась.")
        elif stage == "E" and "immutable" in q:
            add("  Предсказуемость: каждый шаг сервиса — новый объект, проще отладка и thread-safety.")
        elif stage == "E" and "пять" in q:
            add("  POST /game, GET /game/available, POST /game/{id}/join, GET /game/{id}, POST /game/{id}.")
        elif stage == "C" and "runtimeOnly" in q:
            add("  Драйвер нужен только при запуске JVM, не при компиляции — меньше compile classpath.")
        elif stage == "C" and "show-sql" in q:
            add("  Hibernate: insert into games (...) — видишь реальный SQL и значения колонок.")
        elif stage == "D" and "пароль" in q:
            add("  UserEntity.password в Postgres plain text (учёба); в API отдаём только UserDto без пароля.")
        elif stage == "E" and "winnerId" in q:
            add("  null — победа AI, не пользователя (ветка Symbol.O в updateGameState).")
        else:
            add("  См. соответствующий блок теории выше.")
        add("")
        add("  </details>")
        add("")

    add("---")
    add("")
    add("## Чеклист файлов части 2")
    add("")
    add("Отметь после сверки с **Сверка: файл целиком** в каждом блоке:")
    add("")
    _FILES = [
        ("Этап C", ["build.gradle.kts", "application.properties", "GameBoardEntity.java",
                    "CurrentGameEntity.java", "GameRepository.java", "GameMapper.java", "SpringConfig.java"]),
        ("Этап D", ["UserEntity.java", "UserRepository.java", "UserService.java", "UserServiceImpl.java",
                    "SignUpRequest.java", "AuthService.java", "AuthServiceImpl.java", "AuthController.java",
                    "AuthFilter.java", "SecurityConfig.java", "UserDto.java", "UserController.java"]),
        ("Этап E", ["GameState.java", "Symbol.java", "CurrentGame.java", "GameService.java", "GameServiceImpl.java",
                    "CurrentGameEntity.java (полная)", "GameMapper.java (полная)", "CreateGameRequest.java",
                    "CurrentGameDto.java", "GameWebMapper.java", "GameController.java"]),
    ]
    for stage, files in _FILES:
        add(f"### {stage}")
        add("")
        for f in files:
            add(f"- [ ] `{f}`")
        add("")
    add("**Удалить:** `GameStorage.java`, `GameRepositoryImpl.java` (этап C.8).")
    add("")
    add("### Шпаргалка команд (часть 2)")
    add("")
    add("```powershell")
    add("cd B:\\school21\\Java\\Backend\\AP1_Jv_T04B.ID_1421426-1\\src\\TicTacToe_1.2_sql_auth")
    add("$env:JAVA_HOME = \"C:\\Program Files\\Java\\jdk-21\"")
    add(".\\gradlew.bat compileJava    # после каждого блока")
    add(".\\gradlew.bat bootRun         # после C.3, C.8, D.9, E.8")
    add("```")
    add("")
    add("<details><summary>Bash</summary>")
    add("")
    add("```bash")
    add("cd src/TicTacToe_1.2_sql_auth")
    add("export JAVA_HOME=$(/usr/libexec/java_home -v 21)")
    add("./gradlew compileJava")
    add("./gradlew bootRun")
    add("```")
    add("")
    add("</details>")
    add("")
    add("**PostgreSQL:** `psql -U postgres -c \"\\l\"` — список баз; `\\dt` в tictactoe — таблицы games, users.")
    add("")
    add("**Проверка Basic Auth (после D.7):** заголовок `Authorization: Basic <Base64(login:password)>` на любой `/game/*`.")
    add("")
    add("### Карта зависимостей этапов C → D → E")
    add("")
    add("```")
    add("C: Postgres + JPA entity/repo/mapper")
    add("        ↓")
    add("D: users + Basic Auth + AuthFilter (нужен starter-security из C.2)")
    add("        ↓")
    add("E: полная игра + GameController (нужен userId из D.7 AuthFilter)")
    add("```")
    add("")
    add("Не перепрыгивай: этап E без D даст NPE на `currentUserId`. Этап C без Postgres даст connection error на bootRun.")
    add("")
    add("### application.properties — напоминание")
    add("")
    add("```properties")
    add("spring.datasource.username=ТВОЙ_ЛОГИН")
    add("spring.datasource.password=ТВОЙ_ПАРОЛЬ")
    add("```")
    add("")
    add("Замени плейсхолдеры на свои учётные данные PostgreSQL. Не коммить реальный пароль.")
    add("")
    add("### Итог части 2")
    add("")
    para_block("""
**Ты прошёл три задания T04:** (1) персистентность в PostgreSQL через JPA; (2) регистрация и Basic Auth с фильтром до контроллера; (3) PvP-лобби, полная модель игры и все эндпоинты GameController. Каждый блок v2 — теория, микро-шаги, сверка с эталонным кодом из `TicTacToe_1.2_sql_auth`.

**Что дальше.** Часть 3 покроет этапы F и G: готовые curl-сценарии для проверки API и браузерный UI. До этого убедись, что `bootRun` стартует без ошибок, таблицы `games` и `users` есть, а `POST /game` без Authorization возвращает 401.

**Если застрял.** Вернись к блоку, где впервые сломалось поведение; открой «Приложение — расширенная диагностика» выше; сверь файл целиком с проектом-эталоном только после того, как исчерпал свои правки.

**Минимальный smoke-test после E.8:** зарегистрируй пользователя → login с Basic Auth → POST /game с `{"vsComputer":true}` → POST /game/{id} с телом доски. В логах — INSERT в games. Рестарт bootRun → GET /game/{id} возвращает ту же игру.
""", 4)
    add("---")
    add("")

    add("")
    _GLOSS = [
        ("CrudRepository", "Интерфейс Spring Data: save, findById, delete без ручного SQL."),
        ("@Embeddable", "JPA: поля объекта становятся колонками таблицы хозяина."),
        ("ddl-auto=update", "Hibernate добавляет недостающие колонки при старте."),
        ("HikariCP", "Пул JDBC-соединений по умолчанию в Spring Boot."),
        ("Basic Auth", "RFC 7617: логин:пароль в Base64 в заголовке Authorization."),
        ("AuthFilter", "Свой фильтр: 401 или userId в request attribute."),
        ("SecurityFilterChain", "Цепочка Spring Security; наш AuthFilter вставлен через addFilterBefore."),
        ("permitAll", "Spring Security не требует authentication для matcher."),
        ("CURRENT_USER_ID_ATTR", "Ключ request attribute с UUID после успешного Basic Auth."),
        ("WAITING_FOR_PLAYERS", "Состояние лобби PvP до join второго игрока."),
        ("currentTurnPlayerId", "UUID игрока, чей ход при state=PLAYER_TURN."),
        ("vsComputer", "true — PvE с Minimax; false — PvP лобби."),
        ("GameMapper", "Маппер entity ↔ domain (datasource)."),
        ("GameWebMapper", "Маппер DTO ↔ domain (web)."),
        ("422 Unprocessable Entity", "Бизнес-отказ: не твой ход, игра окончена."),
    ]
    for term, defn in _GLOSS:
        add(f"**{term}** — {defn}")
        add("")
        add(f"**Подробнее:** этот термин связывает теорию и код в нескольких блоках части 2. Не заучивай определение — найди, где термин появляется в твоём проекте: открой файл, поставь breakpoint или `show-sql`, увидь эффект. Если после этапа C видишь {term.lower() if term[0].isupper() else term} в логах или аннотациях — значит, блок закрыт правильно.")
        add("")
        add("**Типичная ошибка:** путают с похожим термином из другого этапа (например, GameMapper и GameWebMapper). Держи в голове слой: datasource vs web.")
        add("")

    add("---")
    add("")
    add("*Конец части 2 v2. Следующий файл: этапы F (curl) и G (UI).*")
    add("")
    add("> **Версия генератора:** `_gen_part2.py` + `_gen_part2_blocks.py` — эталонный код из `TicTacToe_1.2_sql_auth`.")
    add("> **Плейсхолдеры БД:** `ТВОЙ_ЛОГИН` / `ТВОЙ_ПАРОЛЬ` в `application.properties`.")
    add("")
