package tictactoe.web.mapper;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.GameBoardDto;

public final class GameWebMapper {

    private GameWebMapper() {
    }

    public static CurrentGameDto toDto(CurrentGame game) {
        if (game == null) {
            return null;
        }
        CurrentGameDto dto = new CurrentGameDto();
        dto.setId(game.getId());
        dto.setBoard(toDto(game.getBoard()));
        dto.setState(game.getState());
        dto.setPlayer1Id(game.getPlayer1Id());
        dto.setPlayer2Id(game.getPlayer2Id());
        dto.setPlayer1Symbol(game.getPlayer1Symbol());
        dto.setPlayer2Symbol(game.getPlayer2Symbol());
        dto.setCurrentTurnPlayerId(game.getCurrentTurnPlayerId());
        dto.setWinnerId(game.getWinnerId());
        dto.setVsComputer(game.isVsComputer());
        return dto;
    }

    public static CurrentGame toDomain(CurrentGameDto dto) {
        if (dto == null) {
            return null;
        }
        GameBoard board = toDomainBoard(dto.getBoard());
        return new CurrentGame(
                dto.getId(),
                board,
                dto.getState() != null ? dto.getState() : tictactoe.domain.model.GameState.PLAYER_TURN,
                dto.getPlayer1Id(),
                dto.getPlayer2Id(),
                dto.getPlayer1Symbol() != null ? dto.getPlayer1Symbol() : tictactoe.domain.model.Symbol.X,
                dto.getPlayer2Symbol() != null ? dto.getPlayer2Symbol() : tictactoe.domain.model.Symbol.O,
                dto.getCurrentTurnPlayerId(),
                dto.getWinnerId(),
                dto.isVsComputer()
        );
    }

    public static GameBoardDto toDto(GameBoard board) {
        if (board == null) {
            return null;
        }
        return new GameBoardDto(board.getCells());
    }

    public static GameBoard toDomainBoard(GameBoardDto dto) {
        if (dto == null || dto.getBoard() == null) {
            return null;
        }
        return new GameBoard(dto.getBoard());
    }
}

// DTO — то, что уходит/приходит по HTTP. CreateGameRequest — только флаг PvE/PvP.
// CurrentGameDto — полная картина для клиента. GameWebMapper — мост web ↔ domain
// (не путать с GameMapper entity ↔ domain).