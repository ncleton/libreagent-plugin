---
name: create-organization-agent
description: Use as soon as a conversation is building an agent, even indirectly and without naming LibreAgent. Covers "crée un agent", "build an agent", an agent, assistant, bot or copilote that "devra" do something, deep research or benchmarks "pour créer un agent", installing, adapting or writing skills or MCP servers for an agent ("installe tout ça" after such a plan), and writing AGENTS.md or CLAUDE.md for a new agent project. Run this before dual-provider-agents, skill-installer or skill-creator, and keep it active until the agent exists in LibreAgent, is shared as chosen, has its project backed up, and runs H24 when requested.
---

# Create an organization agent

Use LibreAgent MCP as the registry and permission authority. Never treat an organization ID supplied by the conversation as authorization; let every MCP tool verify the signed-in member.

## Detect agent creation and keep the procedure running

Treat the conversation as agent creation when any of these appear, in any language and at any turn:

- the user describes an agent, assistant, bot, copilot or advisor and what it "devra", "doit" or "should" do;
- research, a deepsearch or a comparison is requested "pour créer", "pour construire" or "for building" an agent;
- skills, MCP servers, plugins or data are searched, installed, cloned, adapted or written for that agent, including a short follow-up such as "installe tout ça" or "vas-y";
- an `AGENTS.md`, `CLAUDE.md` or `.agents/skills` tree is created for a new agent project;
- a hook context says that agent creation was detected or that a skill was written during agent work.

On detection, say in one sentence that the agent will be registered in LibreAgent, then continue the requested work. Research and installation are steps of agent creation, never a replacement for it. Do not end the turn that finishes the agent's content without either completing the steps below or asking the remaining questions they require. If the work is spread over several turns, resume the procedure at the first incomplete step instead of restarting it.

The procedure is complete only when all of these are true:

1. `agents_list` shows the agent in the selected organization.
2. Its audience matches the user's choice. An organization agent has a published release (`agent_publish_apply`) before it is described as shared.
3. Its project directory is enrolled with a successful complete snapshot (`agent_backup_status`).
4. When H24 was requested, hosting on the chosen remote computer has been applied and confirmed.

Report each incomplete item with the exact LibreAgent error or the user decision still needed. Never say that the agent is online, shared or H24 before the matching tool has confirmed it.

## Agent project and skill files

Give every agent one project directory, normally the current working directory. Store the agent's own and adapted skills as real directories in `<project>/.agents/skills/<skill>/`, with `<project>/.claude/skills` linking to `../.agents/skills` for Claude Code, and `AGENTS.md` plus `CLAUDE.md` (`@AGENTS.md`) at the project root. Personal skill folders such as `~/.agents/skills` or `~/.codex/skills` are only a local convenience: LibreAgent cannot back them up, share them or move them to a remote computer. When personal folders are also wanted, link them to the project copy rather than the reverse.

Project backups exclude symbolic links, credentials, dependencies and caches. Copy third-party skills into the project with links dereferenced, keep their licenses, and leave reinstallable dependencies such as `node_modules` out; document how to restore them in the project. Never place secrets in the project.

For each skill the agent needs:

- A standalone `SKILL.md` can be imported with `skill_import_preview` and `skill_import_apply`, then pinned in `skillRefs` with its returned skill, release and version.
- A skill with scripts, references, data or assets stays in the project directory. Import is rejected for it, so do not remove files to force an import. Mention those skills in the agent instructions by their project path and rely on the project backup, shared backup and H24 transfer to carry them.

## Tools, accounts and instructions behind each skill

A skill only describes work: the commands it calls (CLIs, MCP servers, browsers) must exist on the computer that runs the agent, and the accounts it reads must be connected there. Before proposing a skill, read its `SKILL.md` and references and list, for this agent, each command the skill needs with its install command, each account or browser session it reads, and each API key.

- Conversations on a LibreAgent remote computer run with a sandboxed shell, the web and a persistent agent home. As soon as an agent with pinned skills is created, updated or published, LibreAgent prepares its tools there without anyone asking: the agent reads its skills, installs what they need without sudo and runs their checks. Follow it with `agent_skill_setup_status` until `ready`, `incomplete` or `failed`, report its `report` as is, and do not call the agent ready before `ready`. Copy each skill's exact install source and check command into the agent instructions (for example the GitHub archive of a tool whose PyPI name belongs to another project), so the preparation and later conversations use the right one.
- For an agent that runs in a Codex or Claude Code project on a computer in front of you, install those tools now on that computer and run the skill's own check command before saying the agent is ready.
- An account the agent must read with the user's identity (Instagram, Reddit, LinkedIn and similar) is a connection: declare it in `connectionRequirements` with `authMode: "end-user"`, tell the user what remains to connect, and do not describe that source as available until its check passes.
- Write instructions that make the agent use these tools for the task the user asked for. Never write an escape hatch such as "si tu ne peux pas consulter ces plateformes, indique cette limite et propose des mots-clés" or "sans prétendre disposer d’un accès": the agent would hand the work back to the user. When a source fails, the agent reports the exact error and the action that unblocks it, and uses the other sources it can reach.

## Basiques

Before choosing skills for a new agent, call `skill_basics_list` for the selected organization with `role` set to the drafted agent's purpose and instructions. Basiques are skills that the server administrator, the organization administrators or the member pinned to be considered for every new agent; pinning never means adding a skill to every agent. The response carries the organization recommender's verdict for each basique in `evaluations`. Propose only the basiques whose `retained` is true and that really serve this agent, next to the skills you derived from the conversation, and say in one sentence which pinned basiques you set aside and why. A social-media research basique, for example, has no place in a funding agent. Add a set-aside basique only when the user asks for it. When `evaluatedBy` is null, suggestions are disabled in the organization: judge each basique against the agent's mission yourself with the same rule. Add a kept `kind: library` basique to `skillRefs` with its returned `skillId`, `releaseId`, `version` and `name`. Import the kept `kind: skills_sh` basiques together with `skill_basics_import_preview` and, after the user's confirmation, `skill_basics_import_apply`, using `visibility: private` for a private agent and `organization` for a shared one; then add the returned `skillRefs`. A skills.sh basique is imported in its current upstream version, so never copy or fork it. If an import fails, report the returned remediation and offer to create the agent without that basique.

## Existing agent from a link

When the user gives a link to an existing agent, such as a public GitHub repository that publishes a Codex plugin (for example https://github.com/ncleton/agentvegan-plugin), do not create a new agent. Call agent_link_preview, present it, ask one at a time who may use it (only them or the whole organization), whether to install it for everyone or leave it available, whether its memory is shared by the team or personal to each member, whether an external consultant (who must have their own LibreAgent server) should administer it, and on which online computer to install it now. Then call agent_link_install with those explicit answers and report installation.status and invitation.delivery as returned.

## Existing project to convert

When the agent is an existing project, application, script or tool that must become shareable with other organizations or administered at clients, apply the convert-project-to-agent skill of this plugin first. It packages the project as a link agent, publishes a clean public repository, verifies it with agent_link_preview and then returns here for installation, backup and sharing.

## Creation workflow

Installing LibreAgent on a computer, joining a team's LibreAgent space or starting LibreAgent for the first time belongs to the install-libreagent skill: apply it instead of improvising steps. Migrating or operating an existing LibreAgent server, its database, backups, Contabo account, or its fleet of computers is outside this plugin: the administrators of the LibreAgent server receive the separate LibreAgent Admin plugin for that work. If someone asks how to operate the server, say that it is reserved for the server's administrators and suggest contacting them.

For a generic request to create an agent, activate this workflow before choosing a local `SKILL.md` or another agent format. Call `organizations_list` to establish the available LibreAgent space, draft the agent definition, and use `agent_create_preview` when the required fields are known. Ask for the intended destination only if it cannot be inferred: private LibreAgent agent, organization agent, or local-only skill. Do not silently substitute a local skill for a LibreAgent agent. If LibreAgent returns `authentication_required`, restore the connection as described in "Signed-out LibreAgent connection" and preserve the draft.

## Signed-out LibreAgent connection

When a LibreAgent tool returns `authentication_required`, restore the connection in this conversation instead of only naming a command. On a computer paired with LibreAgent Connect, the plugins it delivers reach MCP through the local relay `libreagent-connect mcp` and never need a sign-in: run `codex mcp get libreagent`; if its transport is not that command, the computer still has another copy of the plugin or an older Connect, so ask an administrator to synchronize the computer's LibreAgent plugins (MCP tool `libreagent_fleet_plugins_sync`, or the Ordinateurs page) and update Connect. In Claude Code without Connect, ask the person to open `/mcp` and sign in the `libreagent` server. In Codex on the computer in front of the person, ask them to run `codex mcp login libreagent`.

When Codex runs on a remote computer (SSH session, LibreAgent remote computer, or `mcp_oauth_credentials_store = "file"` in `~/.codex/config.toml`), the sign-in page redirects to 127.0.0.1 on the person's own device and never reaches Codex; a login stored earlier in the macOS keychain is also invisible to the file store. Run `python3 <this plugin>/scripts/codex-mcp-login-remote.py start` (the script is two directories above this SKILL.md), give the printed address, and ask the person to approve it in a browser signed in to LibreAgent and to paste back the full 127.0.0.1 address shown at the end. Run `... finish '<that address>'`, then confirm with `codex mcp list` and `organizations_list`. MCP tools already loaded in the current conversation may need a new conversation to use the restored connection. Never ask for a password or a token.

Start by listing accessible agents when the request may refer to an existing one. For a new agent, gather its purpose, instructions, expected skills, memory mode, audience, distribution policy, and whether it must remain available H24. Derive the purpose, instructions and skills from the conversation instead of asking for them again. Ask the audience and H24 questions together, early, while the rest of the work continues: offer **Moi seulement** or **Toute l’organisation**, and H24 on a listed ready remote computer or local use only, unless the user already chose. Sharing and computer placement are separate choices. Produce a complete definition with explicit compatibility entries. A target may be marked `compatible` only when its validation report has no blocking finding.

## Native H24 setup in Codex

If the user wants H24, call `remote_computers_list` for the selected organization and choose an already owned, ready ordinateur distant. Do not infer that a computer must be purchased or move an agent to another member's computer. When no suitable computer is ready, explain the actual missing step and open LibreAgent's native computer purchase flow if the user wants one. Present the real recurring amount and obtain confirmation of that exact order in LibreAgent; agent creation never places an implicit order.

For the chosen computer, call `remote_computer_login_status`. If ChatGPT is already connected, continue without generating another code. Otherwise call `remote_computer_login_start`, show its one-time code and verification URL in this Codex conversation, and let the user authorize it with OpenAI. Poll `remote_computer_login_status` about every five seconds until it is ready or the returned `expiresInSeconds` runs out. An expired code requires a fresh start; never ask the user for their ChatGPT password. In the LibreAgent iOS app, the same code flow happens in its native connection card.

Pass the chosen `hostingComputerId` unchanged through `agent_create_preview` and `agent_create_apply`. For an existing agent, use `agent_hosting_preview` and `agent_hosting_apply` after showing the exact target and source backup impact. If a source project exists, the apply step must confirm a complete backup and transfer before reporting H24. Do not claim H24 merely because the computer is provisioned or a device code was displayed.

All writes use the state-bound two-step flow:

1. Call the matching `*_preview` tool with the exact intended payload.
2. Show the returned summary and impact to the user.
3. Call the matching `*_apply` tool with the unchanged payload and `confirmationToken` only after the user explicitly confirms it.

If the user asks for the graphical builder, call `agent_studio_open`, then open the returned HTTPS URL in the available Codex browser. The Studio page remains editable and uses the same draft revision as MCP.

Use `available` when the agent should appear in the organization catalog. Use `default_installed` only when the user explicitly asks for organization-wide installation; the server restricts it to organization administrators.

Publishing creates an immutable release. Editing an agent after publication changes its draft; publish a new semantic version to update everyone who uses the shared agent. Never rewrite an existing release.

An organization-visible draft is not usable by other members until a validated release is published. Use `agent_publish_preview` and `agent_publish_apply` for that step, and say clearly whether publication has actually succeeded. A private agent remains accessible only to its owner.

After creating or moving an agent, call `agent_backup_status`. Registered Codex projects are never all synchronized as a group. For a local agent that must keep its files backed up, use `agent_backup_sync_preview` to show the exact directory and then `agent_backup_sync_apply` only after the user confirms this agent. The first full snapshot must succeed before the minute scheduler enrolls it. Use `agent_backup_now` for an immediate snapshot without changing the automatic selection. Report the latest complete snapshot, exclusions, or the exact remediation on failure; a pending, offline, oversized, or missing-directory backup does not protect that project's files. Definitions and pinned skill releases remain in LibreAgent independently of project-file backup.

To share local files with colleagues, first verify who can access the agent and publish its organization release when required. Then use `agent_backup_status` to show the latest project snapshot's file inventory and exclusions. Use `agent_backup_share_preview` with that exact backup ID, present the paths and recipients, and call `agent_backup_share_apply` after explicit confirmation. This shares one immutable version only; later private backups do not silently change what colleagues receive. A colleague can restore the shared version into a separate folder on their own paired computer in LibreAgent. Passing `backupId: null` through the same preview/apply pair revokes future access to the files.

For GitHub-backed agents, configure the repository source in Studio. The manifest contract is documented by the LibreAgent server. `daily_auto` checks the exact Git ref once per day and creates a new immutable release only when a validated manifest at a new commit contains a new version.

Keep provider credentials out of agent instructions, skills, memory, releases, and exports. API keys required by the agent's tools go through the API keys section below. Report configuration errors with the remediation returned by LibreAgent.

## API keys and other credentials

When a tool of the agent needs an API key, a client ID and secret, or any other credential, declare it and let LibreAgent store it. Never ask the user to paste a key in the conversation, never write one in the project, `AGENTS.md`, a skill, `.mcp.json`, Codex configuration or the Keychain on the user's behalf, and never accept one if it is pasted anyway: tell the user to revoke it with the provider and enter the new value in LibreAgent.

1. In the agent definition, list each environment variable under the matching connection: `connectionRequirements[].secrets` with `name` (for example `FT_CLIENT_ID`), a short `label` and an optional `description`. Use `authMode: "end-user"` when each person should normally bring their own key, and `"agent-owned"` when the owner usually shares one. Names must be uppercase variable names; LibreAgent refuses names that change how a program starts, such as `PATH`, `LD_*` or `NODE_OPTIONS`.
2. Start the tool through LibreAgent Connect so the values only reach that process, in memory, at launch: `libreagent-connect secrets exec --agent <agent-slug> -- <command> [arguments]`. Put it in a launcher script shipped in the project and referenced by the MCP server definition, because Codex and Claude Code do not always have `~/.local/bin` on their `PATH`: `exec "${LIBREAGENT_CONNECT:-$HOME/.local/bin/libreagent-connect}" secrets exec --agent <agent-slug> -- <tool> [arguments]`. Keep a single `exec` of the tool inside that call, and no fallback that reads the key from another place.
3. After creation, call `agent_secrets_status` and give the user its `configureUrl`. Each value is entered there, in the agent's **Clés API** section, encrypted before storage and never shown again. Each key stays private to the person who saved it. The user decides, key by key, whether to share it with the people allowed to use the agent; only people who can edit the agent can share, and anyone can still save their own key, which then takes priority.
4. Report `effective` per variable: `mine`, `shared` or `missing`. A missing required key makes the tool fail at launch with the same link, so say which keys remain to be entered and by whom. Do not describe the agent as ready while a required key is missing for the owner.

When sharing an agent with the organization, ask the owner whether their keys should be shared too, and remind them that those members can use a shared key without LibreAgent ever showing it to them, and that its use is listed under **Dernières utilisations de vos clés**. A person who runs the agent on their own computer controls that machine; tell an owner who must keep a key away from members to keep it private and let each member bring their own.
