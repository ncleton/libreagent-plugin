# LibreAgent Agent Builder

This portable Agent Plugin connects ChatGPT, Codex, Claude Code, and other MCP clients to the LibreAgent registry.

ChatGPT and other hosted clients use the server's OAuth 2.1 authorization-code flow with PKCE. Codex local can use the same OAuth flow or read a personal `mcp:access` token from `LIBREAGENT_API_TOKEN`, as declared by `.mcp.json`. Create that token from **Administration → Jetons API et MCP**; its plaintext value is shown once and must stay in the user's secret environment.

The portable `plugin.json` and `mcp.json` are the cross-client source. `.codex-plugin/plugin.json` and `.mcp.json` provide the Codex compatibility overlay. The plugin contains its skills; the repository's `.agents/skills` and `.claude/skills` paths point to those same files.

The MCP endpoint in `mcp.json` is the LibreAgent server binding shared by the organization. Organization-specific agent exports write their current `PUBLIC_API_URL` into that file and add a server hash to the plugin version. If an administrator moves the organization to another server, publish and distribute a newly generated plugin version; never rewrite an already distributed plugin archive.

When Codex trusts this plugin's local `PostToolUse` hook via `/hooks`, a newly written `SKILL.md` prompts the agent to offer a private or organization import. Codex skips untrusted plugin hooks. The hook reads file paths and timestamps only. The `capture-created-skill` workflow also covers clients without local hooks. Import uses `skill_import_preview` and an explicitly confirmed `skill_import_apply`; additional skill files are rejected until LibreAgent can preserve them.

For Codex OAuth, run `codex mcp login libreagent` and complete the LibreAgent sign-in. The server supports authorization code with PKCE and rotating refresh tokens. If Codex reports `authentication_required`, the plugin is installed but the current MCP connection is not signed in.

For an H24 agent created in Codex, the plugin skill first asks for personal or organization access and lists the signed-in member's owned remote computers. It checks ChatGPT authorization on the chosen computer and presents a device code in Codex only when authorization is needed. `hostingComputerId` is bound into the reviewed creation preview. Existing agents use the separate hosting preview/apply tools. A published organization release is required before other members can use a shared draft. The skill checks backup status and reports file exclusions or errors instead of claiming that an incomplete snapshot is protected.
