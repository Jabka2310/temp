package tictactoe.web.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.service.GameService;
import tictactoe.web.mapper.GameWebMapper;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.ErrorResponse;

import java.util.UUID;

/**
 * REST-контроллер для игры в крестики-нолики.
 * POST /game/{uuid} — принять ход пользователя и вернуть игру с ходом компьютера.
 */
@RestController
@RequestMapping("/game")
public class GameController {

    private final GameService gameService;
    private final tictactoe.datasource.repository.GameRepository gameRepository;

    public GameController(GameService gameService,
                          tictactoe.datasource.repository.GameRepository gameRepository) {
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

        // Запрос первого хода компьютера (игрок играет за O)
        if (Boolean.TRUE.equals(request.getComputerStarts()) && isBoardEmpty(game.getBoard())) {
            CurrentGame withFirstMove = gameService.getFirstMove(game);
            gameRepository.save(withFirstMove);
            return ResponseEntity.ok(GameWebMapper.toDto(withFirstMove));
        }

        if (!gameService.validateBoard(game)) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                    .body(new ErrorResponse("Некорректное состояние игры: изменены предыдущие ходы или неверный ход"));
        }

        if (gameService.isGameEnded(game)) {
            return ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY)
                    .body(new ErrorResponse("Игра уже завершена"));
        }

        CurrentGame withComputerMove = gameService.getNextMove(game);
        gameRepository.save(withComputerMove);

        return ResponseEntity.ok(GameWebMapper.toDto(withComputerMove));
    }

    private static boolean isBoardEmpty(tictactoe.domain.model.GameBoard board) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board.get(i, j) != 0) return false;
            }
        }
        return true;
    }
}
