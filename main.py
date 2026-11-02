import time
print("Carregando módulos...", flush=True)
from stt import gravar, transcrever
from tts import falar, esperar_fim
from tools import rotear
from brain import pensar
print("Módulos carregados.", flush=True)

print("Jarvis pronto. Segure F9 para falar.", flush=True)
falar("Jarvis online.")

while True:
    print("\n[1] Aguardando F9...", flush=True)
    audio = gravar("f9")
    if audio is None or len(audio) < 8000:
        print("[!] Gravação muito curta, ignorada.", flush=True)
        continue
    print(f"[2] Gravado: {len(audio)/16000:.1f}s de áudio. Transcrevendo...", flush=True)

    t0 = time.time()
    texto = transcrever(audio)
    print(f"[3] Transcrição ({time.time()-t0:.1f}s): {texto!r}", flush=True)
    if not texto:
        continue

    resposta_direta = rotear(texto)
    if resposta_direta:
        print(f"[4] Roteador respondeu: {resposta_direta}", flush=True)
        falar(resposta_direta)
    else:
        print("[4] Enviando ao LLM...", flush=True)
        falar("Um momento.")
        t0 = time.time()
        pensar(texto)
        print(f"[5] LLM terminou ({time.time()-t0:.1f}s)", flush=True)

    print("[6] Aguardando o áudio terminar...", flush=True)
    esperar_fim()
    print("[7] Pronto.", flush=True)