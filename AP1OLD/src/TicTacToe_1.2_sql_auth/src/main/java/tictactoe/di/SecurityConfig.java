package tictactoe.di;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import tictactoe.domain.service.AuthService;
import tictactoe.web.filter.AuthFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public AuthFilter authFilter(AuthService authService) {
        return new AuthFilter(authService);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http, AuthFilter authFilter) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/auth/register", "/auth/login").permitAll()
                        .requestMatchers(
                                "/",
                                "/index.html",
                                "/game.html",
                                "/css/**",
                                "/js/**"
                        ).permitAll()
                        .anyRequest().permitAll()
                )
                .addFilterBefore(authFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
//csrf.disable() — REST API без форм, CSRF не нужен
//permitAll для /auth/register, /auth/login — без Authorization
//anyRequest().permitAll() — Spring Security не дублирует проверку; 401/403 даёт AuthFilter
//addFilterBefore — наш фильтр в цепочке Spring Security
//Spring Security по умолчанию блокирует всё. Мы открываем только register/login, остальное — через наш AuthFilter.
// csrf.disable() — для REST без браузерных форм.

//permitAll — без заголовка Authorization
//game/** API не в списке — ходы по-прежнему только с Basic Auth
//Статику открываем, API — защищаем