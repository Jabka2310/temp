package tictactoe.datasource.service;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.service.GameService;
import tictactoe.datasource.repository.GameRepository;

/**
 * Реализация сервиса игровой логики с алгоритмом Минимакс.
 */
public class GameServiceImpl implements GameService {

    private final GameRepository repository;

    public GameServiceImpl(GameRepository repository) {
        this.repository = repository;
    }

    @Override
    public CurrentGame getNextMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        int[] bestMove = findBestMove(board);
        if (bestMove != null) {
            board.set(bestMove[0], bestMove[1], GameBoard.COMPUTER);
        }
        return new CurrentGame(game.getId(), board);
    }

    @Override
    public CurrentGame getFirstMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        // Первый ход компьютера — в центр (оптимально в крестиках-ноликах)
        board.set(1, 1, GameBoard.COMPUTER);
        return new CurrentGame(game.getId(), board);
    }

    @Override
    public boolean validateBoard(CurrentGame game) {
        return repository.findById(game.getId())
                .map(stored -> boardsMatchExceptOnePlayerMove(stored.getBoard(), game.getBoard()))
                .orElseGet(() -> isFirstMoveOnlyOnePlayer(game.getBoard()));
    }

    /** Первый ход: на поле ровно один ход игрока (1). */
    private boolean isFirstMoveOnlyOnePlayer(GameBoard board) {
        int count = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.PLAYER) count++;
                else if (board.get(i, j) != GameBoard.EMPTY) return false; // уже есть O — не первый ход
            }
        }
        return count == 1;
    }

    @Override
    public boolean isGameEnded(CurrentGame game) {
        GameBoard board = game.getBoard();
        return hasWinner(board) || isDraw(board);
    }

    /**
     * Проверка: поле от клиента совпадает с сохранённым, кроме ровно одного нового хода игрока (одна новая 1).
     */
    private boolean boardsMatchExceptOnePlayerMove(GameBoard stored, GameBoard incoming) {
        int playerDiff = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                int s = stored.get(i, j);
                int inc = incoming.get(i, j);
                if (s != inc) {
                    if (s == GameBoard.EMPTY && inc == GameBoard.PLAYER) {
                        playerDiff++;
                    } else {
                        return false; // изменили чужой ход или стёрли ход
                    }
                }
            }
        }
        return playerDiff == 1;
    }

    private boolean hasWinner(GameBoard board) {
        return evaluate(board) != 0;
    }

    private boolean isDraw(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Минимакс: найти лучший ход для компьютера (O).
     */
    private int[] findBestMove(GameBoard board) {
        int bestScore = Integer.MIN_VALUE;
        int[] bestMove = null;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    board.set(i, j, GameBoard.COMPUTER);
                    int score = minimax(board, 0, false);
                    board.set(i, j, GameBoard.EMPTY);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = new int[]{i, j};
                    }
                }
            }
        }
        return bestMove;
    }

    /**
     * Минимакс: компьютер максимизирует, игрок минимизирует.
     * +10 за победу O, -10 за победу X, 0 за ничью.
     */
    private int minimax(GameBoard board, int depth, boolean isMax) {
        int score = evaluate(board);
        if (score == 10) return score - depth;
        if (score == -10) return score + depth;
        if (isDraw(board)) return 0;

        if (isMax) {
            int best = Integer.MIN_VALUE;
            for (int i = 0; i < GameBoard.SIZE; i++) {
                for (int j = 0; j < GameBoard.SIZE; j++) {
                    if (board.get(i, j) == GameBoard.EMPTY) {
                        board.set(i, j, GameBoard.COMPUTER);
                        best = Math.max(best, minimax(board, depth + 1, false));
                        board.set(i, j, GameBoard.EMPTY);
                    }
                }
            }
            return best;
        } else {
            int best = Integer.MAX_VALUE;
            for (int i = 0; i < GameBoard.SIZE; i++) {
                for (int j = 0; j < GameBoard.SIZE; j++) {
                    if (board.get(i, j) == GameBoard.EMPTY) {
                        board.set(i, j, GameBoard.PLAYER);
                        best = Math.min(best, minimax(board, depth + 1, true));
                        board.set(i, j, GameBoard.EMPTY);
                    }
                }
            }
            return best;
        }
    }

    /**
     * Оценка позиции: +10 если выигрыш O, -10 если выигрыш X, 0 иначе.
     */
    private int evaluate(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            if (board.get(i, 0) == board.get(i, 1) && board.get(i, 1) == board.get(i, 2)) {
                if (board.get(i, 0) == GameBoard.COMPUTER) return 10;
                if (board.get(i, 0) == GameBoard.PLAYER) return -10;
            }
            if (board.get(0, i) == board.get(1, i) && board.get(1, i) == board.get(2, i)) {
                if (board.get(0, i) == GameBoard.COMPUTER) return 10;
                if (board.get(0, i) == GameBoard.PLAYER) return -10;
            }
        }
        if (board.get(0, 0) == board.get(1, 1) && board.get(1, 1) == board.get(2, 2)) {
            if (board.get(0, 0) == GameBoard.COMPUTER) return 10;
            if (board.get(0, 0) == GameBoard.PLAYER) return -10;
        }
        if (board.get(0, 2) == board.get(1, 1) && board.get(1, 1) == board.get(2, 0)) {
            if (board.get(0, 2) == GameBoard.COMPUTER) return 10;
            if (board.get(0, 2) == GameBoard.PLAYER) return -10;
        }
        return 0;
    }
}
