#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import psutil
import termios
import tty
import re
from datetime import datetime
from ollama import Client
from duckduckgo_search import DDGS

# --- RAINBOW TECHNOLOGY SIGNATURES ---
# #xyz-rainbow #xyz-rainbowtechnology #rainbowtechnology.xyz #rainbow.xyz #rainbow@rainbowtechnology.xyz #i-love-you #You're not supposed to see this!

ART = r"""
   _____       _       _                     
  |  __ \     (_)     | |                    
  | |__) |__ _ _ _ __ | |__   _____      __  
  |  _  // _` | | '_ \| '_ \ / _ \ \ /\ / /  
  | | \ \ (_| | | | | | |_) | (_) \ V  V /   
  |_|  \_\__,_|_|_| |_|_.__/ \___/ \_/\_/    
                                             
    OLLAMA-RUN V4.2 (LIME-GREEN OUTPUT)
"""

LOGSEQ_PATH = "/media/cloud-xyz/X/[Graph]/pages"
client = Client()

class Session:
    def __init__(self):
        self.model = ""
        self.thinking_mode = "ON"
        self.thinking_level = "Medium"
        self.tools_enabled = True

session = Session()

# --- TOOLS ---
tools = [
    {'type': 'function', 'function': {'name': 'web_search', 'description': 'Búsqueda web.', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}}},
    {'type': 'function', 'function': {'name': 'execute_shell', 'description': 'Bash Linux.', 'parameters': {'type': 'object', 'properties': {'command': {'type': 'string'}}, 'required': ['command']}}},
    {'type': 'function', 'function': {'name': 'logseq_io', 'description': 'Logseq.', 'parameters': {'type': 'object', 'properties': {'action': {'type': 'string', 'enum': ['read', 'write', 'append']}, 'page_name': {'type': 'string'}, 'content': {'type': 'string'}}, 'required': ['action', 'page_name']}}},
    {'type': 'function', 'function': {'name': 'get_system_status', 'description': 'Hardware/Hora.', 'parameters': {'type': 'object', 'properties': {}}}},
]

def web_search(query):
    print(f"\n\033[1;33m[*] Web Search: {query}...\033[0m")
    try:
        with DDGS() as ddgs:
            return json.dumps([r for r in ddgs.text(query, max_results=5)], ensure_ascii=False)
    except Exception as e: return str(e)

def execute_shell(command):
    print(f"\n\033[1;33m[*] Shell Exec: {command}...\033[0m")
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=20)
        return f"OUT: {res.stdout}\nERR: {res.stderr}"
    except Exception as e: return str(e)

def logseq_io(action, page_name, content=None):
    if not page_name.endswith(".md"): page_name += ".md"
    path = os.path.join(LOGSEQ_PATH, page_name)
    try:
        print(f"\n\033[1;33m[*] Logseq ({action}): {page_name}...\033[0m")
        if action == 'read':
            with open(path, 'r', encoding='utf-8') as f: return f.read()
        elif action == 'write':
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f: f.write(content or ""); return "OK"
        elif action == 'append':
            with open(path, 'a', encoding='utf-8') as f: f.write(f"\n- {content}" or ""); return "OK"
    except Exception as e: return str(e)

def get_system_status():
    print(f"\n\033[1;33m[*] System Check...\033[0m")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({"current_time": now, "cpu": psutil.cpu_percent(), "ram_mb": psutil.virtual_memory().available // 10**6})

funcs = {'web_search': web_search, 'execute_shell': execute_shell, 'logseq_io': logseq_io, 'get_system_status': get_system_status}

# --- UI ---
def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b': ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def interactive_menu(options, title):
    idx = 0
    while True:
        os.system('clear')
        print(f"\n  \033[1;36m{title}\033[0m\n")
        for i, opt in enumerate(options):
            if i == idx: print(f"  \033[1;32m> {opt}\033[0m")
            else: print(f"    {opt}")
        key = get_key()
        if key == '\x1b[A': idx = (idx - 1) % len(options)
        elif key == '\x1b[B': idx = (idx + 1) % len(options)
        elif key in ['\r', '\n']: return options[idx]
        elif key == '\x1b': return None

def select_model():
    try:
        models = [m.model for m in client.list().models]
        return interactive_menu(models, "SELECCIONA MODELO")
    except: return None

def get_system_prompt():
    base = "Eres un Asistente de Rainbow Technology. Herramientas: web_search, execute_shell, logseq_io, get_system_status."
    if session.thinking_mode == "OFF": return f"{base}\nResponde directo."
    force = "\nINSTRUCCIÓN CRÍTICA: Razona extensamente ANTES de usar herramientas." if session.thinking_mode == "FORCE" else ""
    thinking = {"Low": "Razona brevemente.", "Medium": "Explica tu plan.", "High": "ANÁLISIS PROFUNDO PASO A PASO."}
    return f"{base}\n{thinking[session.thinking_level]}{force}\nEscribe tu razonamiento de forma visible."

def open_settings():
    while True:
        opt = interactive_menu([f"Modelo: {session.model}", f"Mode: {session.thinking_mode}", f"Level: {session.thinking_level}", "Volver"], "SETTINGS")
        if not opt or "Volver" in opt: break
        if "Modelo" in opt:
            new = select_model()
            if new: session.model = new
        elif "Mode" in opt:
            mode = interactive_menu(["OFF", "ON", "FORCE"], "MODE")
            if mode: session.thinking_mode = mode
        elif "Level" in opt:
            level = interactive_menu(["Low", "Medium", "High"], "LEVEL")
            if level: session.thinking_level = level

def chat():
    os.system('clear')
    print(f"--- RAINBOW OLLAMA-RUN V4.2 ---")
    print(f"Model: {session.model} | Mode: {session.thinking_mode} | Level: {session.thinking_level}")
    msgs = []
    while True:
        try:
            sys_msg = {"role": "system", "content": get_system_prompt()}
            if not msgs or msgs[0]['role'] != 'system': msgs.insert(0, sys_msg)
            else: msgs[0] = sys_msg

            inp = input(f"\n({session.model}) > ")
            if inp.lower() == '/exit': break
            if inp.lower() == '/settings': open_settings(); os.system('clear'); continue

            msgs.append({'role': 'user', 'content': inp})
            full_content = ""
            tools_called = []
            
            # Pensamiento (Cyan)
            if session.thinking_mode != "OFF":
                print("\n\033[1;96m[THINKING]\033[0m \033[0;96m", end="", flush=True)
            
            resp = client.chat(model=session.model, messages=msgs, tools=tools, stream=True)
            for chunk in resp:
                m = chunk['message']
                if m.content:
                    print(m.content, end="", flush=True)
                    full_content += m.content
                if hasattr(m, 'tool_calls') and m.tool_calls: tools_called.extend(m.tool_calls)
            print("\033[0m", end="", flush=True)

            ast_msg = {'role': 'assistant', 'content': full_content}
            if tools_called: ast_msg['tool_calls'] = tools_called
            msgs.append(ast_msg)

            if tools_called:
                for t in tools_called:
                    f = funcs.get(t.function.name)
                    if f:
                        res = f(**t.function.arguments)
                        msgs.append({'role': 'tool', 'content': str(res), 'name': t.function.name})
                
                # Respuesta Final (Verde Lima)
                print("\n\033[1;92mAsistente: ", end="", flush=True)
                final = client.chat(model=session.model, messages=msgs, stream=True)
                f_cont = ""
                for chunk in final:
                    if chunk['message'].content:
                        print(chunk['message'].content, end="", flush=True)
                        f_cont += chunk['message'].content
                print("\033[0m")
                msgs.append({'role': 'assistant', 'content': f_cont})
            else:
                # Si no hubo herramientas, mostramos el contenido como respuesta si no hubo pensamiento previo
                # O si hubo pensamiento, ya se imprimió en cyan. Para consistencia:
                if not tools_called and session.thinking_mode == "OFF":
                    print(f"\033[1;92mAsistente: {full_content}\033[0m")
                elif not tools_called and full_content and session.thinking_mode != "OFF":
                    # Si ya se imprimió en Cyan como pensamiento, no lo repetimos en verde a menos que el usuario quiera
                    pass
                
        except KeyboardInterrupt: break

if __name__ == "__main__":
    session.model = select_model()
    if session.model: chat()
