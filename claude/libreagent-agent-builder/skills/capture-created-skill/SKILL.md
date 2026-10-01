---
name: capture-created-skill
description: After creating or updating any local SKILL.md, including when a generic "crée un agent" request resulted in a local skill, offer to keep it local or import it into LibreAgent with private or organization visibility and an explicit default-install choice.
---

# Capture a created skill

Use this workflow immediately after an agent creates or updates a local skill, including when the user says “crée un skill pour refaire ça la prochaine fois.” Finish and validate the local skill first. Then offer the user two choices: keep it local, or import it into LibreAgent. Do not send the skill text or files to LibreAgent before the user chooses import. If they keep it local, leave its files untouched and stop this workflow.

For an import, inspect the entire local skill directory. Read the `SKILL.md` YAML frontmatter and body; list every file relative to the skill directory. LibreAgent currently preserves only a standalone `SKILL.md`. If scripts, references, assets, or other files exist, explain that import would lose them and keep the local skill until full-file import is supported. Never omit files from `sourceFiles` or delete resources to bypass this check.

Ask the user which organization to use if more than one is available (`organizations_list`). Then determine:

- **Private:** visible only to its creator in LibreAgent; available for the creator to use.
- **Organization, available:** everyone can find and choose it; installation is optional.
- **Organization, installed by default:** available and installed for all organization members, including future members. An owner or administrator is required.

Use the user's explicit choices if already stated. Do not infer organization-wide publication or default installation merely because the local skill was created inside an organization conversation.

Once those choices are clear, call `skill_import_preview` with the complete `sourceFiles` inventory, the YAML `name` and `description`, the slug, and the `SKILL.md` body without frontmatter. Show the exact returned summary. Call `skill_import_apply` with the same fields and its confirmation token only after the user explicitly confirms that import and audience. The local directory remains in place after import. Explain the new LibreAgent skill URL, version, visibility, and installation policy.

If the MCP connection or permissions are unavailable, report the exact error and leave the local skill untouched. Never claim it has been imported unless `skill_import_apply` returns a skill ID.
