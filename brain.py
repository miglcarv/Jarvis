#Passo 6 (cerebro com Ollama)

import re, ollama
from tools import FERRAMENTAS, DISPONIVEIS
from tts import falar

MODELO = "llama3.2:3b"
SISTEMA = ("Você é o Jarvis, assistente de voz em português do Brasil. "
           "Responda em no máximo 2 frases curtas, sem listas nem markdown.")
historico = [{"role": "system", "content": SISTEMA}]

OPCOES = {"num_ctx": 2048, "num_predict": 150, "temperature": 0.4}

def _chamar():
    return ollama.chat(model=MODELO, messages=historico, tools=FERRAMENTAS,
                       stream=True, options=OPCOES, keep_alive="30m",
                       think=False)   # desliga o raciocínio (economiza tokens)

def pensar(texto_usuario):
    historico.append({"role": "user", "content": texto_usuario})
    for _ in range(2):                          # no máx. 1 rodada de ferramenta
        buffer, resposta, chamadas = "", "", []
        for pedaco in _chamar():
            msg = pedaco["message"]
            if msg.get("tool_calls"):
                chamadas += msg["tool_calls"]
            if msg.get("content"):
                buffer += msg["content"]; resposta += msg["content"]
                # fala assim que fecha uma frase
                while (m := re.search(r"[.!?\n]", buffer)):
                    frase, buffer = buffer[:m.end()], buffer[m.end():]
                    if frase.strip(): falar(frase.strip())
        if buffer.strip(): falar(buffer.strip())

        historico.append({"role": "assistant", "content": resposta,
                          "tool_calls": chamadas or None})
        if not chamadas: break
        for c in chamadas:
            f = c["function"]
            resultado = DISPONIVEIS[f["name"]](**f["arguments"])
            historico.append({"role": "tool", "content": str(resultado)})

    del historico[1:-6]   # mantém só as últimas mensagens (contexto pequeno = rápido)