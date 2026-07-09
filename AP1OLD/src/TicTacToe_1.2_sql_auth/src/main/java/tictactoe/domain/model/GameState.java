package tictactoe.domain.model;

public enum GameState {
    WAITING_FOR_PLAYERS, // ждём второго игрока
    PLAYER_TURN, // ход игрока
    DRAW, // ничья
    WIN //Победа
}
