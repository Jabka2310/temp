package tictactoe.domain.service;

import java.util.Optional;
import java.util.UUID;

public interface UserService {
    boolean register(String login, String password); // Вернет тру - если успешная авторизация
    Optional<UUID> authenticate(String login, String password); // Вернет айди если авторизация успешна
    Optional<String> findLoginById(UUID id);
}
