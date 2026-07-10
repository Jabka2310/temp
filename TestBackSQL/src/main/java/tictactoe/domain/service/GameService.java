package tictactoe.domain.service;

import tictactoe.domain.model.CurrentGame;

public interface GameService {
    CurrentGame getNextMove(CurrentGame game); // ход пу через минМакс, ПОЛСЕ хода игрока
    boolean validateBoard(CurrentGame game); //  проверка на изменение старых клеток
    boolean isGameEnded(CurrentGame game); //  завершена ли игра
    CurrentGame getFirstMove(CurrentGame game); //  первый ход ПК (когда игрок играет за о)
}
