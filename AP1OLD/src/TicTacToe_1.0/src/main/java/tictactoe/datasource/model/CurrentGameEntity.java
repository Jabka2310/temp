package tictactoe.datasource.model;

import java.util.UUID;

/**
 * Модель текущей игры в слое datasource (хранение).
 */
public class CurrentGameEntity {

    private final UUID id;
    private final GameBoardEntity board;

    public CurrentGameEntity(UUID id, GameBoardEntity board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() {
        return id;
    }

    public GameBoardEntity getBoard() {
        return board;
    }
}
