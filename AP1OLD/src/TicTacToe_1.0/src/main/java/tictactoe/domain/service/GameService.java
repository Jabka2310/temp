package tictactoe.domain.service;

import tictactoe.domain.model.CurrentGame;

/**
 * Интерфейс сервиса игровой логики.
 */
public interface GameService {

    /**
     * Получить следующий ход текущей игры алгоритмом «Минимакс»
     * (ход компьютера после хода пользователя).
     *
     * @param game текущая игра с обновлённым полем после хода пользователя
     * @return текущая игра с полем после хода компьютера
     */
    CurrentGame getNextMove(CurrentGame game);

    /**
     * Валидация игрового поля: проверка, что предыдущие ходы не изменены.
     *
     * @param game текущая игра с полем от клиента
     * @return true, если поле валидно
     */
    boolean validateBoard(CurrentGame game);

    /**
     * Проверка окончания игры (победа, ничья).
     *
     * @param game текущая игра
     * @return true, если игра завершена
     */
    boolean isGameEnded(CurrentGame game);

    /**
     * Первый ход компьютера (пустое поле → один ход нолика).
     * Используется, когда игрок выбрал играть за O.
     *
     * @param game текущая игра с пустым полем
     * @return игра с одним ходом компьютера (2) на доске
     */
    CurrentGame getFirstMove(CurrentGame game);
}
