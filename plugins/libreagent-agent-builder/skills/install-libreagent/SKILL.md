---
name: install-libreagent
description: Interactive, beginner-friendly onboarding to install LibreAgent. Use whenever someone asks to install, set up, start, reinstall or get instructions for LibreAgent on this computer or another one (Mac, Windows PC, Linux, Raspberry Pi, VPS), to join their company's or team's LibreAgent space from an invitation, to add or pair another computer to their account, or to start using LibreAgent for the first time, for example « donne-moi les consignes pour installer LibreAgent sur un autre ordi », « installe LibreAgent », « je veux rejoindre le LibreAgent de mon équipe ». Start with interactive questions (goal, administrator or member, operating system, this computer or another) instead of a generic guide; hand a company's first server installation to libreagent-first-launch.
---

# Installer LibreAgent, pas à pas

The person may know nothing about LibreAgent, terminals or servers. Never answer an installation request with a ready-made guide covering every case: find out what they want first, then walk them through only their path, one step at a time, checking each result. Speak French, in short sentences, with everyday words: « l'espace LibreAgent de votre équipe », « associer cet ordinateur », « le lien d'invitation ». Name a technical tool only when the person must click or type it.

## How to ask

- Ask with the interactive question tool of the session: in Codex request_user_input, or request_user_input_async when only that one is listed (its answer arrives as the next user message, so stop and wait for it); in Claude Code AskUserQuestion. Only when none is available, ask one plain-text question with two or three short numbered choices.
- Each question has two or three short options, recommended first, each with a one-sentence explanation. The tools add a free answer themselves; do not add « Autre ». Bundle at most three questions that do not depend on each other; ask a dependent question in a later call.
- Do not ask what you can find out. Before the first question, check silently on this computer: the system (uname -sm, or $env:OS on Windows), whether ~/.local/share/libreagent/connection.json exists and which server it names (read only server and cwd, never the token), and whether codex is on the PATH. Use this to pre-select the recommended option, never to skip the goal question.
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

Ask together:

- « Sur quel ordinateur ? »: Mac / PC Windows / Linux ou Raspberry Pi (also a rented server without a screen). Pre-select the detected system.
- « Est-ce l'ordinateur sur lequel nous discutons ? »: Oui, celui-ci / Non, un autre.

Before the steps, state what is needed in one short list: macOS 13 or later (Apple Silicon or Intel); Windows 10 or 11 (x64, or ARM with Windows 11); Linux 64 bits x86-64 or ARM64 (Raspberry Pi 4 or 5 with Raspberry Pi OS 64 bits); an internet connection; a ChatGPT account, because the agents work through Codex, which LibreAgent installs by itself if it is missing; and the computer must stay on for the agents to work. No administrator rights are needed.

The installation page of the server is <adresse>/install/connect/. Give the steps for the chosen system only, one or two at a time, and wait for « C'est fait ».

**Mac**
1. Open <adresse>/install/connect/ and click « Télécharger pour Mac ».
2. Open the downloaded file and drag LibreAgent into Applications, then open LibreAgent from Applications. If macOS says it cannot check the app: click « Terminé », open Réglages Système, Confidentialité et sécurité, and click « Ouvrir quand même » at the bottom.
3. The app comes set for the main LibreAgent server. When the installation page says to replace the server in Réglages (it shows this on every other server, with the address to enter), open Réglages in the app first and enter <adresse>.
4. Click « Associer cet ordinateur ». A LibreAgent page opens: sign in and click « Associer cet ordinateur ». Come back to the app and click « Autoriser ».

**Windows**
1. Open <adresse>/install/connect/, click « Télécharger pour Windows » and open the file. If Windows shows « Windows a protégé votre ordinateur »: « Informations complémentaires », then « Exécuter quand même ».
2. LibreAgent opens at the end. Same steps 3 and 4 as on a Mac.
Without the app, PowerShell works too: irm <adresse>/install.ps1 | iex.

**Linux, Raspberry Pi, rented server**
1. On a server shared with other uses, first create a separate user for the agents: sudo adduser agents, sudo loginctl enable-linger agents, then sudo -iu agents. On a personal computer, run sudo loginctl enable-linger $USER once so LibreAgent keeps running after logout; skip both when sudo is not available and say the service then stops at logout.
2. Paste curl -fsSL <adresse>/install.sh | sh in a terminal (over SSH for a rented server). The command already contains the right server.
3. It shows an association code and opens or names the page Ordinateurs: sign in there, enter the code and approve. Back in the terminal, check the account and organization shown, then confirm. The code is valid 10 minutes; if it expires, run the command again.

**Codex sign-in.** If Codex is not signed in on that computer, LibreAgent shows a ChatGPT link and a code: the person opens the link, signs in to ChatGPT and enters the code. They never send it to you.

**When it is this computer.** You may download and run the command yourself only where it needs no sudo password. Run install.sh in a terminal session (TTY), tell the person to approve the code in the page Ordinateurs, then show them the account and organization the terminal prints and ask, with the question tool, whether to confirm; send the confirmation only after their explicit yes. For the Mac and Windows app, the clicks stay theirs.

**When it is another computer.** Give the steps as a short message they can follow on that computer, and offer to continue there: once LibreAgent is installed, the LibreAgent plugins arrive in Codex and Claude Code on that computer, including this skill.

## 4. Check

- The computer appears « en ligne » in <adresse>/computers; when the LibreAgent MCP tools are available here, also call remote_computers_list.
- On the new computer, a new Codex or Claude Code conversation (one opened before the plugins arrived keeps its previous tools) can call organizations_list: the plugins reach LibreAgent through the paired computer without any sign-in.
- If the computer stays offline: Mac or Windows, open the LibreAgent app and click « Redémarrer le service »; Linux, run libreagent-connect run in a terminal to see the message.

## 5. Wrap-up

Say in a few lines what is ready and checked: the account and its space, the computer associated and online, Codex signed in. Remind them that the computer must stay on for their agents to work, that their ChatGPT and Claude credentials stay on that computer, and that they can revoke it at any time in Ordinateurs. Then ask what to do next: add an agent from the link they received (the agent_link_preview and agent_link_install tools, or LibreAgent, Agents, Ajouter un agent), create their own agent (create-organization-agent skill), or associate another computer.
