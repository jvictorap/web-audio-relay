from flask import Flask, render_template, send_from_directory # type: ignore
from flask_sock import Sock # type: ignore

app = Flask(__name__)
sock = Sock(app)

clientes_conectados = set()
total_acessos = 0

salas = {}

@app.route('/ads.txt')
def serve_ads_txt():
    return send_from_directory(app.root_path, 'ads.txt')

@app.route('/')
def index():
    return render_template('index.html')

# --- Novas Rotas Mapeadas da Interface Principal ---

@app.route('/como-funciona')
def como_funciona():
    return render_template('pc_sem_audio.html', titulo="Landell Áudio-PC")

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/transmitir')
def transmitir():
    # Página principal de roteamento onde rodará o script de captura via navegador
    return render_template('transmitir.html')

@app.route('/receber')
def receber():
    return render_template('receber.html')

# ---------------------------------------------------

@app.route('/admin')
def admin():
    global total_acessos
    total_acessos += 1
    return render_template('admin.html')

@sock.route('/audio/<pin>')
def audio_relay(ws, pin):
    if pin not in salas:
        salas[pin] = []

    salas[pin].append(ws)

    try:
        while True:
            data = ws.receive()
            if data:
                # Envia apenas para quem está na mesma sala (PIN)
                for cliente in salas[pin]:
                    if cliente != ws:
                        try:
                            cliente.send(data)
                        except:
                            pass
    except Exception as e:
        print(f"Desconectado da sala {pin}")
    finally:
        # Remoção segura e limpeza do dicionário
        if ws in salas.get(pin, []):
            salas[pin].remove(ws)
            
        if pin in salas and not salas[pin]:
            del salas[pin]

@app.route('/privacidade')
def privacidade():
    return render_template('privacidade.html')

@app.route('/termos-de-uso')
def termos():
    return render_template('termos.html')

@app.route('/solucoes/pc-sem-audio')
def pc_sem_audio():
    # Corrigido para "Landell" mantendo a consistência da marca
    return render_template('pc_sem_audio.html', titulo="Landell Áudio-PC")

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🌐 SERVIDOR LANDELL ÁUDIO-PC INICIADO")
    print("Acesse http://127.0.0.1:5000 no navegador do PC")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000)
