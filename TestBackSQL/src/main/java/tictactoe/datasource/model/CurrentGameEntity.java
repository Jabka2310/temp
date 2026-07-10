package tictactoe.datasource.model;

import tictactoe.domain.model.GameBoard;

import java.util.UUID;

public class CurrentGameEntity {
    private UUID id;
    private GameBoardEntity board;

    public CurrentGameEntity() {}

    public CurrentGameEntity(UUID id, GameBoardEntity board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public GameBoardEntity getBoard() { return board; }
    public void setBoard(GameBoardEntity board) { this.board = board; }
}
