package tictactoe.web.model;

import java.util.UUID;

/**
 * DTO текущей игры для web-слоя (JSON).
 */
public class CurrentGameDto {

    private UUID id;
    private GameBoardDto board;
    /** true — запрос первого хода компьютера (игрок играет за O). */
    private Boolean computerStarts;

    public CurrentGameDto() {
    }

    public CurrentGameDto(UUID id, GameBoardDto board) {
        this.id = id;
        this.board = board;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public GameBoardDto getBoard() {
        return board;
    }

    public void setBoard(GameBoardDto board) {
        this.board = board;
    }

    public Boolean getComputerStarts() {
        return computerStarts;
    }

    public void setComputerStarts(Boolean computerStarts) {
        this.computerStarts = computerStarts;
    }
}
