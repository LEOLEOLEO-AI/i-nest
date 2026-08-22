---
name: gsk-task-status
version: 1.0.0
description: 'Look up an existing task project previously created with create_task:
  returns its status, page URL (task_url), and extracted result artifacts. Use this
  — never a new create_task call — when you need the link or outcome of a task you
  already created.'
metadata:
  category: general
  requires:
    bins:
    - gsk
  cliHelp: gsk task_status --help
---

# gsk-task-status

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for auth, global flags, and security rules.

Look up an existing task project previously created with create_task: returns its status, page URL (task_url), and extracted result artifacts. Use this — never a new create_task call — when you need the link or outcome of a task you already created.

## Usage

```bash
gsk task_status [options]
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `<project_id>` (positional) | Yes | The project_id returned by create_task (data.project_id in its response). (string) |

## See Also

- [gsk-shared](../gsk-shared/SKILL.md) — Authentication and global flags


<!-- orphan-cleanup: no MOC found, tagged -->
