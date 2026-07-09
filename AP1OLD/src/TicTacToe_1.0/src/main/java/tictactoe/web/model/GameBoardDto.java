package tictactoe.web.model;

/**
 * DTO игрового поля для web-слоя (JSON).
 */
public class GameBoardDto {

    private int[][] board;

    public GameBoardDto() {
        this.board = new int[3][3];
    }

    public GameBoardDto(int[][] board) {
        this.board = board;
    }

    public int[][] getBoard() {
        return board;
    }

    public void setBoard(int[][] board) {
        this.board = board;
    }
}
