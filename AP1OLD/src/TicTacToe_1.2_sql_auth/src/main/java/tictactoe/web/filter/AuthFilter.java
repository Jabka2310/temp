package tictactoe.web.filter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.filter.GenericFilterBean;
import tictactoe.domain.service.AuthService;

import java.io.IOException;
import java.util.UUID;

public class AuthFilter extends GenericFilterBean {
    public static final String CURRENT_USER_ID_ATTR = "currentUserId";

    private final AuthService authService;

    public AuthFilter(AuthService authService) {
        this.authService = authService;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String path = httpRequest.getRequestURI();
        if (isPublicPath(path)) {
            chain.doFilter(request, response);
            return;
        }

        String authHeader = httpRequest.getHeader("Authorization");
        UUID userId = authService.authorize(authHeader);

        if (userId == null) {
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return; // НЕ вызываем chain.doFilter — запрос не доходит до контроллера
        }

        httpRequest.setAttribute(CURRENT_USER_ID_ATTR, userId);
        chain.doFilter(request, response);
    }

    private static boolean isPublicPath(String path) {
        if ("/auth/register".equals(path) || "/auth/login".equals(path)) {
            return true;
        }
        if ("/".equals(path) || "/index.html".equals(path) || "/game.html".equals(path)) {
            return true;
        }
        return path.startsWith("/css/") || path.startsWith("/js/")
                || path.endsWith(".txt"); // test.txt при проверке шага 6.1
    }
}

//фильтр стоит до контроллера. Нет auth → 401, запрос не доходит до GameController.
// Есть auth → кладём userId в request attribute — в PvP (Задание 3) оттуда узнаем «кто ходит».
