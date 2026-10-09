# Prytan for Gemini CLI

An extension bundling Prytan's connector (`https://staging.prytan.ai/mcp`), a context file with the memory protocol, and two hooks that run
on your own computer: at session start and before each message they ask Prytan for what you saved that fits (a task
line of at most 300 characters, made here; the message itself does not leave). Gemini CLI's AfterAgent hook takes no
context, so the checkpoint after each answer is asked for by the context file, not by a hook.

Install: `gemini extensions install https://github.com/KWW-DEV/prytan-plugins` (the extension is the `gemini-cli` folder; until it is in the gallery,
clone the repository and `gemini extensions link ./gemini-cli`). Sign in to Prytan when the connector asks, tick
"Remember my preferences", and for the hooks make a key on https://my.staging.prytan.ai ("Keys for agent apps") and save it in
`~/.prytan/key` or set `PRYTAN_HOOK_KEY`. Licence: MIT.
