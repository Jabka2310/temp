package tictactoe.datasource.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import tictactoe.domain.model.GameBoard;

/**
 * Доска 3x3 как встраиваемый объект в таблице games.
 * 9 отдельных колонок: cell_00 ... cell_22
 */
@Embeddable
public class GameBoardEntity {

    @Column(name = "cell_00") private int cell00;
    @Column(name = "cell_01") private int cell01;
    @Column(name = "cell_02") private int cell02;
    @Column(name = "cell_10") private int cell10;
    @Column(name = "cell_11") private int cell11;
    @Column(name = "cell_12") private int cell12;
    @Column(name = "cell_20") private int cell20;
    @Column(name = "cell_21") private int cell21;
    @Column(name = "cell_22") private int cell22;

    public GameBoardEntity() {
    }

    public GameBoardEntity(int[][] cells) {
        cell00 = cells[0][0]; cell01 = cells[0][1]; cell02 = cells[0][2];
        cell10 = cells[1][0]; cell11 = cells[1][1]; cell12 = cells[1][2];
        cell20 = cells[2][0]; cell21 = cells[2][1]; cell22 = cells[2][2];
    }

    public int[][] getCells() {
        return new int[][]{
                {cell00, cell01, cell02},
                {cell10, cell11, cell12},
                {cell20, cell21, cell22}
        };
    }

    public void setFromBoard(int[][] cells) {
        cell00 = cells[0][0]; cell01 = cells[0][1]; cell02 = cells[0][2];
        cell10 = cells[1][0]; cell11 = cells[1][1]; cell12 = cells[1][2];
        cell20 = cells[2][0]; cell21 = cells[2][1]; cell22 = cells[2][2];
    }

    public int get(int row, int col) {
        return getCells()[row][col];
    }

    public void set(int row, int col, int value) {
        switch (row * GameBoard.SIZE + col) {
            case 0 -> cell00 = value;
            case 1 -> cell01 = value;
            case 2 -> cell02 = value;
            case 3 -> cell10 = value;
            case 4 -> cell11 = value;
            case 5 -> cell12 = value;
            case 6 -> cell20 = value;
            case 7 -> cell21 = value;
            case 8 -> cell22 = value;
            default -> throw new IllegalArgumentException("Invalid cell");
        }
    }
}

//Замена двумерных массивов, т.к jpa плохо хранит двумерные массивы
//@Embeddable — «кусок таблицы», не отдельная таблица. Доска ляжет колонками cell_00…cell_22 внутри games.
//setFromBoard нужен мапперу — копирует int[][] в поля.
