package tictactoe.web.model;

import java.util.UUID;

public class UserDto {

    private UUID id;
    private String login;

    public UserDto() {
    }

    public UserDto(UUID id, String login) {
        this.id = id;
        this.login = login;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }
}

