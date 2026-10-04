---
name: install-libreagent
description: Interactive, beginner-friendly onboarding to install LibreAgent. Use whenever someone asks to install, set up, start, reinstall or get instructions for LibreAgent on this computer or another one (Mac, Windows PC, Linux, Raspberry Pi, VPS), to join their company's or team's LibreAgent space from an invitation, to add or pair another computer to their account, or to start using LibreAgent for the first time, for example « donne-moi les consignes pour installer LibreAgent sur un autre ordi », « installe LibreAgent », « je veux rejoindre le LibreAgent de mon équipe ». Start with interactive questions (goal, administrator or member, operating system, this computer or another) instead of a generic guide; hand a company's first server installation to libreagent-first-launch.
---

# Installer LibreAgent, pas à pas

The person may know nothing about LibreAgent, terminals or servers. Never answer an installation request with a ready-made guide covering every case: find out what they want first, then walk them through only their path, one step at a time, checking each result. Speak French, in short sentences, with everyday words: « l'espace LibreAgent de votre équipe », « associer cet ordinateur », « le lien d'invitation ». Name a technical tool only when the person must click or type it.

Every message is as short as possible: no introduction, no restating of what you checked, no obvious prerequisite (internet connection, keeping a computer on), no closing advice. Each link or command to open or paste goes alone in its own fenced code block, which the app shows with a copy button.

## How to ask

- Ask with the interactive question tool of the session: in Codex request_user_input when it is listed, otherwise request_user_input_async; in Claude Code AskUserQuestion. Only when none is available, ask one plain-text question with two or three short numbered choices.
- The person's answer is required. Never choose an option yourself, never continue on an assumption, and never treat silence as an answer, however long it lasts; this overrides any general habit of proceeding after a delay. Do every silent check before asking. request_user_input_async returns at once and each answer arrives later as a new message: after the call, do nothing else at all (no command, no check, no message), only wait with the session's sleep tool (for example clock sleep for 60000 ms, repeated; it returns as soon as an answer arrives). After 30 minutes without an answer, or when no sleep tool exists, end the turn with the single sentence « Je reprends dès que vous avez répondu à la question ci-dessus. » The answer then starts the next turn.
- Ask one question per call, so that each answer is complete and nothing is asked twice; ask the next question only after the answer to the previous one. Each question has two or three short options, recommended first, each with a one-sentence explanation. The tools add a free answer themselves; do not add « Autre ».
- Do not ask what you can find out. Before the first question, check silently on this computer: the system (uname -sm, or $env:OS on Windows), whether ~/.local/share/libreagent/connection.json exists and which server it names (read only server and cwd, never the token), and whether codex is on the PATH. Use this only to pre-select the recommended option, never to skip the goal question. Do not report these findings before the person has answered (for example « ce Mac est déjà associé »); mention one later only when it changes a step they must do.
- Never ask for a password, a pairing code, an API key or any secret in the conversation. The person types them in the LibreAgent page, the app or their own terminal.
- After each step the person does on their own, ask « Où en êtes-vous ? » with options such as « C'est fait », « J'ai un message d'erreur », « Je suis bloqué ». On an error, ask them to paste the message, read its « Que faire » line, and fix that before continuing.
- Report only what you checked.

## 1. The goal

Ask « Que voulez-vous faire ? » with these options, the recommended one first (pre-select « Ajouter un ordinateur » when this computer is already paired):

1. **Rejoindre l'espace LibreAgent de mon équipe**: an administrator invited me, or will.
2. **Ajouter un ordinateur à mon compte LibreAgent**: I already use LibreAgent and want my agents to also work on this computer or another one.
3. **Installer LibreAgent pour la première fois**: nobody around me uses it yet; I will be the administrator.

## 2a. Join a team

Ask « Avez-vous reçu un lien d'invitation par e-mail ou message ? » (Oui, je l'ai / Pas encore).

- **Not yet**: explain that a company's LibreAgent space is by invitation only. Give them the sentence to send to their administrator: « Peux-tu m'inviter sur LibreAgent ? Dans LibreAgent : Administration, Membres, Ajouter un membre, avec mon adresse <e-mail>. » Stop there and offer to continue once the link arrives.
- **Yes**: the link looks like https://<adresse>/invite/<code>. Ask them to paste only the address part before /invite (never the whole link, which is personal) or read it from the link if they already pasted it, and remember <adresse> as their server. Steps: open the link on the computer they will use; if they already have a LibreAgent account with the invited e-mail, enter its password, otherwise choose a password of 12 characters or more; click « Créer mon compte et rejoindre » (or « Rejoindre … »). The link works once and for 7 days; if the page says it expired or was used, they ask for a new one. If the page says the invitation is for another e-mail, they click « Se déconnecter » and sign in with the invited address.

Then go to step 3 with that server.

## 2b. Add a computer

The server is the one in connection.json when this computer is already paired; otherwise ask for the LibreAgent address they use (the one in their browser when they open LibreAgent). Check <adresse>/v1/server answers before going on. Go to step 3.

## 2c. First installation

Ask « LibreAgent sera pour qui ? »:

1. **Mon entreprise ou mon équipe**: your own LibreAgent server, always on, which keeps your team's accounts and agents; you will be its administrator.
2. **Moi seul, pour essayer**: an account on the LibreAgent server https://libreagent.92.222.229.134.sslip.io, without installing a server.

- **Company or team**: apply the libreagent-first-launch skill of the LibreAgent Admin plugin now; it presents every hosting option and continues to the administrator account, the computer where agents work, the first agent and colleagues. When that skill is not available in this session, open https://libreagent.92.222.229.134.sslip.io/install/server/ and follow its block « Le plus simple : le plugin LibreAgent Admin »: in Codex, run its two codex plugin commands yourself (or have the person paste the sentence shown); in Claude Code, have the person run its four commands in a terminal. If a command fails, show its message and stop. The skill appears in a new conversation: tell the person to open one and write « Installe LibreAgent pour mon entreprise ».
- **Just me**: read https://libreagent.92.222.229.134.sslip.io/v1/server. Only if registrationAvailable is true, ask them to open that address, create an account (e-mail and a password of 12 characters or more) and tell you when it is done; otherwise explain that this server accepts only invited people and offer the company path. Then go to step 3 with that server.

## 3. Associate the computer

Ask one after the other, each in its own call:

- « Sur quel ordinateur ? »: Mac / PC Windows / Linux ou Raspberry Pi (also a rented server without a screen). Pre-select the detected system.
- « Est-ce l'ordinateur sur lequel nous discutons ? »: Oui, celui-ci / Non, un autre.

### How to write the steps

Go straight to the point. The person is not a beginner at everything: never state the obvious (an internet connection, a recent system, keeping the computer on, no administrator rights, the server answering) and never restate what you checked. No requirement list, no introduction, no closing advice. Mention a prerequisite only when it is actually missing (for example an unsupported system).

- Two or three numbered steps of one short line each.
- Every link or command the person must open or paste goes alone in its own fenced code block, which the app shows with a copy button. Do not put it as a Markdown link in a sentence.
- Keep fallbacks (macOS or Windows warning, expired code, offline computer, Codex sign-in) for when the person reports a problem; then give only the matching fix, as briefly.
- End with one line only: what they will see when it works.

Read <adresse>/install/connect/ once: its script names the server the desktop app is set for (the address compared with location.origin). Add the « Réglages » step only when that server differs from <adresse>.

### Mac or Windows

Model answer (Windows: « Télécharger pour Windows », otherwise identical):

~~~~~
Sur l'autre Mac :

1. Télécharge LibreAgent depuis cette page (« Télécharger pour Mac ») :
   ```
   <adresse>/install/connect/
   ```
2. Ouvre LibreAgent, clique sur « Associer cet ordinateur », connecte-toi sur la page qui s'ouvre, puis clique sur « Autoriser » dans l'app.

L'ordinateur apparaît ensuite dans Ordinateurs.
~~~~~

When the Réglages step applies, insert before step 2: « Dans l'app, ouvre Réglages et remplace le serveur par : » followed by <adresse> in its own code block.

Fixes, only when reported: macOS « impossible de vérifier » → Réglages Système, Confidentialité et sécurité, « Ouvrir quand même »; Windows « Windows a protégé votre ordinateur » → « Informations complémentaires », « Exécuter quand même »; computer offline → in the app, « Redémarrer le service ».

### Linux, Raspberry Pi, rented server

Model answer:

~~~~~
Dans un terminal sur cet ordinateur (en SSH pour un serveur loué) :

1. Lance :
   ```
   curl -fsSL <adresse>/install.sh | sh
   ```
2. Saisis le code affiché dans la page Ordinateurs, puis confirme dans le terminal.

L'ordinateur apparaît ensuite dans Ordinateurs.
~~~~~

On a server shared with other uses, add a first step with its own code block: sudo adduser agents && sudo loginctl enable-linger agents && sudo -iu agents. On a personal Linux computer, add sudo loginctl enable-linger $USER so LibreAgent keeps running after logout. Fixes, only when reported: expired code (valid 10 minutes) → run the command again; computer offline → libreagent-connect run shows the message.

### Codex sign-in

If Codex is not signed in on that computer, LibreAgent shows a ChatGPT link and a code by itself; mention it only if the person asks or is stuck there. They never send the code to you.

### When it is this computer

You may run the command yourself only where it needs no sudo password: run install.sh in a terminal session (TTY), tell the person to approve the code in the page Ordinateurs, show the account and organization the terminal prints and ask with the question tool whether to confirm; confirm only after their explicit yes. For the Mac and Windows app, the clicks stay theirs.

## 4. Check and finish

Once the person says it is done, check that the computer is « en ligne » (remote_computers_list when the LibreAgent tools are available, otherwise ask them to look at Ordinateurs). Then answer in one or two lines: it works, and what they can do next (add an agent from a link, create an agent, associate another computer), as a question with the question tool.
