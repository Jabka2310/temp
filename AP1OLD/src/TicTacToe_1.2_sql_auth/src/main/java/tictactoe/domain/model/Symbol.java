package tictactoe.domain.model;

public enum Symbol {
    X, O;

    public int toBoardValue() {
        return this == X ? 1 : 2;
    }

    public static Symbol fromBoardValue(int value) {
        return value == 1 ? X : O;
    }
}
// Меняем крестики и нолики на 1 и 2 И наоборот