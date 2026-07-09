package tictactoe.web.model;

import tictactoe.domain.model.GameBoard;

public class GameBoardDto {
    private int[][] board;

    public GameBoardDto() {
        this.board = new int[GameBoard.SIZE][GameBoard.SIZE];
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
