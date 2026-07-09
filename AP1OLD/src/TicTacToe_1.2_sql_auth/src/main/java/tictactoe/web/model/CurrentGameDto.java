package tictactoe.web.model;

import tictactoe.domain.model.GameState;
import tictactoe.domain.model.Symbol;

import java.util.UUID;

public class CurrentGameDto {

    private UUID id;
    private GameBoardDto board;
    private GameState state;
    private UUID player1Id;
    private UUID player2Id;
    private Symbol player1Symbol;
    private Symbol player2Symbol;
    private UUID currentTurnPlayerId;
    private UUID winnerId;
    private boolean vsComputer;
    private Boolean computerStarts; // legacy для PvE «играю за O»

    public CurrentGameDto() {
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public GameBoardDto getBoard() { return board; }
    public void setBoard(GameBoardDto board) { this.board = board; }

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

    public Boolean getComputerStarts() { return computerStarts; }
    public void setComputerStarts(Boolean computerStarts) { this.computerStarts = computerStarts; }
}