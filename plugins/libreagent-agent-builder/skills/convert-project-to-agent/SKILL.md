---
name: convert-project-to-agent
description: Convert an existing project, app, script, CLI or local tool into a real LibreAgent agent that other organizations can add from its link and that a consultant can administer at each client. Use when the user wants to "faire de <projet> un agent", "transformer ce projet en agent LibreAgent", make a project shareable or installable on LibreAgent, deliver a tool to clients through LibreAgent, or administer it at clients as a consultant. Runs before create-organization-agent for existing code; use create-organization-agent alone for an agent written from scratch.
---

# Convert an existing project into a LibreAgent agent

An existing project becomes a LibreAgent agent when another LibreAgent space can add it from one public link, install it on a member's computer through Codex, and when the author can administer it at each client from their own LibreAgent server. Do the conversion in the project itself, verify it with the real LibreAgent tools, and report each step that is not confirmed by a tool.

## What LibreAgent accepts

A link agent is a public GitHub repository that LibreAgent reads at HEAD, without credentials:

- `.agents/plugins/marketplace.json`: catalog `name` (ASCII letters, digits, dashes, underscores or dots) and `plugins[]` entries with `source: {source: "local", path: "./plugins/<name>"}`.
- `plugins/<name>/.codex-plugin/plugin.json`: `name`, semantic `version`, `description`, `skills: "./skills/"`, optional `mcpServers`, and `interface` with `displayName`, `shortDescription`, `longDescription`, `developerName`, `defaultPrompt` and a PNG, JPG, WebP or SVG `logo`. LibreAgent shows these fields in its preview and records the version as the first release.
- `.claude-plugin/marketplace.json` and `plugins/<name>/.claude-plugin/plugin.json` for Claude Code, pointing at the same skills.
- `AGENTS.md` at the root, `CLAUDE.md` containing `@AGENTS.md`.

LibreAgent installs the plugin through Codex on the member's paired computer and clones the repository as the agent's folder. Everything the agent needs to build or run must therefore be in that repository or be installed by one of its skills. `https://github.com/ncleton/agentvegan-plugin` is the reference layout.

## Procedure

1. **Audit the project.** Read its README, entry points, build scripts, configuration and Git state. Write down, from the code: the platform it needs (for example macOS with Apple Mail), the tools to install, the permissions only a person can grant, the services and API keys it uses, and every value that belongs to the current user (names, paths under a home folder, bundle identifiers, default accounts). Note uncommitted work by other people or other conversations and never commit it.
2. **Decide what is private.** List tracked files and history that contain personal or client data: screenshots of real content, exports, logs, captures, local configuration, credentials. If any exist in Git history, the source repository must not become public. Publish instead a separate public repository with a fresh history, produced by an export script kept in the source project (see step 5). Never rewrite or force-push the user's source history to make it publishable.
3. **Make it installable at a client.** Replace user-specific defaults by configuration read at runtime. Each external credential belongs to the person who runs the agent: declare it as described in create-organization-agent, section "API keys and other credentials", or let the application store it in the system keychain from its own interface. Never ship a key, never ask for one in the conversation. When the project only runs on one platform, the installer skill checks it first and stops with the exact reason on any other computer, including LibreAgent's always-on Linux computers.
4. **Write the agent's skills** in `plugins/<name>/skills/` as real directories:
   - an installer skill that checks prerequisites, builds or installs the project from the cloned folder, guides each permission the person must grant, and verifies the result with a real command;
   - one usage skill per real job of the project, calling its actual CLI, API or MCP server and describing the confirmation required before any irreversible action;
   - `AGENTS.md` with the agent's mission, where its code lives, the commands it may run and the rules it must keep.
   Keep the plugin version identical in the Codex and Claude manifests and bump it for every published change.
5. **Build the public repository.** Add an export script to the source project that takes the committed HEAD with `git archive`, removes the private paths found in step 2, copies the plugin layout, and commits the result in the public checkout with a message naming the source commit. Run `gitleaks` (or the github-agent-publisher readiness script) on the export and treat any secret or client detail as a blocker. Create or update the GitHub repository with the visibility the user chose; a link agent must be public. If GitHub authentication fails, stop and give the exact command to fix it (for example `gh auth login -h github.com`); do not describe the agent as shareable.
6. **Verify with LibreAgent.** Call `organizations_list`, then `agent_link_preview` with the public URL. The agent is installable only when the preview returns the plugin with its name, description, version and logo. Report `partnersConfigured`: without it, the consultant step below cannot work and the server administrator must configure `FEDERATION_SIGNING_KEY_FILE`.
7. **Install it in the author's own space** with `agent_link_install` after explicit answers to the four questions of agent_link_preview (audience, installation, memory, consultant) and the computer on which to install it now. Report `installation.status` exactly: installed, waiting_computer, or failed with its cause.
8. **Back up the source project.** The public repository does not contain the private parts, so enroll the source project folder with `agent_backup_sync_preview` and `agent_backup_sync_apply` after confirmation, then confirm a complete snapshot with `agent_backup_status`.

## Administer the agent at clients

Each client company runs its own LibreAgent server. Give the client administrator the public link and the author's e-mail. The client adds the agent from the link (web page Ajouter un agent, or agent_link_install in Codex) and answers "Oui" to the consultant question with that e-mail. The author receives the invitation, opens it, gives the address of their own LibreAgent server and accepts while signed in with the invited address as owner or administrator of their space. The client's server then creates the partnership and delegates the agent in co-managed mode with manual updates. The author administers it from Partenaires, Ouvrir chez le client: definition, versions, diagnostics, audience, installation and memory settings, installation counters. The author never sees the client's members, conversations, memory or files.

When the client already has a partnership with the author's server, the author can instead offer a published version of the agent in managed (locked) or co-managed mode; the client accepts it with automatic or manual updates. A version that changes the engine, channels, connections, schedules or memory mode always waits for the client administrator.

Code updates reach clients through the public repository: bump the plugin version, export, push, and the members' Codex refreshes the plugin from the catalog. Say which clients still need to approve a pending version instead of assuming they are up to date.

## Completion report

Give the public repository URL and commit, the source commit it was exported from, the paths kept private, the result of agent_link_preview, the installation status in the author's space, the backup snapshot, and the exact message to send to a client administrator. List every incomplete item with the returned error or the decision still needed.
