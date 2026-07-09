package tictactoe.datasource.service;

import org.springframework.stereotype.Service;
import tictactoe.domain.service.AuthService;
import tictactoe.domain.service.UserService;
import tictactoe.web.model.SignUpRequest;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.UUID;

@Service
public class AuthServiceImpl implements AuthService {
    private final UserService userService;

    public AuthServiceImpl(UserService userService) {
        this.userService = userService;
    }

    @Override
    public boolean register(SignUpRequest request) {
        if (request == null) return false;
        return userService.register(request.getLogin(), request.getPassword());
    }

    @Override
    public UUID authorize(String authorizationHeader) {
        String[] credentials = parseBasicAuth(authorizationHeader);
        if (credentials == null) {
            return null;
        }
        return userService.authenticate(credentials[0], credentials[1]).orElse(null);
    }

    private String[] parseBasicAuth(String header) {
        if (header == null || !header.startsWith("Basic ")) {
            return null;
        }
        try {
            String base64 = header.substring(6).trim();
            String decoded = new String(Base64.getDecoder().decode(base64), StandardCharsets.UTF_8);
            int colonIndex = decoded.indexOf(':');
            if (colonIndex < 0) {
                return null;
            }
            String login = decoded.substring(0, colonIndex);
            String password = decoded.substring(colonIndex + 1);
            return new String[]{login, password};
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}


//parseBasicAuth — сердце Basic Auth. Берёт заголовок, отрезает "Basic ", декодирует Base64,
// режет по первому :. Если что-то не так — null, фильтр вернёт 401.