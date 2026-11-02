import numpy as np
import sounddevice as sd
import keyboard
from faster_whisper import WhisperModel

TAXA = 16000

# Inicialização do modelo
modelo = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)

def gravar(tecla="f9"):
    print(f"Pressione e SEGURE '{tecla.upper()}' para falar...")
    
    # 1. Espera a tecla ser pressionada fisicamente
    while not keyboard.is_pressed(tecla):
        sd.sleep(10)

    print("Gravando...")
    partes = []

    # 2. Abre a gravação e mantém enquanto a tecla continuar pressionada
    with sd.InputStream(samplerate=TAXA, channels=1, dtype="float32",
                        callback=lambda d, *_: partes.append(d.copy())):
        while keyboard.is_pressed(tecla):
            sd.sleep(20)

    print("Gravação finalizada. Transcrevendo...")
    return np.concatenate(partes).flatten() if partes else None

def transcrever(audio):
    if audio is None or len(audio) == 0:
        return ""
    
    segmentos, _ = modelo.transcribe(
        audio, 
        language="pt", 
        beam_size=1, 
        vad_filter=True
    )
    return " ".join(s.text for s in segmentos).strip()

# Exemplo de loop de execução:
if __name__ == "__main__":
    while True:
        audio_capturado = gravar(tecla="f9")
        texto = transcrever(audio_capturado)
        if texto:
            print(f"Resultado: {texto}\n")