package tictactoe.web.controller;

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
// POST /game, GET /game/available, POST /game/{id}/join, GET /game/{id} плюс старый POST /game/{id} для хода.