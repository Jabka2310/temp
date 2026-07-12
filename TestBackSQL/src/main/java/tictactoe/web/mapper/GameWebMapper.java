package tictactoe.web.mapper;

import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameBoard;
import tictactoe.web.model.CurrentGameDto;
import tictactoe.web.model.GameBoardDto;

import static tictactoe.datasource.mapper.GameMapper.toDomainBoard;

public final class GameWebMapper {
    private GameWebMapper(){}

    public static CurrentGameDto toDto(CurrentGame game) {
        if (game == null) return null;
        return new CurrentGameDto(game.getId(), toDto(game.getBoard()));
    }

    public static CurrentGame toDomain(CurrentGameDto dto) {
        if (dto == null) return null;
        return new CurrentGame(dto.getId(), toDomainBoard(dto.getBoard()));
    }

    public static GameBoardDto toDto (GameBoard board) {
        if (board == null) return null;
        return new GameBoardDto(board.getCells());
    }

    public static GameBoard toDomainBoard(GameBoardDto dto) {
        if (dto == null) return null;
        return new GameBoard(dto.getBoard());
    }
}
