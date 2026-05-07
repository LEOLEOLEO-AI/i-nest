---
description: Send and receive emails through your dedicated genspark.email address
---

# Email

You have a dedicated email address: **qinrangliu@genspark.email**

Users can contact you by sending emails to this address. Inbound emails are delivered
to you as messages. Use the `gsk` CLI to send replies or new emails.

## Commands

- `gsk email reply "<body>" --to "<message-id>"` — Reply to an inbound email (same thread)
- `gsk email send "<body>" --to "<recipient>" --subject "<subject>"` — Send a new email
- `gsk email status` — Show email configuration and recent threads

## Replying to Emails

When you receive an email, it will appear as a message like:

```
[Email received]
From: alice@gmail.com
Subject: Help me set up my project
Message-ID: <abc123@mail.gmail.com>

Hi, I need help with...
```

To reply in the same thread, use the Message-ID:

```bash
gsk email reply "Here's what I found..." --to "<abc123@mail.gmail.com>"
```

## Sending New Emails

```bash
gsk email send "Hello! Here is the report you requested." \
  --to "alice@gmail.com" \
  --subject "Your requested report"
```

## Guidelines

- Always reply to emails promptly — the sender is waiting for a response
- Keep replies concise, clear, and actionable
- If the email asks you to perform a task, complete it first, then reply with the results
- Reference prior messages in the thread when relevant for context
- Acknowledge attachments and describe what you processed
- Use a professional but friendly tone
- For long results, summarize key points in the email and mention that details are available in the workspace

