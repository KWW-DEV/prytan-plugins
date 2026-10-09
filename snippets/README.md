# Prytan in VS Code, Cursor and Cline

The connector is the same everywhere: `https://staging.prytan.ai/mcp` (streamable HTTP; the app signs you in on Prytan's own page). These
files add what each app can run. Copy `prytan_hook.py` from `../hooks/` next to each hook file; it needs Python 3 and
nothing else. For every hook, make a key on https://my.staging.prytan.ai ("Keys for agent apps") and save it in `~/.prytan/key` or set
`PRYTAN_HOOK_KEY`.

| App | Connector | Hooks | File here |
|---|---|---|---|
| VS Code (Copilot agent mode) | `.vscode/mcp.json` | `.github/hooks/prytan.json` with the setting `chat.useClaudeHooks` on: a recall before each message, a reminder when an answer sent no checkpoint | `vscode/` |
| Cursor | Settings → MCP, or `.cursor/mcp.json` | `~/.cursor/hooks.json`: a recall at session start only (Cursor has no hook before each message), a reminder at stop | `cursor/` |
| Cline | MCP Servers → Remote | `~/Documents/Cline/Rules/Hooks/UserPromptSubmit` (macOS and Linux; an executable file named after the event): a recall before each message; no stop hook with context | `cline/` |

Reach, honestly: none of these apps loads a skill from a plugin, so the memory protocol comes only from the tool
descriptions and the hooks. Licence: MIT.
