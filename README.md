# Prytan plugins

Prytan is your own memory of what you like and how you like things done, shared by every AI you use. Before each
message it recalls what fits; as you talk, your AI saves what you tell it about yourself (preferences, decisions,
plans, interests, changes), on your say-so. You see, correct and delete all of it on your Prytan page (https://my.staging.prytan.ai).

This repository holds the plugins, one per AI app family. Each bundles the same three things: Prytan's connector
(the MCP server at `https://staging.prytan.ai/mcp`), a skill that says when to recall and what to save, and hooks that run on your own
computer. Nothing here is secret; the key for the hooks is yours and is never in this repository.

| Folder | For | What loads |
|---|---|---|
| this folder (the root) | **Claude**: claude.ai, Claude Desktop, Cowork, Claude Code | the connector and the skill everywhere; the hooks in Cowork and Claude Code |
| `codex/` | **ChatGPT and Codex** | the connector and the skills in ChatGPT; the hooks in Codex |
| `gemini-cli/` | **Gemini CLI** | the connector, the context file and the hooks |
| `snippets/` | **VS Code, Cursor, Cline** | the connector; a hook where the app has one |

## Install: Claude

- **claude.ai or Claude Desktop:** Customize → Plugins → Add marketplace → `KWW-DEV/prytan-plugins`, then install
  "Prytan". A plugin installed on claude.ai also reaches Claude Code when you sign in there.
- **Claude Code:** `claude plugin marketplace add KWW-DEV/prytan-plugins` then `claude plugin install prytan@prytan-plugins`.
- **A zip** of each plugin is on the [latest release](https://github.com/KWW-DEV/prytan-plugins/releases/latest) (Customize → Plugins → Add → Upload plugin).

Then sign in to Prytan when the connector asks (an email code on Prytan's own page) and tick "Remember my preferences".

## The hooks and your key

In Cowork and Claude Code the hooks ask Prytan, before each message, for what you saved that fits. A short task line
(at most 300 characters, made on your computer) goes to Prytan; your message does not. For that the hooks need a key:
make one on https://my.staging.prytan.ai under "Keys for agent apps" (shown once; it only reads; revoke it there). Put it in the plugin's
`prytan_key` setting when the app asks, or in a file `~/.prytan/key`, or set `PRYTAN_HOOK_KEY`. Without a key the
hooks stay quiet and the connector still works.

If Prytan is slow or down, the hooks print nothing and the chat goes on unchanged.

## What each app does with this plugin

| App | Connector | Skill | Recall before each message | Checkpoint reminder |
|---|---|---|---|---|
| claude.ai, Claude Desktop | yes | yes | by the AI, from the skill | by the AI, from the skill |
| Cowork | yes | yes | yes (hook) | yes (hook) |
| Claude Code | yes | yes | yes (hook) | yes (hook) |
| ChatGPT (web, desktop, mobile) | yes | yes | by the AI, from the skill | by the AI, from the skill |
| Codex | yes | yes | yes (hook) | yes (hook) |
| Gemini CLI | yes | context file | yes (hook) | by the AI, from the context file |
| VS Code (Copilot) | yes | no | yes (hook, with the setting on) | yes (hook) |
| Cursor | yes | no | at session start only | yes (hook) |
| Cline | yes | no | yes (hook) | no |

## Privacy

The hooks send Prytan only the task line and the app's name, with your key. Nothing you say is logged by Prytan. The
connector is Prytan's one address for everyone: nothing about you is in it. Prytan's privacy policy: https://prytan.ai/legal/personal-privacy.

Licence: MIT.
