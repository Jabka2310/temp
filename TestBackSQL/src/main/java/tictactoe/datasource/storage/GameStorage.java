package tictactoe.datasource.storage;


import tictactoe.datasource.model.CurrentGameEntity;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class GameStorage  {
    private final Map<UUID, CurrentGameEntity> games = new ConcurrentHashMap<>(); // высокопроизводительная, потокобезопасная версия HashMap

    // Сохранение игры в мапу (потом удалить)
    public void put(UUID id, CurrentGameEntity game) { games.put(id, game); }

    // Поиск игры (вытаскиваем из памяти) Так же тут защита от NullPointerExe
    public Optional<CurrentGameEntity> get(UUID id) { return Optional.ofNullable(games.get(id)); }
}
