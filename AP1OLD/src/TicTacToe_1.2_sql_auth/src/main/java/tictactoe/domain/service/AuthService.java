package tictactoe.domain.service;

import tictactoe.web.model.SignUpRequest;

import java.util.UUID;

public interface AuthService {

    boolean register(SignUpRequest request);

    /** @return UUID пользователя или null если неверные credentials */
    UUID authorize(String authorizationHeader);
}
