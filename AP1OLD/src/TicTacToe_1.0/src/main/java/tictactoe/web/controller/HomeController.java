package tictactoe.web.controller;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Обработчик корневого пути — при заходе на http://localhost:8080/
 */
@RestController
public class HomeController {

    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String home() {
        return """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Крестики-нолики</title>
            <style>
            * { box-sizing: border-box; }
            body {
              font-family: 'Segoe UI', system-ui, sans-serif;
              background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
              color: #e8e8e8;
              min-height: 100vh; margin: 0; padding: 2rem 1rem;
              text-align: center;
            }
            .wrap { max-width: 360px; margin: 0 auto; }
            h1 {
              font-size: 1.75rem; font-weight: 600; margin: 0 0 0.25rem 0;
              background: linear-gradient(90deg, #00d9ff, #00ff88);
              -webkit-background-clip: text; -webkit-text-fill-color: transparent;
              background-clip: text;
            }
            .sub { color: #8892a0; font-size: 0.9rem; margin-bottom: 0.75rem; }
            .side, .difficulty {
              display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;
              margin-bottom: 1rem;
            }
            .side label, .difficulty label {
              display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.25rem;
            }
              display: flex; align-items: center; gap: 0.35rem;
              cursor: pointer; font-size: 0.85rem; color: #a0aec0;
            }
            .side input, .difficulty input { accent-color: #00d9ff; }
            .side input:checked + span, .difficulty input:checked + span { color: #00d9ff; font-weight: 600; }
            .msg {
              min-height: 1.5rem; font-size: 0.95rem; margin-bottom: 1rem;
              color: #00d9ff; font-weight: 500;
            }
            .msg.err { color: #ff6b6b; }
            .msg.win { color: #00ff88; }
            .board {
              display: grid; grid-template-columns: repeat(3, 1fr);
              gap: 6px; width: 198px; margin: 0 auto 1.5rem;
              background: rgba(0,0,0,0.2); padding: 10px; border-radius: 12px;
              box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
            }
            .cell {
              width: 56px; height: 56px; border: 2px solid #2d3748;
              font-size: 28px; font-weight: 700;
              display: flex; align-items: center; justify-content: center;
              cursor: pointer; background: #1a1f2e;
              border-radius: 8px; transition: all 0.2s ease;
            }
            .cell:hover { background: #252b3b; border-color: #00d9ff; box-shadow: 0 0 12px rgba(0,217,255,0.2); }
            .cell.x { color: #00d9ff; cursor: default; border-color: #00d9ff40; animation: pop 0.25s ease; }
            .cell.o { color: #ff6b9d; cursor: default; border-color: #ff6b9d40; animation: pop 0.25s ease; }
            .cell.win { background: rgba(0,255,136,0.15); border-color: #00ff88; box-shadow: 0 0 16px rgba(0,255,136,0.3); }
            @keyframes pop { 0% { transform: scale(0.6); opacity: 0; } 70% { transform: scale(1.05); } 100% { transform: scale(1); opacity: 1; } }
            .btn {
              padding: 0.6rem 1.25rem; font-size: 1rem; cursor: pointer;
              background: linear-gradient(135deg, #00d9ff, #0099cc);
              color: #0f0f1a; border: none; border-radius: 8px;
              font-weight: 600; transition: transform 0.15s, box-shadow 0.15s;
            }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,217,255,0.4); }
            .btn:active { transform: translateY(0); }
            .stats {
              margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #2d3748;
              font-size: 0.85rem; color: #8892a0;
            }
            .stats span { color: #00ff88; font-weight: 600; }
            </style>
            </head>
            <body>
            <div class="wrap">
            <h1>Крестики-нолики</h1>
            <p class="sub" id="sub">Ты — X, компьютер — O</p>
            <div class="side">
              <label><input type="radio" name="side" value="x" checked><span>Играть за X</span></label>
              <label><input type="radio" name="side" value="o"><span>Играть за O</span></label>
            </div>
            <div class="difficulty">
              <label><input type="radio" name="diff" value="easy" checked><span>Лёгкая</span></label>
              <label><input type="radio" name="diff" value="medium"><span>Средняя</span></label>
              <label><input type="radio" name="diff" value="hard"><span>Сложная</span></label>
            </div>
            <div class="msg" id="msg"></div>
            <div class="board" id="board"></div>
            <button class="btn" id="newGame">Новая игра</button>
            <div class="stats" id="stats">Побед: <span id="wins">0</span> из <span id="total">0</span> игр</div>
            </div>
            <script>
            let gameId = null;
            let board = [[0,0,0],[0,0,0],[0,0,0]];
            let gameOver = false;
            let wins = 0, total = 0;
            const boardEl = document.getElementById('board');
            const msgEl = document.getElementById('msg');
            function difficulty() { return document.querySelector('input[name="diff"]:checked').value; }
            function playAsO() { return document.querySelector('input[name="side"]:checked').value === 'o'; }
            function updateSub() {
              document.getElementById('sub').textContent = playAsO() ? 'Ты — O, компьютер — X' : 'Ты — X, компьютер — O';
            }
            document.querySelectorAll('input[name="side"]').forEach(el => el.addEventListener('change', updateSub));
            function showMsg(t, type) {
              msgEl.textContent = t || '';
              msgEl.classList.remove('err', 'win');
              if (type === 'err') msgEl.classList.add('err');
              if (type === 'win') msgEl.classList.add('win');
            }
            function updateStats(winner) {
              total++;
              if (winner === 1) wins++;
              document.getElementById('wins').textContent = wins;
              document.getElementById('total').textContent = total;
            }
            function render() {
              boardEl.innerHTML = '';
              const winLine = getWinLine();
              const isWin = (r, c) => winLine.some(([a,b]) => a===r && b===c);
              for (let i = 0; i < 3; i++) {
                for (let j = 0; j < 3; j++) {
                  const c = document.createElement('div');
                  c.className = 'cell';
                  const v = board[i][j];
                  const asO = playAsO();
                  if (v === 1) { c.textContent = asO ? 'O' : 'X'; c.classList.add(asO ? 'o' : 'x'); }
                  else if (v === 2) { c.textContent = asO ? 'X' : 'O'; c.classList.add(asO ? 'x' : 'o'); }
                  if (isWin(i, j)) c.classList.add('win');
                  if (v !== 0 || gameOver) c.style.cursor = 'default';
                  else c.onclick = () => move(i, j);
                  boardEl.appendChild(c);
                }
              }
            }
            function checkWinner() {
              const b = board;
              for (let i = 0; i < 3; i++) {
                if (b[i][0] && b[i][0]===b[i][1]&&b[i][1]===b[i][2]) return b[i][0];
                if (b[0][i] && b[0][i]===b[1][i]&&b[1][i]===b[2][i]) return b[0][i];
              }
              if (b[0][0]&&b[0][0]===b[1][1]&&b[1][1]===b[2][2]) return b[0][0];
              if (b[0][2]&&b[0][2]===b[1][1]&&b[1][1]===b[2][0]) return b[0][2];
              if (b.flat().every(x=>x!==0)) return 'draw';
              return null;
            }
            function getWinLine() {
              const b = board;
              for (let i = 0; i < 3; i++) {
                if (b[i][0]&&b[i][0]===b[i][1]&&b[i][1]===b[i][2]) return [[i,0],[i,1],[i,2]];
                if (b[0][i]&&b[0][i]===b[1][i]&&b[1][i]===b[2][i]) return [[0,i],[1,i],[2,i]];
              }
              if (b[0][0]&&b[0][0]===b[1][1]&&b[1][1]===b[2][2]) return [[0,0],[1,1],[2,2]];
              if (b[0][2]&&b[0][2]===b[1][1]&&b[1][1]===b[2][0]) return [[0,2],[1,1],[2,0]];
              return [];
            }
            function getEmptyCells() {
              const out = [];
              for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) if (board[i][j] === 0) out.push([i,j]);
              return out;
            }
            function computerMoveEasy() {
              const empty = getEmptyCells();
              if (empty.length === 0) return;
              const [r, c] = empty[Math.floor(Math.random() * empty.length)];
              board[r][c] = 2;
            }
            async function move(row, col) {
              if (board[row][col] !== 0 || gameOver) return;
              if (!gameId) gameId = crypto.randomUUID();
              board[row][col] = 1;
              render();
              const diff = difficulty();
              if (diff === 'easy') {
                showMsg('Ход компьютера...');
                await new Promise(r => setTimeout(r, 400));
                computerMoveEasy();
                gameOver = checkWinner();
                if (gameOver === 1) { showMsg('Ты победил!', 'win'); updateStats(1); }
                else if (gameOver === 2) { showMsg('Победил компьютер!', 'err'); updateStats(2); }
                else if (gameOver === 'draw') { showMsg('Ничья!'); updateStats(0); }
                else showMsg('');
                render();
                return;
              }
              showMsg('Ход компьютера...');
              const delay = diff === 'medium' ? 600 : 200;
              await new Promise(r => setTimeout(r, delay));
              try {
                const r = await fetch('/game/' + gameId, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ id: gameId, board: { board: board }, computerStarts: false })
                });
                const data = await r.json().catch(() => ({}));
                if (!r.ok) { showMsg(data.error || 'Ошибка ' + r.status, 'err'); board[row][col]=0; render(); return; }
                board = data.board.board;
                gameOver = checkWinner();
                if (gameOver === 1) { showMsg('Ты победил!', 'win'); updateStats(1); }
                else if (gameOver === 2) { showMsg('Победил компьютер!', 'err'); updateStats(2); }
                else if (gameOver === 'draw') { showMsg('Ничья!'); updateStats(0); }
                else showMsg('');
                render();
              } catch (e) { showMsg('Ошибка сети: ' + e.message, 'err'); board[row][col]=0; render(); }
            }
            document.getElementById('newGame').onclick = async () => {
              gameId = crypto.randomUUID();
              gameOver = false;
              showMsg('');
              if (playAsO()) {
                if (difficulty() === 'easy') {
                  board = [[0,0,0],[0,0,0],[0,0,0]];
                  board[1][1] = 2;
                  render();
                } else {
                  board = [[0,0,0],[0,0,0],[0,0,0]];
                  render();
                  showMsg('Ход компьютера...');
                  await new Promise(r => setTimeout(r, difficulty() === 'medium' ? 600 : 200));
                  const r = await fetch('/game/' + gameId, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: gameId, board: { board: board }, computerStarts: true })
                  });
                  const data = await r.json().catch(() => ({}));
                  if (r.ok && data.board) board = data.board.board;
                  else showMsg(data.error || 'Ошибка', 'err');
                  showMsg('');
                  render();
                }
              } else {
                board = [[0,0,0],[0,0,0],[0,0,0]];
                render();
              }
            };
            render();
            updateSub();
            </script>
            </body>
            </html>
            """;
    }
}
