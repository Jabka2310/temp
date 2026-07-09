package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;
import tictactoe.domain.service.GameService;
import tictactoe.datasource.mapper.GameMapper;
import tictactoe.datasource.repository.GameRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class GameServiceImpl implements GameService {

    private final GameRepository gameRepository;

    public GameServiceImpl(GameRepository gameRepository) {
        this.gameRepository = gameRepository;
    }

    @Override
    public void saveGame(CurrentGame game) {
        gameRepository.save(GameMapper.toEntity(game));
    }

    @Override
    public CurrentGame createGame(UUID creatorId, boolean vsComputer) {
        UUID gameId = UUID.randomUUID();
        GameBoard emptyBoard = new GameBoard();

        if (vsComputer) {
            return new CurrentGame(
                    gameId, emptyBoard,
                    GameState.PLAYER_TURN,
                    creatorId, null,
                    Symbol.X, Symbol.O,
                    creatorId,
                    null,
                    true
            );
        }

        return new CurrentGame(
                gameId, emptyBoard,
                GameState.WAITING_FOR_PLAYERS,
                creatorId, null,
                Symbol.X, Symbol.O,
                null, null,
                false
        );
    }

    @Override
    public List<CurrentGame> getAvailableGames() {
        return gameRepository.findByState(GameState.WAITING_FOR_PLAYERS)
                .stream()
                .map(GameMapper::toDomain)
                .toList();
    }

    @Override
    public CurrentGame joinGame(UUID gameId, UUID playerId) {
        CurrentGame game = getGame(gameId)
                .orElseThrow(() -> new IllegalArgumentException("Game not found"));

        if (game.getState() != GameState.WAITING_FOR_PLAYERS) {
            throw new IllegalStateException("Game is not waiting for players");
        }
        if (game.getPlayer1Id().equals(playerId)) {
            throw new IllegalStateException("Cannot join your own game");
        }

        return new CurrentGame(
                game.getId(), game.getBoard(),
                GameState.PLAYER_TURN,
                game.getPlayer1Id(), playerId,
                game.getPlayer1Symbol(), Symbol.O,
                game.getPlayer1Id(),
                null,
                false
        );
    }

    @Override
    public Optional<CurrentGame> getGame(UUID gameId) {
        return gameRepository.findById(gameId).map(GameMapper::toDomain);
    }

    @Override
    public CurrentGame makeMove(UUID gameId, CurrentGame incoming, UUID playerId) {
        CurrentGame stored = getGame(gameId)
                .orElseThrow(() -> new IllegalArgumentException("Game not found"));

        if (stored.getState() != GameState.PLAYER_TURN) {
            throw new IllegalStateException("Game is not in progress");
        }
        if (!playerId.equals(stored.getCurrentTurnPlayerId())) {
            throw new IllegalStateException("Not your turn");
        }
        if (!validateBoard(stored, incoming, playerId)) {
            throw new IllegalStateException("Invalid board");
        }

        CurrentGame afterPlayerMove = stored.withBoard(incoming.getBoard());
        CurrentGame afterPlayerMoveChecked = updateGameState(afterPlayerMove);

        if (afterPlayerMoveChecked.getState() == GameState.WIN
                || afterPlayerMoveChecked.getState() == GameState.DRAW) {
            return afterPlayerMoveChecked;
        }

        if (stored.isVsComputer()) {
            CurrentGame afterComputer = getNextMove(afterPlayerMoveChecked);
            return updateGameState(afterComputer);
        }

        UUID nextPlayer = stored.getPlayer1Id().equals(playerId)
                ? stored.getPlayer2Id()
                : stored.getPlayer1Id();

        return updateGameState(afterPlayerMoveChecked.withCurrentTurn(nextPlayer));
    }

    @Override
    public CurrentGame getFirstMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        board.set(1, 1, GameBoard.COMPUTER);
        CurrentGame afterComputer = game.withBoard(board);
        return updateGameState(afterComputer.withCurrentTurn(game.getPlayer1Id()));
    }

    @Override
    public CurrentGame getNextMove(CurrentGame game) {
        GameBoard board = game.getBoard().copy();
        int[] bestMove = findBestMove(board);
        if (bestMove != null) {
            board.set(bestMove[0], bestMove[1], GameBoard.COMPUTER);
        }
        return game.withBoard(board);
    }

    @Override
    public boolean validateBoard(CurrentGame stored, CurrentGame incoming, UUID playerId) {
        Symbol playerSymbol = stored.getSymbolByPlayerId(playerId);
        if (playerSymbol == null) {
            return false;
        }
        int expectedValue = playerSymbol.toBoardValue();
        return boardsMatchExceptOneMove(stored.getBoard(), incoming.getBoard(), expectedValue);
    }

    @Override
    public CurrentGame updateGameState(CurrentGame game) {
        int winnerValue = evaluateWinner(game.getBoard());

        if (winnerValue != 0) {
            Symbol winnerSymbol = Symbol.fromBoardValue(winnerValue);
            UUID winnerId = game.getPlayerIdBySymbol(winnerSymbol);
            if (game.isVsComputer() && winnerSymbol == Symbol.O) {
                winnerId = null; // победа компьютера
            }
            return game.withWinner(winnerId);
        }

        if (isBoardFull(game.getBoard())) {
            return game.asDraw();
        }

        return game.withState(GameState.PLAYER_TURN);
    }

    private boolean boardsMatchExceptOneMove(GameBoard stored, GameBoard incoming, int expectedValue) {
        int diff = 0;
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                int s = stored.get(i, j);
                int inc = incoming.get(i, j);
                if (s != inc) {
                    if (s == GameBoard.EMPTY && inc == expectedValue) {
                        diff++;
                    } else {
                        return false;
                    }
                }
            }
        }
        return diff == 1;
    }

    private boolean isBoardFull(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            for (int j = 0; j < GameBoard.SIZE; j++) {
                if (board.get(i, j) == GameBoard.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    private int evaluateWinner(GameBoard board) {
        for (int i = 0; i < GameBoard.SIZE; i++) {
            if (board.get(i, 0) != GameBoard.EMPTY
                    && board.get(i, 0) == board.get(i, 1)
                    && board.get(i, 1) == board.get(i, 2)) {
                return board.get(i, 0);
            }
            if (board.get(0, i) != GameBoard.EMPTY
                    && board.get(0, i) == board.get(1, i)
                    && board.get(1, i) == board.get(2, i)) {
                return board.get(0, i);
            }
        }
        if (board.get(0, 0) != GameBoard.EMPTY
                && board.get(0, 0) == board.get(1, 1)
                && board.get(1, 1) == board.get(2, 2)) {
            return board.get(0, 0);
        }
        if (board.get(0, 2) != GameBoard.EMPTY
                && board.get(0, 2) == board.get(1, 1)
                && board.get(1, 1) == board.get(2, 0)) {
            return board.get(0, 2);
        }
        return 0;
    }

    // --- Minimax (без изменений из T03) ---

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

    private int minimax(GameBoard board, int depth, boolean isMax) {
        int score = evaluateMinimax(board);
        if (score == 10) return score - depth;
        if (score == -10) return score + depth;
        if (isBoardFull(board)) return 0;

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

    private int evaluateMinimax(GameBoard board) {
        int w = evaluateWinner(board);
        if (w == GameBoard.COMPUTER) return 10;
        if (w == GameBoard.PLAYER) return -10;
        return 0;
    }
}