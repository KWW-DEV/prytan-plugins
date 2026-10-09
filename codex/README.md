# Prytan for ChatGPT and Codex

Prytan is your own memory of what you like and how you like things done, shared by every AI you use. This plugin
bundles Prytan's connector (`https://staging.prytan.ai/mcp`), two skills (the memory protocol, and a setup skill), and hooks that run in
Codex on your own computer: a recall before each message and a checkpoint reminder after an answer that sent none.

ChatGPT (web, desktop, mobile) loads the connector and the skills; hooks run only in Codex, after you approve them in
`/hooks`.

## Install

- A local marketplace: add this repository to `~/.agents/plugins/marketplace.json` (or copy the `codex/` folder
  there), or download the zip from the [latest release](https://github.com/KWW-DEV/prytan-plugins/releases/latest).
- Sign in to Prytan when the connector asks (an email code on Prytan's own page) and tick "Remember my preferences".
- For the hooks, make a key on https://my.staging.prytan.ai under "Keys for agent apps" and save it in `~/.prytan/key`, or in a file named
  `prytan-key` in the plugin's data folder, or set `PRYTAN_HOOK_KEY`. The key only reads; revoke it on the same page.

If Prytan is slow or down the hooks print nothing and the chat goes on unchanged. Licence: MIT.
