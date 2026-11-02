import subprocess, tempfile, queue, threading, os, sys
import sounddevice as sd, soundfile as sf

VOICE = "pt_BR-faber-medium"
PASTA = os.path.dirname(os.path.abspath(__file__))
fila = queue.Queue()

def _gerar_e_tocar(texto):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        caminho = f.name
    r = subprocess.run(
        [sys.executable, "-m", "piper", "-m", VOICE, "-f", caminho],
        input=texto.encode("utf-8"), capture_output=True, cwd=PASTA)
    if r.returncode != 0:
        print("Erro do Piper:", r.stderr.decode("utf-8", errors="ignore"))
        return
    dados, taxa = sf.read(caminho)
    sd.play(dados, taxa); sd.wait()
    os.remove(caminho)

def _worker():
    while True:
        texto = fila.get()
        if texto is None:
            break
        try:
            _gerar_e_tocar(texto)
        except Exception as e:
            print("Erro no TTS:", e)
        fila.task_done()

threading.Thread(target=_worker, daemon=True).start()

def falar(texto):
    fila.put(texto)

def esperar_fim():
    fila.join()