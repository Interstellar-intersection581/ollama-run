# 🌈 Rainbow Ollama-Run v4.8

Un orquestador avanzado para **Ollama** con tools, skills, historial persistente, temas visuales y visualización de pensamiento en tiempo real.

![Rainbow Ollama-Run](banner.svg)

## 🚀 Características

- **Tools integradas** — Búsqueda web (DuckDuckGo), Shell, Logseq, Estado del sistema. Toggle ON/OFF con `/tools`
- **Skills** — Roles de IA activables (code review, translate, SQL, seguridad…). Toggle con `/skills`, por defecto OFF
- **Search skills** — Busca e instala nuevas skills online desde `/skills → [Search skills]`
- **Historial persistente** — Autoguardado en `~/.ollama-run/sessions/`. Carga con `/history`
- **Temas visuales** — `default`, `matrix`, `dracula`, `amber`, `mono`. Cambia en `/settings → Theme`
- **Thinking modes** — `OFF`, `ON`, `FORCE`. Bloques de pensamiento y respuesta claramente separados
- **Pull & Search de modelos** — `ollama-run pull <modelo>` o `/search` con flecha `→` para ver variantes
- **Config persistente** — Modelo, tema, tools y skills se recuerdan entre sesiones (`~/.ollama-run/config.json`)

## 🛠️ Instalación

```bash
pip install ollama duckduckgo-search psutil requests
pip install -e .
```

O con el instalador:

```bash
./install.sh
```

## 💬 Comandos en el chat

| Comando | Descripción |
|---|---|
| `/settings` | Modelo, thinking, tema, pull, buscar, chats |
| `/tools` | Activar/desactivar herramientas |
| `/skills` | Activar/desactivar skills de IA |
| `/search` | Buscar modelos en la librería Ollama |
| `/pull <modelo>` | Descargar un modelo |
| `/history` | Ver y cargar conversaciones anteriores |
| `/exit` | Salir |

## ⌨️ Navegación en menús

| Tecla | Acción |
|---|---|
| `↑` `↓` | Navegar |
| `Enter` | Seleccionar |
| `Space` | Toggle ON/OFF (tools/skills) |
| `→` | Ver detalles del modelo |
| `d` | Borrar entrada (historial) |
| `ESC` | Volver / Cancelar |

## 📁 Archivos

```
~/.ollama-run/
├── config.json          # Configuración persistente
├── sessions/            # Historial de conversaciones
└── skills_catalog.json  # Skills instaladas
```

---
#xyz-rainbow | #xyz-rainbowtechnology | #rainbowtechnology.xyz
