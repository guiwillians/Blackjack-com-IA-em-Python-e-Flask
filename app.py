from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# --- Lógica do Jogo (A mesma que você já tem) ---
def criar_baralho():
    suits = ['♥', '♦', '♣', '♠']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    baralho = [{'valor': valor, 'naipe': naipe} for naipe in suits for valor in values]
    return baralho

def embaralhar(baralho):
    random.shuffle(baralho)

def calcular_pontos(mao):
    pontos = 0
    ases = 0
    for carta in mao:
        if carta['valor'] in ['J', 'Q', 'K']:
            pontos += 10
        elif carta['valor'] == 'A':
            pontos += 11
            ases += 1
        else:
            pontos += int(carta['valor'])
    
    while pontos > 21 and ases > 0:
        pontos -= 10
        ases -= 1
    
    return pontos

def vez_do_dealer_com_ia(mao_dealer, baralho, dificuldade, mao_jogador):
    pontos_dealer = calcular_pontos(mao_dealer)
    pontos_jogador = calcular_pontos(mao_jogador)
    
    if dificuldade == 'facil':
        while pontos_dealer < 15:
            mao_dealer.append(baralho.pop())
            pontos_dealer = calcular_pontos(mao_dealer)
    elif dificuldade == 'medio':
        while pontos_dealer < 17:
            mao_dealer.append(baralho.pop())
            pontos_dealer = calcular_pontos(mao_dealer)
    elif dificuldade == 'dificil':
        if mao_jogador:
            valor_carta_visivel = calcular_pontos([mao_jogador[0]])
        else:
            valor_carta_visivel = 0
        while pontos_dealer < 17:
            if pontos_dealer > 11 and valor_carta_visivel > 6:
                break
            mao_dealer.append(baralho.pop())
            pontos_dealer = calcular_pontos(mao_dealer)
    elif dificuldade == 'impossivel':
        while pontos_dealer < pontos_jogador and pontos_dealer <= 21:
            mao_dealer.append(baralho.pop())
            pontos_dealer = calcular_pontos(mao_dealer)

# --- Rotas da API ---
# A rota principal que serve o HTML
@app.route('/')
def home():
    return render_template('index.html')

# A rota para iniciar um novo jogo
@app.route('/iniciar_jogo', methods=['POST'])
def iniciar_jogo():
    data = request.get_json()
    dificuldade = data['dificuldade']
    
    global baralho_global, mao_jogador_global, mao_dealer_global, dificuldade_global
    
    baralho_global = criar_baralho()
    embaralhar(baralho_global)
    mao_jogador_global = [baralho_global.pop(), baralho_global.pop()]
    mao_dealer_global = [baralho_global.pop(), baralho_global.pop()]
    dificuldade_global = dificuldade
    
    return jsonify({
        'jogador': [f"{c['valor']}{c['naipe']}" for c in mao_jogador_global],
        'dealer': [f"{mao_dealer_global[0]['valor']}{mao_dealer_global[0]['naipe']}", '??'],
        'pontos_jogador': calcular_pontos(mao_jogador_global),
        'pontos_dealer': '??'
    })

# A rota para o jogador comprar uma carta
@app.route('/comprar_carta', methods=['POST'])
def comprar_carta():
    mao_jogador_global.append(baralho_global.pop())
    pontos = calcular_pontos(mao_jogador_global)
    
    return jsonify({
        'jogador': [f"{c['valor']}{c['naipe']}" for c in mao_jogador_global],
        'pontos_jogador': pontos,
        'status_jogo': 'jogando' if pontos <= 21 else 'voce_estourou'
    })

# A rota para o jogador parar e a IA jogar
@app.route('/parar', methods=['POST'])
def parar():
    vez_do_dealer_com_ia(mao_dealer_global, baralho_global, dificuldade_global, mao_jogador_global)
    
    pontos_jogador = calcular_pontos(mao_jogador_global)
    pontos_dealer = calcular_pontos(mao_dealer_global)
    
    resultado = "empate"
    if pontos_jogador > 21:
        resultado = "voce_perdeu"
    elif pontos_dealer > 21:
        resultado = "voce_venceu"
    elif pontos_jogador > pontos_dealer:
        resultado = "voce_venceu"
    elif pontos_jogador < pontos_dealer:
        resultado = "voce_perdeu"
    
    return jsonify({
        'jogador': [f"{c['valor']}{c['naipe']}" for c in mao_jogador_global],
        'dealer': [f"{c['valor']}{c['naipe']}" for c in mao_dealer_global],
        'pontos_jogador': pontos_jogador,
        'pontos_dealer': pontos_dealer,
        'resultado': resultado
    })

if __name__ == '__main__':
    baralho_global = []
    mao_jogador_global = []
    mao_dealer_global = []
    dificuldade_global = ''
    app.run(debug=True)