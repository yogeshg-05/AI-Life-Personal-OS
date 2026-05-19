# AI Life Personal OS

This is a Flask-based personal productivity dashboard with tasks, expenses, notes, and an AI integration.

## Local run
1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run locally:

```bash
python app.py
```

The app runs on http://127.0.0.1:5010 by default.

## Prepare GitHub repository and push
1. Initialize git and commit:

```bash
git init
git add .
git commit -m "Initial import: AI Life Personal OS"
```

2. Create a GitHub repository (web or using GitHub CLI) and push:

Using GitHub CLI (`gh`):

```bash
gh repo create <your-username>/ai-life-personal-os --public --source=. --remote=origin --push
```

Or create repo on github.com, then:

```bash
git remote add origin https://github.com/<your-username>/ai-life-personal-os.git
git branch -M main
git push -u origin main
```

## Deploy to Render
1. Go to https://render.com and sign in.
2. Click "New" → "Web Service" → "Connect a repository" and choose the GitHub repository you just pushed.
3. For the service settings use:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Branch: `main`
4. Optionally, add an environment variable `FLASK_ENV=production`.

Alternatively you can import `render.yaml` from the repo when creating a new service.

## Notes & Security
- `config_dashboard.json` contains API keys for AI access; keep it private. The file is included in `.gitignore` by default.
- The app stores user files like `user_registry.json` and per-user dashboards locally; consider migrating to a proper database for production.

If you want, I can initialize a local git repo here and prepare the first commit. I can also provide the exact `gh` commands to create the GitHub repo and attempt to create it if you provide GitHub access (token or `gh` CLI logged in).
