package tictactoe.domain.model;

import java.util.UUID;

public class CurrentGame {

    private final UUID id;
    private final GameBoard board;
    private final GameState state;
    private final UUID player1Id;
    private final UUID player2Id;           // null если vsComputer или ждём игрока
    private final Symbol player1Symbol;
    private final Symbol player2Symbol;
    private final UUID currentTurnPlayerId; // чей ход (при PLAYER_TURN)
    private final UUID winnerId;            // кто победил (при WIN)
    private final boolean vsComputer;

    public CurrentGame(UUID id, GameBoard board, GameState state,
                       UUID player1Id, UUID player2Id,
                       Symbol player1Symbol, Symbol player2Symbol,
                       UUID currentTurnPlayerId, UUID winnerId,
                       boolean vsComputer) {
        this.id = id;
        this.board = board;
        this.state = state;
        this.player1Id = player1Id;
        this.player2Id = player2Id;
        this.player1Symbol = player1Symbol;
        this.player2Symbol = player2Symbol;
        this.currentTurnPlayerId = currentTurnPlayerId;
        this.winnerId = winnerId;
        this.vsComputer = vsComputer;
    }

    /** Упрощённый конструктор для обратной совместимости (T03) */
    public CurrentGame(UUID id, GameBoard board) {
        this(id, board, GameState.PLAYER_TURN,
                null, null, Symbol.X, Symbol.O,
                null, null, true);
    }

    public UUID getId() { return id; }
    public GameBoard getBoard() { return board; }
    public GameState getState() { return state; }
    public UUID getPlayer1Id() { return player1Id; }
    public UUID getPlayer2Id() { return player2Id; }
    public Symbol getPlayer1Symbol() { return player1Symbol; }
    public Symbol getPlayer2Symbol() { return player2Symbol; }
    public UUID getCurrentTurnPlayerId() { return currentTurnPlayerId; }
    public UUID getWinnerId() { return winnerId; }
    public boolean isVsComputer() { return vsComputer; }

    public CurrentGame withBoard(GameBoard newBoard) {
        return new CurrentGame(id, newBoard, state, player1Id, player2Id,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withState(GameState newState) {
        return new CurrentGame(id, board, newState, player1Id, player2Id,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withCurrentTurn(UUID turnPlayerId) {
        return new CurrentGame(id, board, state, player1Id, player2Id,
                player1Symbol, player2Symbol, turnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withPlayer2(UUID p2) {
        return new CurrentGame(id, board, state, player1Id, p2,
                player1Symbol, player2Symbol, currentTurnPlayerId, winnerId, vsComputer);
    }

    public CurrentGame withWinner(UUID winner) {
        return new CurrentGame(id, board, GameState.WIN, player1Id, player2Id,
                player1Symbol, player2Symbol, null, winner, vsComputer);
    }

    public CurrentGame asDraw() {
        return new CurrentGame(id, board, GameState.DRAW, player1Id, player2Id,
                player1Symbol, player2Symbol, null, null, vsComputer);
    }

    /** UUID игрока, у которого symbol X или O */
    public UUID getPlayerIdBySymbol(Symbol symbol) {
        if (symbol == player1Symbol) return player1Id;
        if (symbol == player2Symbol) return player2Id;
        return null;
    }

    public Symbol getSymbolByPlayerId(UUID playerId) {
        if (playerId != null && playerId.equals(player1Id)) return player1Symbol;
        if (playerId != null && playerId.equals(player2Id)) return player2Symbol;
        return null;
    }
}

// раньше игра = id + доска. Теперь ещё игроки, символы, чей ход,
// победитель, PvE или PvP. Методы withBoard, withState… — immutable-стиль:
// не мутируем объект, а создаём копию с изменением (удобно в сервисе).