const dealerHandEl = document.getElementById('dealer-hand');
const playerHandEl = document.getElementById('player-hand');
const dealerScoreEl = document.getElementById('dealer-score');
const playerScoreEl = document.getElementById('player-score');
const startBtn = document.getElementById('start-btn');
const hitBtn = document.getElementById('hit-btn');
const standBtn = document.getElementById('stand-btn');
const gameStatusEl = document.getElementById('game-status');
const difficultySelect = document.getElementById('difficulty-select');

// --- Funções de Renderização (front-end) ---
function renderHand(hand, element) {
    element.innerHTML = '';
    hand.forEach(cardStr => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        cardDiv.textContent = cardStr;
        element.appendChild(cardDiv);
    });
}

function updateUI(data) {
    renderHand(data.jogador, playerHandEl);
    playerScoreEl.textContent = data.pontos_jogador;
    
    if (data.dealer) {
        renderHand(data.dealer, dealerHandEl);
    }
    if (data.pontos_dealer) {
        dealerScoreEl.textContent = data.pontos_dealer;
    }
    
    if (data.resultado) {
        let mensagem = '';
        if (data.resultado === 'voce_venceu') mensagem = 'Você Venceu!';
        else if (data.resultado === 'voce_perdeu') mensagem = 'Você Perdeu!';
        else if (data.resultado === 'empate') mensagem = 'Empate.';
        gameStatusEl.textContent = mensagem;
        
        startBtn.disabled = false;
        hitBtn.disabled = true;
        standBtn.disabled = true;
        difficultySelect.disabled = false;
    } else if (data.status_jogo) {
        if (data.status_jogo === 'voce_estourou') {
            gameStatusEl.textContent = 'Você estourou! Fim de jogo.';
            startBtn.disabled = false;
            hitBtn.disabled = true;
            standBtn.disabled = true;
            difficultySelect.disabled = false;
        }
    }
}

// --- Funções que se comunicam com o Servidor Python ---
startBtn.addEventListener('click', () => {
    gameStatusEl.textContent = 'Jogo iniciado!';
    hitBtn.disabled = false;
    standBtn.disabled = false;
    startBtn.disabled = true;
    difficultySelect.disabled = true;
    
    fetch('/iniciar_jogo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dificuldade: difficultySelect.value })
    })
    .then(response => response.json())
    .then(data => updateUI(data));
});

hitBtn.addEventListener('click', () => {
    fetch('/comprar_carta', { method: 'POST' })
    .then(response => response.json())
    .then(data => updateUI(data));
});

standBtn.addEventListener('click', () => {
    fetch('/parar', { method: 'POST' })
    .then(response => response.json())
    .then(data => updateUI(data));
});