from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

# Arquivo de pedidos
ARQUIVO_PEDIDOS = "pedidos.json"

# Data do evento
DATA_EVENTO = "01/01/2000"  # qualquer data anterior a hoje

# Cardápio
CARDAPIO = {
    "Caipirinha / Caipiroska": {"pre_venda": 8.0, "dia_evento": 10.0},
    "Roska de Morango": {"pre_venda": 12.0, "dia_evento": 15.0},
    "Roska de Abacaxi": {"pre_venda": 8.0, "dia_evento": 10.0},
    "Roska de Limão": {"pre_venda": 8.0, "dia_evento": 10.0},
    "Roska de Uva": {"pre_venda": 8.0, "dia_evento": 10.0},
    "Roska de Maracujá": {"pre_venda": 8.0, "dia_evento": 10.0},
    "Roska Mix Premium": {"pre_venda": 18.0, "dia_evento": 22.0},
    "Gin Tônica / Gin Tropical": {"pre_venda": 17.0, "dia_evento": 20.0},
    "Aperol Spritz": {"pre_venda": 22.0, "dia_evento": 25.0},
}

# Funções para pedidos
def carregar_pedidos():
    try:
        with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def persistir_pedidos(pedidos):
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

def preco_unitario(nome_item):
    hoje = datetime.now().strftime("%d/%m/%Y")
    if nome_item in CARDAPIO:
        return CARDAPIO[nome_item]["pre_venda"] if hoje < DATA_EVENTO else CARDAPIO[nome_item]["dia_evento"]
    return 0.0

# Carrega pedidos existentes
pedidos = carregar_pedidos()

# Rotas
@app.route("/")
def index():
    return render_template("index.html", cardapio=CARDAPIO)

@app.route("/pedido", methods=["POST"])
def novo_pedido():
    nome = request.form.get("nome")
    item = request.form.get("item")
    quantidade = int(request.form.get("quantidade", 1))
    preco = preco_unitario(item)
    total = preco * quantidade

    pedido = {
        "id": str(int(datetime.now().timestamp()*1000))[-6:],
        "cliente": nome,
        "drink": item,
        "quantidade": quantidade,
        "total_price": total,
        "status": "pendente",
        "timestamp": datetime.now().isoformat()
    }

    pedidos.append(pedido)
    persistir_pedidos(pedidos)
    return redirect(url_for("meus_pedidos", cliente=nome))

@app.route("/pedidos/<cliente>")
def meus_pedidos(cliente):
    user_pedidos = [p for p in pedidos if p["cliente"] == cliente]
    return render_template("pedidos.html", pedidos=user_pedidos, cliente=cliente)

@app.route("/admin")
def admin():
    return render_template("admin.html", pedidos=pedidos)

# Inicialização do app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
