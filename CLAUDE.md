# CLAUDE.md — ollama-run

## General Principles
- Be concise and action-oriented. If the request is unambiguous, execute immediately without asking for confirmation or giving lengthy explanations first.

## Git & Shell
- For simple git operations (push, pull, commit, create repo), run the commands directly without clarifying questions. Use `gh` CLI when available.
- Default: stage all relevant files, write a concise commit message, push to current branch.

## Development Workflow
- After implementing any feature or fix, run `python3 -m py_compile main.py` to verify syntax before declaring done.
- Do not claim a feature is complete until it has been verified working.
