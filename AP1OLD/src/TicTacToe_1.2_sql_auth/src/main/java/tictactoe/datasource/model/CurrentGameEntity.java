package tictactoe.datasource.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;

import java.util.UUID;

@Entity
@Table(name = "games")
public class CurrentGameEntity {

    @Id
    private UUID id;

    @Embedded
    private GameBoardEntity board;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private GameState state;

    @Column(name = "player1_id")
    private UUID player1Id;

    @Column(name = "player2_id")
    private UUID player2Id;

    @Enumerated(EnumType.STRING)
    @Column(name = "player1_symbol")
    private Symbol player1Symbol;

    @Enumerated(EnumType.STRING)
    @Column(name = "player2_symbol")
    private Symbol player2Symbol;

    @Column(name = "current_turn_player_id")
    private UUID currentTurnPlayerId;

    @Column(name = "winner_id")
    private UUID winnerId;

    @Column(name = "vs_computer", nullable = false)
    private boolean vsComputer;

    public CurrentGameEntity() {
        this.board = new GameBoardEntity();
        this.state = GameState.PLAYER_TURN;
        this.vsComputer = false;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public GameBoardEntity getBoard() { return board; }
    public void setBoard(GameBoardEntity board) { this.board = board; }

    public GameState getState() { return state; }
    public void setState(GameState state) { this.state = state; }

    public UUID getPlayer1Id() { return player1Id; }
    public void setPlayer1Id(UUID player1Id) { this.player1Id = player1Id; }

    public UUID getPlayer2Id() { return player2Id; }
    public void setPlayer2Id(UUID player2Id) { this.player2Id = player2Id; }

    public Symbol getPlayer1Symbol() { return player1Symbol; }
    public void setPlayer1Symbol(Symbol player1Symbol) { this.player1Symbol = player1Symbol; }

    public Symbol getPlayer2Symbol() { return player2Symbol; }
    public void setPlayer2Symbol(Symbol player2Symbol) { this.player2Symbol = player2Symbol; }

    public UUID getCurrentTurnPlayerId() { return currentTurnPlayerId; }
    public void setCurrentTurnPlayerId(UUID currentTurnPlayerId) { this.currentTurnPlayerId = currentTurnPlayerId; }

    public UUID getWinnerId() { return winnerId; }
    public void setWinnerId(UUID winnerId) { this.winnerId = winnerId; }

    public boolean isVsComputer() { return vsComputer; }
    public void setVsComputer(boolean vsComputer) { this.vsComputer = vsComputer; }
}

// те же поля, что в domain, но с JPA-колонками. Hibernate добавит колонки в games (или обновит схему).
// @Enumerated(STRING) — в БД хранится WAITING_FOR_PLAYERS, а не число.