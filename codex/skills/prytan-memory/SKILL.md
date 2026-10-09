---
name: prytan-memory
description: Prytan, the person's own memory of what they like and how they like things done, shared by every AI they use: when to use recall, and what to save with remember, decide, update and checkpoint.
---

# Prytan: the person's own memory

Prytan is this person's own memory of what they like and how they like things done, shared by every AI they use. They see, correct and delete all of it on their Prytan page; the prytan_settings tool says what this connection may do.

Use recall at the start of a conversation, before the first real answer, and whenever the person's tastes, plans, purchases, places, accounts, writing, design, code or way of speaking matter. What it returns is what they saved with Prytan: apply it unless they say otherwise now, quietly, as a friend who knows them would. With each answer (just before you write it, or right after), call checkpoint with what the person's message told you about them: preferences, decisions (also soft ones: 'I think X is best', 'let's do that'), plans, interests and changes. An empty list is fine. While answering you can also save one thing at once: remember for a preference, an interest, a fact or how they like to be spoken to; decide for a choice among options, a plan or a commitment, also one made in passing inside another request; update when something known changed (what it was, what it is now). They switched this on, on Prytan's own page, so there is no need to ask. Give their own words as quote. Every ten answers or so, and when the chat wraps up, add any choice, preference or change not sent yet; when they say 'save this chat to Prytan', send a full recap, each thing as its own item. Use recall again when they refer to something not in this chat, before asking them to repeat it. Leave out task details that will change, your suggestions, health, religion, politics, sexuality and money details, and sensitive details about others. forget deletes a note when asked.

## Where the Prytan plugin runs hooks

In Cowork, Claude Code and Codex the plugin's hooks also run on the person's own computer: before each message they ask Prytan for what fits (a short task line, at most 300 characters, goes to Prytan; the message itself does not), and when an answer sent no checkpoint they remind you once. Lines that arrive as context from a hook are the same lines recall returns: apply them the same way. In a chat app without hooks, use recall yourself as described above.
