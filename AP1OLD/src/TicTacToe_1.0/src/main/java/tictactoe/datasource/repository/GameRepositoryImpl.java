package tictactoe.datasource.repository;

import tictactoe.datasource.mapper.GameMapper;
import tictactoe.datasource.model.CurrentGameEntity;
import tictactoe.datasource.storage.GameStorage;
import tictactoe.domain.model.CurrentGame;

import java.util.Optional;
import java.util.UUID;

/**
 * Реализация репозитория для работы с хранилищем игр.
 */
public class GameRepositoryImpl implements GameRepository {

    private final GameStorage storage;

    public GameRepositoryImpl(GameStorage storage) {
        this.storage = storage;
    }

    @Override
    public void save(CurrentGame game) {
        CurrentGameEntity entity = GameMapper.toEntity(game);
        storage.put(game.getId(), entity);
    }

    @Override
    public Optional<CurrentGame> findById(UUID id) {
        return storage.get(id).map(GameMapper::toDomain);
    }
}
