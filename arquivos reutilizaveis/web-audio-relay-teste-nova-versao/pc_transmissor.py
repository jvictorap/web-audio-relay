import sounddevice as sd
import websocket
import time
import random

SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 1024
DEVICE_INDEX = 1

# 1. Geração de um PIN para a sala
PIN = str(random.randint(1000, 9999))

# 2. Uso do protocolo ws:// e da rota correta (exemplo)
SERVER_URL = f"ws://192.168.0.10:5000/audio/{PIN}"

def iniciar_transmissao():
    print(f"Tentando conectar ao servidor em {SERVER_URL}")
    print(f"Seu PIN de acesso é: {PIN}")

    ws = websocket.WebSocket()

    try:
        ws.connect(SERVER_URL)
        print("🟢 Conectado ao Servidor com sucesso!")
        print("Capturando áudio e enviando para a nuvem... (Pressione Ctrl+C para parar)")

        with sd.RawInputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                               dtype='int16', blocksize=CHUNK, device=DEVICE_INDEX) as stream_in:
            while True:
                data, _ = stream_in.read(CHUNK)
                # O servidor precisaria de uma lógica específica para decodificar esse PCM
                ws.send_binary(bytes(data))

    except ConnectionRefusedError:
        print("Erro: O servidor Flask não está rodando ou recusou a conexão.")
    except Exception as e:
        print(f"A Conexão caiu ou houve um erro: {e}")
    finally:
        ws.close()
        print("Transmissão encerrada.")

if __name__ == "__main__":
    iniciar_transmissao()