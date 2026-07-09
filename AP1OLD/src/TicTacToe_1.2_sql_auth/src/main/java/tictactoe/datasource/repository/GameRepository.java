package tictactoe.datasource.repository;

import org.springframework.data.repository.CrudRepository;
import tictactoe.datasource.model.CurrentGameEntity;
import tictactoe.domain.model.CurrentGame;
import tictactoe.domain.model.GameState;

import java.util.List;
import java.util.UUID;

public interface GameRepository extends CrudRepository<CurrentGameEntity, UUID>{
    List<CurrentGameEntity> findByState(GameState state);
}

//findByState(WAITING_FOR_PLAYERS) — список игр для GET /game/available.
// Spring Data снова генерирует SQL по имени метода.