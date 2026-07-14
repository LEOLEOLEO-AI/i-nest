---
name: gsk-outlook-calendar
version: 1.0.0
description: 'Outlook Calendar operations. Actions: list, create, respond, modify,
  delete.'
metadata:
  category: general
  requires:
    bins:
    - gsk
  cliHelp: gsk outlook_calendar --help
---

# gsk-outlook-calendar

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for auth, global flags, and security rules.

Outlook Calendar operations. Actions: list, create, respond, modify, delete.

## Usage

```bash
gsk outlook_calendar [options]
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `<action>` (positional) | Yes | Action to perform. 'list': List upcoming calendar events; 'create': Create a new calendar event; 'respond': RSVP (accept / decline / tentative) to an existing invite. Supports --comment and --proposed_new_time (Outlook-only counter-proposal); 'modify': Modify (Graph PATCH /me/events/{id}) an existing event in place without delete+create; 'delete': Delete a calendar event (string, one of: list, create, respond, modify, delete) |
| `--filter_query` | No | [list] Text to filter calendar events by subject. Empty for listing all events in the time range. (string) |
| `--time_min` | No | [list] Optional. Start time for the calendar view (ISO 8601 timestamp). Defaults to 30 days ago. (string) |
| `--time_max` | No | [list] Optional. End time for the calendar view (ISO 8601 timestamp). Defaults to 60 days from now. (string) |
| `--from_account` | No | [list] Optional: Email address of the Outlook account to use. Use this when the user has multiple Outlook accounts connected. If not specified, uses the default Outlook account. \| [create] Optional: Email address of the Outlook account to use. Use this when the user has multiple Outlook accounts connected. If not specified, uses the default Outlook account. \| [respond] Optional: Email address of the Outlook account to use. Defaults to the user's primary Outlook account. \| [modify] Optional: Email address of the Outlook account to use. \| [delete] Optional: Email address of the Outlook account to use. Use this when the user has multiple Outlook accounts connected. If not specified, uses the default Outlook account. (string) |
| `--summary` | No | [create] The title of the event \| [modify] New event title (maps to Outlook's 'subject' field). (string) |
| `--location` | No | [create] The location of the event \| [modify] New event location. (string) |
| `--description` | No | [create] Description or details of the event. Supports restricted HTML formatting (safe subset rendered via Vue v-html): <a>, <b>, <strong>, <i>, <em>, <u>, <br>, <p>, <ul>, <ol>, <li>, <span>, <img>. Use for links, bold, italics, lists, line breaks, images. \| [modify] New event body (HTML allowed — Outlook renders the same restricted subset as create). (string) |
| `--time_zone` | No | [create] Time zone for the event (e.g., 'GMT-07:00') \| [respond] Optional time zone used for the proposed_new_time payload (IANA name, e.g. 'America/Los_Angeles'). Defaults to UTC. \| [modify] Optional IANA time zone for start/end (e.g. 'America/Los_Angeles'). Defaults to UTC. (string) |
| `--time_zone_name` | No | [create] Time zone name for the event (e.g., 'America/Los_Angeles') (string) |
| `--start_time` | No | [create] Start time of the event in ISO 8601 format, must include correct timezone offset (e.g., 'yyyy-mm-ddThh:mm:ss+hh:mm') \| [modify] New start time (ISO 8601 with timezone offset). Pass with --end_time when rescheduling. (string) |
| `--end_time` | No | [create] End time of the event in ISO 8601 format, must include correct timezone offset (e.g., 'yyyy-mm-ddThh:mm:ss-hh:mm') \| [modify] New end time (ISO 8601 with timezone offset). Required if start_time is given. (string) |
| `--attendees` | No | [create] List of email addresses of attendees \| [modify] REPLACE the attendee list with this set of emails. Mutually exclusive with add_attendees / remove_attendees. (array) |
| `--calendar_id` | No | [create] The calendar identifier. Use 'primary' for the user's primary calendar or provide a specific calendar email address (string) |
| `--event_id` | No | [create] The event identifier. If the request is to modify an existing event, provide the event_id of the event to be modified. If the request is to create a new event, leave this field empty. \| [respond] Outlook event id of the invitation to respond to (from a prior outlook_calendar_list call). \| [modify] Outlook event id to modify. \| [delete] The Outlook Calendar event ID to delete (string) |
| `--recurrence` | No | [create] Recurrence pattern for the event (object) |
| `--send_notifications` | No | [create] Whether to send email notifications to attendees \| [modify] Whether attendees get a notification of the change. Default true. (boolean) |
| `--importance` | No | [create] Event importance (low, normal, high) \| [modify] Event importance: low / normal / high. (string) |
| `--sensitivity` | No | [create] Event sensitivity (normal, personal, private, confidential) \| [modify] Event sensitivity: normal / personal / private / confidential. (string) |
| `--show_as` | No | [create] Show as status (free, tentative, busy, oof, workingElsewhere, unknown) \| [modify] Show-as status: free / tentative / busy / oof / workingElsewhere / unknown. (string) |
| `--skip_confirmation` | No | [create] If true, create the event directly in Outlook Calendar instead of returning a local draft. Required when the caller has no UI to review/confirm a draft (e.g. sandbox agents shelling out via gsk). (boolean, default: `False`) |
| `--auto_skip_confirmation` | No | [create] Set to true ONLY if the workflow step has [AUTO_SKIP_CONFIRMATION] marker. This indicates the node is configured to always skip confirmation. (boolean, default: `False`) |
| `--response` | No | [respond] RSVP value. 'accept' / 'decline' / 'tentative' (Yes / No / Maybe). When proposed_new_time is provided, this is forced to 'tentative' because Graph rejects counter-proposals on accept / decline. (string, one of: accept, decline, tentative) |
| `--comment` | No | [respond] Optional free-text comment shown to the organizer alongside the response. (string) |
| `--proposed_new_time` | No | [respond] Optional counter-proposal slot in '<START_ISO>..<END_ISO>' form (e.g. '2026-05-21T14:00:00-07:00..2026-05-21T14:30:00-07:00'). Forces response='tentative' — Graph rejects proposedNewTime on accept / decline. (string) |
| `--scope` | No | [respond] Recurring-series scope. 'single' (default) responds for the specific occurrence only; 'series' resolves the seriesMasterId and responds for the entire series. \| [modify] Recurring-series scope. 'single' (default) patches the specific occurrence; 'series' resolves the seriesMasterId and patches the master event. (string, one of: single, series, default: `single`) |
| `--send_response` | No | [respond] Whether Graph should notify the organizer of the response. Default true. (boolean, default: `True`) |
| `--add_attendees` | No | [modify] Append these attendees to the existing list. (array) |
| `--remove_attendees` | No | [modify] Remove these attendees from the existing list (case-insensitive email match). (array) |
| `--delete_series` | No | [delete] If true and the event is recurring, delete the entire series. If false, only delete the single instance. Default is false. (boolean, default: `False`) |

## See Also

- [gsk-shared](../gsk-shared/SKILL.md) — Authentication and global flags

