package tictactoe.di;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import tictactoe.datasource.repository.GameRepository;
import tictactoe.datasource.repository.GameRepositoryImpl;
import tictactoe.datasource.service.GameServiceImpl;
import tictactoe.datasource.storage.GameStorage;
import tictactoe.domain.service.GameService;

/**
 * Spring Configuration: граф зависимостей.
 * — Хранилище игр (singleton)
 * — Репозиторий для работы с хранилищем
 * — Сервис для работы с репозиторием
 */
@Configuration
public class SpringConfig {

    @Bean
    public GameStorage gameStorage() {
        return new GameStorage();
    }

    @Bean
    public GameRepository gameRepository(GameStorage gameStorage) {
        return new GameRepositoryImpl(gameStorage);
    }

    @Bean
    public GameService gameService(GameRepository gameRepository) {
        return new GameServiceImpl(gameRepository);
    }
}
