# Take My Stuff

A personal web app to share items you want to give away to friends.

## Project structure

```
take-my-stuff/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Procfile                # Railway start command
├── templates/
│   ├── index.html          # Public browse page
│   ├── admin_login.html    # Admin login
│   └── admin_dashboard.html
└── static/
    ├── css/style.css
    ├── js/main.js
    └── img/                # Put a custom logo image here if you have one
```

## Local development

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

The app will be at http://localhost:5000
Admin panel at http://localhost:5000/admin

## Environment variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Random secret string for Flask sessions |
| `DATABASE_URL` | Postgres connection string — set this manually by referencing your Postgres service's DATABASE_URL on Railway. Without it, the app falls back to a local SQLite file that gets wiped on every redeploy. |
| `CLOUDINARY_CLOUD_NAME` | From your Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | From your Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | From your Cloudinary dashboard |
| `ADMIN_PASSWORD` | Password to access /admin — share this with close friends if you want them posting items too |

## Deploying to Railway

1. Push this folder to your GitHub repo
2. Connect the repo to your Railway project
3. Add a PostgreSQL database in the same Railway project
4. On your app service, set `DATABASE_URL` to reference the Postgres service (critical — without this, data is lost on every redeploy)
5. Add the remaining environment variables in Railway → Variables
6. Railway auto-deploys on every push to main

## Admin panel

Go to `/admin` — log in with your `ADMIN_PASSWORD`. Since this password may be shared with friends, each item now has a "Posted by" field so everyone can see who posted what.

From there you can:
- Upload new items with a photo, title, category, optional note, and your name
- See which items have been claimed and by whom
- Mark items as gone once picked up
- Delete items at any time
