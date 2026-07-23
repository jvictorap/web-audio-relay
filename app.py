from flask import Flask, render_template # type: ignore
from flask_sock import Sock # type: ignore

app = Flask(__name__)
sock = Sock(app)

clientes_conectados = set()
total_acessos = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    global total_acessos
    total_acessos +=1
    return render_template('admin.html')

@sock.route('/audio')
def audio_relay(ws):
    clientes_conectados.add(ws)
    print(f"Novo dispositivo conectado! Total na sala: {len(clientes_conectados)}")

    try:
        while True:
            data = ws.receive()
            if data:
                for cliente in clientes_conectados.copy():
                    if cliente != ws:
                        try:
                            cliente.send(data)
                        except Exception:
                            clientes_conectados.remove(cliente)

    except:
        pass
    finally:
        if ws in clientes_conectados:
            clientes_conectados.remove(ws)
        print(f"Dispositivo saiu. Total na sala: {len(clientes_conectados)}")


if __name__ == '__main__':

    print("--------------------------------------------------")
    print("🌐 SERVIDOR RELAY INICIADO")
    print("Acesse http://127.0.0.1:5000 no navegador do PC")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000)