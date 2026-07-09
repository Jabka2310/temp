package tictactoe.datasource.storage;

import tictactoe.datasource.model.CurrentGameEntity;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Потокобезопасное хранилище текущих игр.
 */
public class GameStorage {

    private final Map<UUID, CurrentGameEntity> games = new ConcurrentHashMap<>();

    public void put(UUID id, CurrentGameEntity game) {
        games.put(id, game);
    }

    public Optional<CurrentGameEntity> get(UUID id) {
        return Optional.ofNullable(games.get(id));
    }
}
