---
name: prytan-setup
description: Help the person connect Prytan for the first time: sign in on Prytan's own page, tick what the connection may do, and, for the hooks, make a key on My Prytan and save it in a file.
---

# Setting up Prytan

Prytan's connector signs the person in on Prytan's own page (https://my.staging.prytan.ai): an email code, then a tick for "Remember my
preferences". That is all a chat needs.

The hooks (the recall before each message, the checkpoint reminder) run on this computer and read Prytan with a key
the person makes themselves:

1. Open https://my.staging.prytan.ai and sign in.
2. Under "Keys for agent apps", choose the app and press "Make a key". The key is shown once.
3. Save it in a file named `prytan-key` in this plugin's data folder, or in `~/.prytan/key` (one line, nothing else),
   or set the environment variable PRYTAN_HOOK_KEY. Ask the person to do this themselves rather than paste the key in
   the chat.
4. A key only reads. It is revoked on the same page.

If a hook finds no key, or Prytan is slow or down, it prints nothing and the chat goes on unchanged.
