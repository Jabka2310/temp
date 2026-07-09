package tictactoe.datasource.repository;

import tictactoe.domain.model.CurrentGame;

import java.util.Optional;
import java.util.UUID;

/**
 * Репозиторий для работы с хранилищем игр.
 */
public interface GameRepository {

    /**
     * Сохранить текущую игру.
     */
    void save(CurrentGame game);

    /**
     * Получить текущую игру по UUID.
     */
    Optional<CurrentGame> findById(UUID id);
}
