package tictactoe.domain.model;

/**
 * Модель игрового поля в виде целочисленной матрицы 3x3.
 * 0 — пустая клетка, 1 — крестик (игрок), 2 — нолик (компьютер).
 */
public class GameBoard {

    public static final int SIZE = 3;
    public static final int EMPTY = 0;
    public static final int PLAYER = 1;  // X
    public static final int COMPUTER = 2; // O

    private final int[][] cells;

    public GameBoard() {
        this.cells = new int[SIZE][SIZE];
    }

    public GameBoard(int[][] cells) {
        this.cells = new int[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            System.arraycopy(cells[i], 0, this.cells[i], 0, SIZE);
        }
    }

    public int get(int row, int col) {
        return cells[row][col];
    }

    public void set(int row, int col, int value) {
        cells[row][col] = value;
    }

    public int[][] getCells() {
        int[][] copy = new int[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            System.arraycopy(cells[i], 0, copy[i], 0, SIZE);
        }
        return copy;
    }

    public GameBoard copy() {
        return new GameBoard(cells);
    }
}
