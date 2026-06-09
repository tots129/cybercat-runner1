import streamlit as st

# Configuração da página do Streamlit
st.set_page_config(
    page_title="CyberCat Runner - Streamlit", 
    page_icon="🐱", 
    layout="centered"
)

# Título e descrição na interface do Streamlit
st.title("🐱 CyberCat Runner no Streamlit")
st.write("Um jogo de corrida infinita estilo Cyberpunk feito para rodar direto no seu app Python!")

# Todo o código HTML, CSS e JavaScript do seu jogo + Sistema de Dicas Dinâmico
jogo_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #0d0e15;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #fff;
            overflow: hidden;
            padding-top: 10px;
        }
        #speed-control-panel {
            margin-bottom: 15px;
            background: #10111a;
            padding: 8px 15px;
            border-radius: 20px;
            border: 1px solid #00ffcc;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .speed-btn {
            background-color: #ff0055;
            color: white;
            border: none;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        #speed-val { font-weight: bold; color: #00ffcc; min-width: 30px; text-align: center; }
        #game-container {
            position: relative;
            width: 100%;
            max-width: 700px;
            height: 280px;
            background: linear-gradient(to bottom, #1a1c29, #10111a);
            border: 4px solid #ff0055;
            border-radius: 8px;
            box-shadow: 0 0 20px #ff0055;
            overflow: hidden;
        }
        #floor { position: absolute; bottom: 0; width: 100%; height: 20px; background-color: #ff0055; }
        #player {
            position: absolute;
            bottom: 20px;
            left: 50px;
            width: 40px;
            height: 40px;
            background-color: #00ffcc;
            border-radius: 8px;
            box-shadow: 0 0 15px #00ffcc;
        }
        #player::before, #player::after {
            content: ''; position: absolute; top: -8px; width: 0; height: 0;
            border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 8px solid #00ffcc;
        }
        #player::before { left: 4px; } #player::after { right: 4px; }
        #player.ducking { height: 20px; }
        .obstacle-ground { position: absolute; bottom: 20px; width: 30px; height: 40px; background-color: #ffff00; border-radius: 4px; }
        .obstacle-air { position: absolute; bottom: 65px; width: 40px; height: 15px; background-color: #ff00ff; border-radius: 4px; }
        #score-board { position: absolute; top: 15px; right: 20px; font-size: 20px; font-weight: bold; color: #00ffcc; }
        #game-over {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.85); flex-direction: column; align-items: center; justify-content: center;
        }
        #game-over h2 { color: #ff0055; font-size: 32px; margin-bottom: 15px; }
        button.main-btn {
            padding: 10px 20px; font-size: 16px; background-color: #00ffcc; color: #000;
            border: none; border-radius: 5px; cursor: pointer; font-weight: bold;
        }
        #instructions { margin-top: 15px; font-size: 13px; color: #888; text-align: center; }

        /* --- ESTILO DA NOVA CAIXA DE DICAS --- */
        #tips-container {
            margin-top: 20px;
            width: 100%;
            max-width: 700px;
            background-color: rgba(28, 133, 219, 0.1);
            border-left: 5px solid #1c85db;
            padding: 15px;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }
        #tip-text {
            font-size: 14px;
            color: #d1ecf1;
            line-height: 1.4;
        }
        #next-tip-btn {
            background-color: #1c85db;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
            transition: 0.2s;
        }
        #next-tip-btn:hover {
            background-color: #299bf5;
        }
    </style>
</head>
<body>
    <div id="speed-control-panel">
        <span>Velocidade Atual:</span>
        <button class="speed-btn" onclick="adjustSpeed(-0.5)">-</button>
        <span id="speed-val">4.5</span>
        <button class="speed-btn" onclick="adjustSpeed(0.5)">+</button>
    </div>
    <div id="game-container">
        <div id="score-board">SCORE: <span id="score">0</span></div>
        <div id="player"></div>
        <div id="floor"></div>
        <div id="game-over">
            <h2>SISTEMA CORROMPIDO</h2>
            <p style="margin-bottom: 20px;">Sua pontuação final: <span id="final-score">0</span></p>
            <button class="main-btn" onclick="resetGame()">REINICIAR</button>
        </div>
    </div>
    <div id="instructions">
        Pressione <strong>Seta para Cima (↑)</strong> ou <strong>Espaço</strong> para Pular.<br>
        Pressione <strong>Seta para Baixo (↓)</strong> para Agachar.
    </div>

    <div id="tips-container">
        <div id="tip-text">💡 Carregando dicas...</div>
        <button id="next-tip-btn" onclick="showNextTip()">Próxima Dica ➔</button>
    </div>

    <script>
        const player = document.getElementById('player');
        const gameContainer = document.getElementById('game-container');
        const scoreDisplay = document.getElementById('score');
        const finalScoreDisplay = document.getElementById('final-score');
        const gameOverScreen = document.getElementById('game-over');
        const speedValDisplay = document.getElementById('speed-val');
        const tipTextDisplay = document.getElementById('tip-text');

        let gravity = 0.35; let jumpForce = 11.5;     
        let initialSpeed = 4.5; let gameSpeed = initialSpeed; 
        let isJumping = false; let isDucking = false;
        let position = 20; let velocity = 0; let score = 0;
        let isGameOver = false; let obstacles = []; let spawnTimer = 0;

        // BANCO DE DICAS EM JAVASCRIPT
        const listaDeDicas = [
            "Dica: Clique dentro da caixa do jogo antes de jogar para que o teclado responda aos comandos!",
            "Dica: Os lasers rosa vêm pelo alto! Mantenha a Seta para Baixo (↓) pressionada para passar deslizando.",
            "Dica: Os drones amarelos são terrestres. Use Espaço ou Seta para Cima (↑) para saltar sobre eles.",
            "Dica: Quer treinar os seus reflexos? Use o botão '+' e comece a partida direto na velocidade 8.0!",
            "Dica: O jogo acelera automaticamente a cada 600 pontos. Fique esperto!",
            "Dica: O pulo do CyberCat possui baixa gravidade. Use o tempo no ar para planejar o seu próximo movimento.",
            "Dica: Se o jogo travar ou não responder, clique em qualquer área preta dentro do retângulo rosa.",
            "Dica: Sabia que esse jogo foi feito utilizando comunicação híbrida entre HTML e Streamlit? 🐱"
        ];

        let currentTipIndex = 0;

        function sortearDica() {
            let novoIndex;
            // Evita repetir a mesma dica duas vezes seguidas no sorteio
            do {
                novoIndex = Math
