package tictactoe.datasource.mapper;

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
// Репозиторий по-прежнему работает только с entity — domain остаётся чистым от @Column.