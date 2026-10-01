# LibreAgent Agent Builder

This plugin connects Codex, and Claude Code through the repository's linked skills, to the LibreAgent registry.

Codex connects to the MCP server with the server's OAuth 2.1 authorization-code flow with PKCE.

`.codex-plugin/plugin.json` and `.mcp.json` are the plugin manifest. Do not add a root `plugin.json`: Codex 0.159 then uses the portable manifest and loads none of the plugin's hooks, whatever `extensions.com.openai.hooks` declares. The plugin contains its skills; the repository's `.agents/skills` and `.claude/skills` paths point to those same files.

The MCP endpoint in `.mcp.json` is the LibreAgent server binding shared by the organization. If an administrator moves the organization to another server, publish and distribute a new plugin version; never rewrite an already distributed plugin archive.

When Codex trusts this plugin's local hooks via `/hooks`, a `UserPromptSubmit` hook recognizes a conversation that builds an agent, including indirect requests such as research "pour créer un agent" and later turns like "installe tout ça", and reminds the model to run `create-organization-agent` until the agent is created, shared, backed up and hosted as chosen. A `PostToolUse` hook notices newly written, copied or installed `SKILL.md`, `AGENTS.md` and `CLAUDE.md` files. Codex skips untrusted plugin hooks, so the skill descriptions carry the same detection on their own. The hooks read prompts, file paths and timestamps only and never upload anything. Import uses `skill_import_preview` and an explicitly confirmed `skill_import_apply` for standalone skills; skills with scripts, references or data stay in the agent's project directory, whose backup, shared snapshot and H24 transfer carry every file. Run `python3 -m unittest discover plugins/libreagent-agent-builder/tests` after changing the detection.

For Codex OAuth, run `codex mcp login libreagent` and complete the LibreAgent sign-in. The server supports authorization code with PKCE and rotating refresh tokens. If Codex reports `authentication_required`, the plugin is installed but the current MCP connection is not signed in.

For an H24 agent created in Codex, the plugin skill first asks for personal or organization access and lists the signed-in member's owned remote computers. It checks ChatGPT authorization on the chosen computer and presents a device code in Codex only when authorization is needed. `hostingComputerId` is bound into the reviewed creation preview. Existing agents use the separate hosting preview/apply tools. A published organization release is required before other members can use a shared draft. The skill checks backup status and reports file exclusions or errors instead of claiming that an incomplete snapshot is protected.
