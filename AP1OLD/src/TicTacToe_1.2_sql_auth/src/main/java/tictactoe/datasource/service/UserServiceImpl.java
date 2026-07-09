package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.datasource.model.UserEntity;
import tictactoe.datasource.repository.UserRepository;
import tictactoe.domain.service.UserService;

import java.util.Optional;
import java.util.UUID;

@Service
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public boolean register(String login, String password) {
        if (login == null || password == null || login.isBlank() || password.isBlank()) return false;
        if (userRepository.existsByLogin(login)) return false;
        UUID id = UUID.randomUUID();
        userRepository.save(new UserEntity(id, login, password));
        return true;
    }

    @Override
    public Optional<UUID> authenticate(String login, String password) {
        return userRepository.findByLogin(login)
                .filter(user -> user.getPassword().equals(password))
                .map(UserEntity::getId);
    }

    @Override
    public Optional<String> findLoginById(UUID id) {
        return userRepository.findById(id).map(UserEntity::getLogin);
    }
}
