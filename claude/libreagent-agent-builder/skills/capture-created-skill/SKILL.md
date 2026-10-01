---
name: capture-created-skill
description: After creating, installing, copying, renaming or adapting any local SKILL.md, including third-party skills installed for an agent and skills produced by a "crée un agent" request, offer to keep it local or import it into LibreAgent with private or organization visibility and an explicit default-install choice. When the skill serves an agent being built, hand over to create-organization-agent.
---

# Capture a created skill

Use this workflow immediately after an agent creates or updates a local skill, including when the user says “crée un skill pour refaire ça la prochaine fois.” Installing, cloning, copying, renaming or editing a third-party skill counts as creating or updating it. Finish and validate the local skill first.

If the skill was written, installed or adapted for an agent that the conversation is building, follow `create-organization-agent` instead of stopping here: the skill belongs in that agent's project directory and LibreAgent registers the agent itself. Use the import steps below only for standalone skills the agent pins.

Otherwise, offer the user two choices: keep it local, or import it into LibreAgent. Do not send the skill text or files to LibreAgent before the user chooses import. If they keep it local, leave its files untouched and stop this workflow.

For an import, inspect the entire local skill directory. Read the `SKILL.md` YAML frontmatter and body; list every file relative to the skill directory. LibreAgent currently preserves only a standalone `SKILL.md` through skill import. If scripts, references, assets, or other files exist, never omit them from `sourceFiles` or delete them to bypass this check. Offer instead to make the skill part of a LibreAgent agent project with `create-organization-agent`: its project backup keeps every file, can be shared with colleagues and moves with the agent to an H24 computer.

Ask the user which organization to use if more than one is available (`organizations_list`). Then determine:

- **Private:** visible only to its creator in LibreAgent; available for the creator to use.
- **Organization, available:** everyone can find and choose it; installation is optional.
- **Organization, installed by default:** available and installed for all organization members, including future members. An owner or administrator is required.

Use the user's explicit choices if already stated. Do not infer organization-wide publication or default installation merely because the local skill was created inside an organization conversation.

Once those choices are clear, call `skill_import_preview` with the complete `sourceFiles` inventory, the YAML `name` and `description`, the slug, and the `SKILL.md` body without frontmatter. Show the exact returned summary. Call `skill_import_apply` with the same fields and its confirmation token only after the user explicitly confirms that import and audience. The local directory remains in place after import. Explain the new LibreAgent skill URL, version, visibility, and installation policy.

If the MCP connection or permissions are unavailable, report the exact error and leave the local skill untouched. Never claim it has been imported unless `skill_import_apply` returns a skill ID.
