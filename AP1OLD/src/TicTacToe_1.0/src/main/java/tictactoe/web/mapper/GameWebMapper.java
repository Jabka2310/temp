package tictactoe.web.mapper;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.GameBoardDto;

/**
 * Маппер между моделями domain и web (DTO).
 */
public final class GameWebMapper {

    private GameWebMapper() {
    }

    public static CurrentGameDto toDto(CurrentGame game) {
        if (game == null) {
            return null;
        }
        GameBoardDto boardDto = toDto(game.getBoard());
        return new CurrentGameDto(game.getId(), boardDto);
    }

    public static CurrentGame toDomain(CurrentGameDto dto) {
        if (dto == null) {
            return null;
        }
        GameBoard board = toDomainBoard(dto.getBoard());
        return new CurrentGame(dto.getId(), board);
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
