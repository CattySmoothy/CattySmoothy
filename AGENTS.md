# AGENTS.md - CattySmoothy/Raichuu Website

## Project Overview

This is a Flask-based artist portfolio and community website for **Raichuu** (CattySmoothy). The site features:
- Artist profile and portfolio pages
- Community member showcase with Discord-like UI
- Donation/support system via Stripe
- Subscription tiers (Basic, Premium)
- Real-time theme customization (HSL picker)
- Responsive design (Desktop, Tablet, Mobile)

## Essential Commands

### Local Development
```bash
python3 app.py
# Runs on http://localhost:5001 (debug mode, host="0.0.0.0", port=5001)
```

### Dependencies
```bash
pip install -r requirements.txt
# Or with virtualenv: .venv/bin/pip install -r requirements.txt
```

### Deployment
```bash
# Manual deploy on server:
cd /home/rachel/eclipsogate.org/CattySmoothy
git pull origin main
/home/rachel/eclipsogate.org/CattySmoothy/.venv/bin/pip install -r requirements.txt
sudo systemctl restart raichuu
```

## Project Structure

```
CattySmoothy/
├── app.py                 # Flask app entry point, loads routes, sets up Stripe
├── routes.py              # All route handlers, page rendering, Stripe checkout sessions
├── requirements.txt       # Python dependencies
├── crush.json             # Crush MCP configuration (flask-inspector)
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template with sidebar nav, settings panel, game HUD header
│   ├── home.html          # Home/community page with member cards
│   ├── support.html       # Donation and subscription pricing
│   ├── donors.html        # Public donor list
│   └── ...                # Other pages (about, commissions, collections, etc.)
├── static/
│   ├── css/
│   │   ├── style.css      # Page-specific styles
│   │   ├── redesign.css   # Theme variables (ocean, forest, etc.) and dark theme
│   │   └── design-system.css  # Design tokens and utilities
│   └── images/            # Static assets, Figma exports
├── figma/                 # Figma design exports (Desktop.png, Mobile.png, etc.)
├── .github/workflows/
│   └── deploy.yml         # Auto-deploys to eclipsogate.org on push to main
├── raichuu.service        # systemd service for production
└── DEPLOYMENT_GUIDE.md    # Detailed deployment documentation
```

## Architecture & Control Flow

### Request Flow
1. `app.py` creates Flask app, loads `.env`, configures Stripe, calls `register_routes(app)`
2. `routes.py` defines all routes using the `@app.route()` decorator pattern
3. Routes render templates with `render_template()` and pass data (title, publishable_key, donors, etc.)
4. Templates extend `base.html` which provides the sidebar nav, HUD header, and settings panel

### Key Routes
- `/` → `home.html` (community showcase)
- `/support` → `support.html` (donation/subscription pricing)
- `/donate?amount=X` → `donate.html` (Stripe checkout)
- `/create-checkout-session` → POST endpoint for one-time donations
- `/create-subscription-session` → POST endpoint for subscriptions
- `/donors?key=X` → Donor list (secret key reveals all donors)

### Theme System
The site uses CSS custom properties for theming:
- `redesign.css` defines theme variables under `[data-theme="..."]` selectors
- `base.html` includes inline JS that restores saved theme from `localStorage` before paint (prevents flash)
- Settings panel in base.html lets users pick themes via HSL picker

### Data
- **Donors**: Hardcoded in `routes.py` as a Python list (no database)
- **Community members**: Hardcoded in `home.html` as Jinja2 template variables
- **Stripe**: Uses server-side Session create for checkout; no webhooks implemented

## Code Conventions

### Python
- 4-space indentation
- Flask route handlers use `request.args.get()` for query params, `request.get_json()` for POST body
- Stripe amounts converted: `int(float(amount) * 100)` (dollars to cents)
- DOMAIN defaults to `http://localhost:5001`

### HTML/Jinja2
- Templates use `{% extends "base.html" %}` and `{% block content %}{% endblock %}`
- Static assets via `{{ url_for('static', filename='path') }}`
- Conditional classes: `class="{% if condition %}active{% endif %}"`
- Loops: `{% for item in list %}...{% endfor %}`

### CSS
- CSS custom properties for design tokens (defined in `design-system.css`)
- Theme variables in `redesign.css` under `[data-theme="ocean"]`, `[data-theme="forest"]`, etc.
- Inter and Poppins fonts from Google Fonts

## Testing

**No test suite exists.** To verify changes:
1. Run `python3 app.py`
2. Open http://localhost:5001
3. Navigate relevant pages manually

## Important Gotchas

1. **No database**: Donor list and community members are hardcoded. To persist changes, they'd need to be stored in a real database.

2. **Stripe webhook not implemented**: Payment confirmation is client-side only (redirect to `/success`). For production, implement Stripe webhooks to verify payments.

3. **Secret key in donors route**: The admin key `c4tty5m00thy` is hardcoded in `routes.py:45`. Anyone who finds it can see all donors.

4. **Theme flash prevention**: The inline script in `base.html` that restores theme from localStorage MUST stay in `<head>` before any CSS loads, otherwise users see a white flash.

5. **.env not committed**: Environment variables (Stripe keys, etc.) are in a local `.env` file, not in the repo. Server uses a `.venv` in a non-standard location (`/home/rachel/eclipsogate.org/CattySmoothy/.venv`).

6. **Port mismatch**: App runs on port 5001 locally but the systemd service just runs `app.py` (Flask default 5000 in production).

7. **No CSRF protection**: Flask-WTF or similar CSRF protection is not used. The donation forms submit directly to Stripe.

8. **MCP server**: There's a custom Flask inspector MCP in `.crush/mcp/flask-inspector.py` referenced in `crush.json`. This is for development tooling and doesn't affect production.

## Adding New Pages

1. Create HTML file in `templates/`
2. Add route in `routes.py`:
   ```python
   @app.route('/page-name')
   def page_name():
       return render_template('page-name.html', title="Page Title")
   ```
3. Add nav link in `templates/base.html` sidebar
4. Test at http://localhost:5001/page-name

## Adding New Themes

Edit `static/css/redesign.css` and add a new `[data-theme="name"]` block with CSS custom properties. Then add the theme option to the settings panel in `base.html`.

## Git Workflow

- Push to `main` branch triggers GitHub Actions deployment
- `.gitignore` excludes: `__pycache__/`, `*.pyc`, `.venv/`, `.DS_Store`, `.env`
