package tictactoe; // корневой пакет — spring ищет классы начиная отсюда

import org.springframework.boot.SpringApplication; // класс который реально запускает spring boot
import org.springframework.boot.autoconfigure.SpringBootApplication; // главная аннотация приложения
import org.springframework.web.bind.annotation.GetMapping; // чтобы повесить обработчик на GET-запрос
import org.springframework.web.bind.annotation.RestController; // класс который отдаёт json/текст в ответ на http

@SpringBootApplication // говорит spring: это наше приложение, подтяни tomcat, json и т.д.
public class TicTacToeApplication {

    public static void main(String[] args) { // стандартная точка входа в java
        SpringApplication.run(TicTacToeApplication.class, args); // поднимает сервер на 8080
    }
}
