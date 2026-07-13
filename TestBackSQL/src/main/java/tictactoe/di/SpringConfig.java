package tictactoe.di;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import tictactoe.datasource.repository.GameRepository;
import tictactoe.datasource.repository.GameRepositoryImpl;
import tictactoe.datasource.service.GameServiceImpl;
import tictactoe.datasource.storage.GameStorage;
import tictactoe.domain.service.GameService;

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
