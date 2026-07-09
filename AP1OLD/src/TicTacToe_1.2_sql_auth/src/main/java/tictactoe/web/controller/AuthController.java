package tictactoe.web.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.service.AuthService;
import tictactoe.web.model.ErrorResponse;
import tictactoe.web.model.SignUpRequest;

import java.util.UUID;

@RestController
@RequestMapping("/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody SignUpRequest request) {
        boolean success = authService.register(request);
        if (success) return ResponseEntity.ok().build();
        return ResponseEntity.badRequest()
                .body(new ErrorResponse("Registration failed: login may already exist"));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestHeader(value = "Authorization", required = false) String authHeader) {
        UUID userId = authService.authorize(authHeader);
        if (userId == null) return ResponseEntity.status(401)
                .body(new ErrorResponse("Unauthorized"));
        return ResponseEntity.ok(userId);
    }

}

