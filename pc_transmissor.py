import sounddevice as sd
import websocket
import time

SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 100
DEVICE_INDEX = 1

SERVER_URL = "ws://127.0.0.1:5000/audio"

def iniciar_transmissao():
    print(f"Tentando conectar ao servidor em {SERVER_URL}")

    ws = websocket.WebSocket()

    try:
        ws.connect(SERVER_URL)
        print("🟢 Conectado ao Servidor com sucesso!")
        print("Capturando áudio e enviando para a nuvem... (Pressione Ctrl+C para parar)")

        with sd.RawInputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                               dtype='int16', blocksize=CHUNK, device=DEVICE_INDEX) as stream_in:
            while True:
                data, _ = stream_in.read(CHUNK)

                ws.send_binary(bytes(data))

    except ConnectionRefusedError:
        print("Erro: O servidor (app.py) não está rodando ou recusou a conexão.")
    except Exception as e:
        print(f"A Conexão caiu ou houve um erro: {e}")
    finally:
        ws.close()
        print("Transmissão encerrada.")


if __name__ == "__main__":
    iniciar_transmissao()