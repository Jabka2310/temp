package tictactoe.web.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tictactoe.domain.service.UserService;
import tictactoe.web.model.UserDto;

import java.util.UUID;

@RestController
@RequestMapping("/user")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{userId}")
    public ResponseEntity<?> getUser(@PathVariable UUID userId) {
        return userService.findLoginById(userId)
                .map(login -> ResponseEntity.ok(new UserDto(userId, login)))
                .orElse(ResponseEntity.notFound().build());
    }
}
// GET /user/{uuid} — посмотреть login по id (например, узнать ник соперника). Пароль не отдаём — только UserDto.