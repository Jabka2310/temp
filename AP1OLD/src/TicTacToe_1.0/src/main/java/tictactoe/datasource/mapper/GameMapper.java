package tictactoe.datasource.mapper;

import tictactoe.datasource.model.CurrentGameEntity;
import tictactoe.datasource.model.GameBoardEntity;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;

/**
 * Маппер между моделями domain и datasource.
 */
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
        GameBoardEntity boardEntity = toEntityBoard(game.getBoard());
        return new CurrentGameEntity(game.getId(), boardEntity);
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
}
