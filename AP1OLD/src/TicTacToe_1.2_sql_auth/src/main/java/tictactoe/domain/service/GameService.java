package tictactoe.domain.service;

import tictactoe.domain.model.CurrentGame;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface GameService {

    CurrentGame createGame(UUID creatorId, boolean vsComputer);

    List<CurrentGame> getAvailableGames();

    CurrentGame joinGame(UUID gameId, UUID playerId);

    Optional<CurrentGame> getGame(UUID gameId);

    CurrentGame makeMove(UUID gameId, CurrentGame incoming, UUID playerId);

    void saveGame(CurrentGame game);

    // --- методы T03 (Minimax PvE) ---
    CurrentGame getNextMove(CurrentGame game);
    CurrentGame getFirstMove(CurrentGame game);
    boolean validateBoard(CurrentGame stored, CurrentGame incoming, UUID playerId);
    CurrentGame updateGameState(CurrentGame game);
}