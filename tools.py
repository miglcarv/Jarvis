import os, re, subprocess, datetime, webbrowser

def que_horas():
    return datetime.datetime.now().strftime("São %H:%M")

def abrir_programa(nome: str):
    apps = {"chrome": "chrome", "bloco de notas": "notepad", "calculadora": "calc"}
    exe = apps.get(nome.lower())
    if not exe: return f"Não conheço o programa {nome}"
    subprocess.Popen(exe, shell=True)
    return f"Abrindo {nome}"

def pesquisar_web(consulta: str):
    webbrowser.open(f"https://www.google.com/search?q={consulta}")
    return f"Pesquisando {consulta}"

# 1) Roteador: comandos previsíveis NÃO passam pelo LLM (latência ~0)
ROTAS = [
    (r"que horas", lambda m: que_horas()),
    (r"abr[ae] (?:o |a )?(.+)", lambda m: abrir_programa(m.group(1))),
    (r"pesquis[ae] (?:por )?(.+)", lambda m: pesquisar_web(m.group(1))),
]

def rotear(texto):
    t = texto.lower().strip()
    for padrao, funcao in ROTAS:
        m = re.search(padrao, t)
        if m: return funcao(m)
    return None   # não reconheceu: manda para o LLM

# 2) Descrição das ferramentas para o LLM (curta e objetiva)
FERRAMENTAS = [
    {"type": "function", "function": {
        "name": "abrir_programa", "description": "Abre um programa no PC",
        "parameters": {"type": "object",
                       "properties": {"nome": {"type": "string"}},
                       "required": ["nome"]}}},
    {"type": "function", "function": {
        "name": "pesquisar_web", "description": "Pesquisa algo no Google",
        "parameters": {"type": "object",
                       "properties": {"consulta": {"type": "string"}},
                       "required": ["consulta"]}}},
]
DISPONIVEIS = {"abrir_programa": abrir_programa, "pesquisar_web": pesquisar_web}