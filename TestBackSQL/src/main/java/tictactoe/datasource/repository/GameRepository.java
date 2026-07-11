package tictactoe.datasource.repository;

import tictactoe.domain.model.CurrentGame;

import java.util.Optional;
import java.util.UUID;

public interface GameRepository {
    void save(CurrentGame game); // Сохранение состояния после каждого хода
    Optional<CurrentGame> findById(UUID id);
}
