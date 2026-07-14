---
name: shopify-store
version: 1.0.0
description: "Shopify Section and theme template development, and store data queries (e.g. product count). Use when users mention template/theme/section, or ask about their store (products, orders). Default to single Section unless they say 'entire theme' or 'multiple sections'. Covers sections/*.liquid, templates/*.json, deployment confirmation, and QuickToken for API access."
metadata:
  category: general
---

# shopify-store

Use this skill when handling **Shopify** requests in CLAW, including:

- **Theme / Section**: Creating or editing Sections, page templates, Liquid files, holiday/promo pages.
- **Store data**: Querying the store (e.g. product count, orders) — requires Store URL and Admin API token when not already configured.

## Default Scope (for theme/section work)

- **Default**: When users say "template" or "theme" (without "entire" or "complete"), create a **single Section** (e.g. header, product display, holiday section), not a full theme.
- **Full theme**: Only when the user explicitly says "entire theme", "complete theme", or "multiple sections", build a full theme with multiple sections.

| User says | Do this |
|-----------|---------|
| "Create a shopping theme", "Design a product display template" | Create a **Section** (e.g. product-display section) |
| "I need an entire theme", "Help me build a theme with multiple sections" | Create a **full theme** (multiple sections + templates) |

## Capabilities and Boundaries

- **Can do**: Single or multiple Shopify Sections (.liquid + schema), section customization, snippets, page template JSON, holiday/promo sections (e.g. Dragon Boat Festival, Hero, countdown, gift cards), direct deployment to store (with user confirmation).
- **Focus**: Section files (with schema), section assets, compatibility with existing themes, reusable components.
- **Deployment**: Only after explicit user consent; prefer Admin API, then Shopify CLI; if Admin API Token is already set, do not use interactive CLI login.

## Deployment Rules (Required)

1. **No auto-deploy**: Any push to a Shopify store must be confirmed by the user (e.g. "Deploy to live store?") before running; never upload by default.
2. **Template updates are not auto-uploaded**: After modifying or updating templates, do not upload by default; only run upload when the user explicitly says "upload" or "deploy".
3. **Prefer Admin API**: If Admin API Token is configured, use API for deployment; use Shopify CLI only when no token is available.
4. **Security**: Use environment variables for tokens; do not put tokens in code; confirm user has appropriate permissions before deployment.

## How to Get Your Shopify API Tokens

Deployment to a store requires **Shopify Store URL** and **Admin API access token**.

- **If the user already has it configured** (environment variables or Store URL + Access Token filled in the product): Do not guide them to install or obtain again; deploy using the existing configuration.
- **If the user has not configured yet**: Then guide them through these two steps (aligned with CLAW / in-product Shopify setup). **When asking the user for Store URL and Admin API Access Token, always include the QuickToken app link** so they can install it: https://apps.shopify.com/gen-manager

**When asking for credentials**, you can say something like:  
"To access your Shopify store I need: 1) Store URL (e.g. your-store.myshopify.com) 2) Admin API Access Token. You can get the token by installing the QuickToken app: https://apps.shopify.com/gen-manager — open it from your Shopify admin and copy the Store URL and Access Token from the homepage. If these are already set as environment variables, tell me the variable names and I'll use them."

**1. Install QuickToken App**  
Search for "QuickToken" in the Shopify App Store and install it to the user's store, or use the direct link: [QuickToken — API Token Manage](https://apps.shopify.com/gen-manager).

**2. Get Your Shopify Info**  
Open QuickToken from the Shopify admin. Store URL and Access Token are shown on the homepage. Copy and paste them into the form above (or the configuration place required by the current environment).

- Use environment variables for deployment (e.g. `SHOPIFY_ADMIN_API_TOKEN`, store URL); do not put tokens in code or logs.

## Theme Directory Structure

```
Project root/
├── assets/          # CSS, JS, images
├── config/          # settings_schema.json, settings_data.json
├── layout/          # theme.liquid, etc.
├── locales/         # e.g. en.default.json
├── sections/        # Section .liquid files
├── snippets/        # Reusable code snippets
└── templates/       # Page templates (e.g. index.json, page.xxx.json)
```

- Sections go in `sections/<name>.liquid`.
- For JSON page templates (e.g. `templates/page.duanwu.json`), reference sections via `sections` and `order`.

## Section and Page Template

- **Section**: A `.liquid` file with HTML/CSS/Liquid and `{% schema %}` (settings, presets).
- **Page template** (e.g. Horizon): Usually provide both  
  1) Section file: `sections/xxx.liquid` (e.g. `duanwu-festival.liquid`);  
  2) Page template: `templates/page.xxx.json`, where `type` matches the section filename (without `.liquid`).

**Page template JSON example:**

```json
{
  "sections": {
    "main_duanwu": {
      "type": "duanwu-festival",
      "settings": {}
    }
  },
  "order": ["main_duanwu"]
}
```

## CLAW / Permission Notes

- If the system reports "Template files were created successfully, but the page could not be created automatically due to token permission limits":  
  - Treat as **done**: Section and page template files are ready or already uploaded to the user's theme (e.g. Horizon).  
  - **User side**: They need to create or edit the page in Shopify admin and select the corresponding template.
- In your reply, clearly state: which files were generated/uploaded, what the template includes (Hero, intro, cards, countdown, banner, etc.), and what the user should do next in admin.

## Template Content Description

When describing or generating a template, list "what the template includes" by module, e.g. Hero, holiday/event intro, featured gift cards, live countdown, promo banner, so the user can verify and configure in admin.

## Technical Notes

- **Liquid**: Variables `{{ }}`, conditionals `{% if %}`, loops `{% for %}`, `{% schema %}` for settings/presets.
- **Section schema**: `name`, `settings` array (type, id, label), `presets`, so the theme editor can customize.
- **Best practices**: Image optimization, critical CSS/JS, fewer unnecessary API calls in Liquid; keep styles inline or inside the section to avoid depending on assets that are not uploaded.

## See Also

- [gsk-shared](../gsk-shared/SKILL.md) — Authentication and global flags (when using gsk in the same flow)
- [Shopify Theme docs](https://shopify.dev/docs/themes)
- [Liquid reference](https://shopify.dev/docs/api/liquid)
- [gsk-aidrive](../gsk-aidrive/SKILL.md) — For uploading generated files to user storage

