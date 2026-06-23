---
name: gsk-google-calendar
version: 1.0.0
description: 'Google Calendar operations. Actions: list, create, respond, modify,
  delete.'
metadata:
  category: general
  requires:
    bins:
    - gsk
  cliHelp: gsk google_calendar --help
---

# gsk-google-calendar

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for auth, global flags, and security rules.

Google Calendar operations. Actions: list, create, respond, modify, delete.

## Usage

```bash
gsk google_calendar [options]
```

## Flags

| Flag | Required | Description |
|------|----------|-------------|
| `<action>` (positional) | Yes | Action to perform. 'list': List upcoming calendar events; 'create': Create a new calendar event; 'respond': RSVP (accept / decline / tentative) to an existing invite so the organizer's UI reflects the response; 'modify': Modify (events.patch) an existing event in place without delete+create; 'delete': Delete a calendar event (string, one of: list, create, respond, modify, delete) |
| `--filter_query` | No | [list] Text to filter calendar events, empty for listing all events (string) |
| `--time_min` | No | [list] Optional. Start time of the search range (RFC3339 timestamp) (string) |
| `--time_max` | No | [list] Optional. End time of the search range (RFC3339 timestamp) (string) |
| `--from_account` | No | [list] Optional: Email address of the Gmail account to use. Use this when the user has multiple Gmail accounts connected. If not specified, uses the default Gmail account. \| [create] Optional: Email address of the Gmail account to use. Use this when the user has multiple Gmail accounts connected. If not specified, uses the default Gmail account. \| [respond] Optional: Email address of the Gmail account to use. Defaults to the user's primary Gmail account. \| [modify] Optional: Email address of the Gmail account to use. \| [delete] Optional: Email address of the Gmail account to use. Use this when the user has multiple Gmail accounts connected. If not specified, uses the default Gmail account. (string) |
| `--summary` | No | [create] The title of the event \| [modify] New event title (optional). (string) |
| `--location` | No | [create] The location of the event \| [modify] New event location (optional). (string) |
| `--description` | No | [create] Description or details of the event. Supports restricted HTML formatting (safe subset rendered via Vue v-html): <a>, <b>, <strong>, <i>, <em>, <u>, <br>, <p>, <ul>, <ol>, <li>, <span>, <img>. Use for links, bold, italics, lists, line breaks, images. \| [modify] New event description (optional). Supports the same restricted HTML subset as create. (string) |
| `--time_zone` | No | [create] Time zone for the event (e.g., 'GMT-07:00') \| [modify] Optional time zone for start/end (e.g. 'America/Los_Angeles' or 'GMT-07:00'). (string) |
| `--time_zone_name` | No | [create] Time zone name for the event (e.g., 'America/Los_Angeles') (string) |
| `--start_time` | No | [create] Start time of the event in ISO 8601 format, must include correct timezone offset (e.g., 'yyyy-mm-ddThh:mm:ss+hh:mm') \| [modify] New start time (ISO 8601 with timezone offset, e.g. '2026-05-20T10:00:00-07:00'). Pass with --end_time when rescheduling. (string) |
| `--end_time` | No | [create] End time of the event in ISO 8601 format, must include correct timezone offset (e.g., 'yyyy-mm-ddThh:mm:ss-hh:mm') \| [modify] New end time (ISO 8601 with timezone offset). Required if start_time is given. (string) |
| `--attendees` | No | [create] List of email addresses of attendees \| [modify] REPLACE the attendee list with this set of emails. Mutually exclusive with add_attendees / remove_attendees. (array) |
| `--calendar_id` | No | [create] The calendar identifier. Use 'primary' for the user's primary calendar or provide a specific calendar email address (string) |
| `--event_id` | No | [create] The event identifier. If the request is to modify an existing event, provide the event_id of the event to be modified. If the request is to create a new event, leave this field empty. \| [respond] Google Calendar event id of the invitation to respond to. For a recurring-series instance, the id has shape '<seriesId>_<startTs>'. \| [modify] Google Calendar event id to modify. For a recurring-series instance, the id has shape '<seriesId>_<startTs>'. \| [delete] The Google Calendar event ID to delete (string) |
| `--recurrence` | No | [create] Recurrence rules (e.g., ['RRULE:FREQ=DAILY;COUNT=2']) \| [modify] New recurrence rules (e.g. ['RRULE:FREQ=WEEKLY;BYDAY=MO']). Only honored when scope=series. (array) |
| `--send_notifications` | No | [create] Whether to send email notifications to attendees \| [respond] Whether Google should notify the organizer of the response. Default true. \| [modify] Whether attendees get a notification of the change. Default true. (boolean) |
| `--skip_confirmation` | No | [create] If true, create the event directly in Google Calendar instead of returning a local draft. Required when the caller has no UI to review/confirm a draft (e.g. sandbox agents shelling out via gsk). (boolean, default: `False`) |
| `--auto_skip_confirmation` | No | [create] Set to true ONLY if the workflow step has [AUTO_SKIP_CONFIRMATION] marker. This indicates the node is configured to always skip confirmation. (boolean, default: `False`) |
| `--response` | No | [respond] RSVP value. 'accept' / 'decline' / 'tentative' (Yes / No / Maybe). (string, one of: accept, decline, tentative) |
| `--comment` | No | [respond] Optional free-text comment shown to the organizer alongside the response. (string) |
| `--scope` | No | [respond] Recurring-series scope. 'single' (default) responds for the specific instance only; 'series' responds for the entire series (patches the master event). \| [modify] Recurring-series scope. 'single' (default) patches the specific instance; 'series' patches the master event so the change applies to every occurrence. (string, one of: single, series, default: `single`) |
| `--add_attendees` | No | [modify] Append these attendees to the existing list. Combine with remove_attendees for an additive edit; both leave attendees the caller didn't name alone. (array) |
| `--remove_attendees` | No | [modify] Remove these attendees from the existing list (case-insensitive email match). (array) |
| `--delete_series` | No | [delete] If true and the event is recurring, delete the entire series. If false, only delete the single instance. Default is false. (boolean, default: `False`) |

## See Also

- [gsk-shared](../gsk-shared/SKILL.md) — Authentication and global flags

