---
name: gsk-salesforce
version: 1.0.0
description: 'Salesforce DX CLI (`sf`) operations in a pre-authenticated sandbox.
  Actions: run (forwards any `sf` subcommand).'
metadata:
  category: general
  requires:
    bins:
    - gsk
  cliHelp: gsk sf --help
---

# gsk-salesforce

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for auth, global flags, and security rules.

Salesforce DX CLI (`sf`) operations in a pre-authenticated sandbox. Actions: run (forwards any `sf` subcommand).

**Authorization:** Salesforce uses Genspark's OAuth connector — auth lives in the user's Genspark account, not in the VM browser. If `gsk sf` returns a "not connected" / "not authorized" error, direct the user to `https://www.genspark.ai/api/oauth/salesforce/login` (opens in their main browser). Do **not** recommend the VNC remote desktop / `openclaw://browser` for Salesforce login — that path bypasses the Genspark OAuth token store and the CLI will still report "not connected".

## Usage

```bash
gsk sf [options]
```

**Aliases:** `sf`

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `<action>` (positional) | Yes | Action to perform. 'run': Run an `sf` subcommand inside the pre-authenticated sandbox. Provide the subcommand and flags as you would type them after `sf`. (string, one of: run) |
| `--args` | No | [run] The `sf` subcommand and its arguments (everything after `sf`). Example: `data query --query "SELECT COUNT() FROM Account"`. (string) |
| `--timeout` | No | [run] Optional timeout in seconds. Default 120. Raise for long-running ops like bulk import. (integer, default: `120`) |

## See Also

- [gsk-shared](../gsk-shared/SKILL.md) — Authentication and global flags

