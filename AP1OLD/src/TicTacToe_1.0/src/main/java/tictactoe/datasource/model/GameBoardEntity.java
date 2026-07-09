package tictactoe.datasource.model;

/**
 * Модель игрового поля в слое datasource (хранение).
 */
public class GameBoardEntity {

    private final int[][] cells;

    public GameBoardEntity() {
        this.cells = new int[3][3];
    }

    public GameBoardEntity(int[][] cells) {
        this.cells = new int[3][3];
        for (int i = 0; i < 3; i++) {
            System.arraycopy(cells[i], 0, this.cells[i], 0, 3);
        }
    }

    public int get(int row, int col) {
        return cells[row][col];
    }

    public void set(int row, int col, int value) {
        cells[row][col] = value;
    }

    public int[][] getCells() {
        int[][] copy = new int[3][3];
        for (int i = 0; i < 3; i++) {
            System.arraycopy(cells[i], 0, copy[i], 0, 3);
        }
        return copy;
    }
}
