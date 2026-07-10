package tictactoe.domain.model;

import java.util.UUID;

public class CurrentGame {
    private final UUID id;
    private final GameBoard board;

    public CurrentGame(UUID id, GameBoard board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() { return id; }
    // Сервис делает copy() перед ходом
    public GameBoard getBoard() { return board; }

}
