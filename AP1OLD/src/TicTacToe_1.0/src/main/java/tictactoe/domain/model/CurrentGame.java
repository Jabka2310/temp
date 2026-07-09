package tictactoe.domain.model;

import java.util.UUID;

/**
 * Модель текущей игры: уникальный идентификатор и игровое поле.
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
}
