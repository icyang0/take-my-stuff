# Free Stuff Board

A personal web app to share items you want to give away to friends.

## Project structure

```
free-stuff-board/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Procfile                # Railway start command
├── templates/
│   ├── index.html          # Public browse page
│   ├── admin_login.html    # Admin login
│   └── admin_dashboard.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Local development

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with your credentials (never commit this)
cp .env.example .env
# Fill in the values in .env

# 4. Run the app
flask run
```

The app will be at http://localhost:5000
Admin panel at http://localhost:5000/admin

## Environment variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Random secret string for Flask sessions |
| `DATABASE_URL` | Postgres connection string (auto-set by Railway) |
| `CLOUDINARY_CLOUD_NAME` | From your Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | From your Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | From your Cloudinary dashboard |
| `ADMIN_PASSWORD` | Password to access /admin |

## Deploying to Railway

1. Push this folder to your GitHub repo
2. Connect the repo to your Railway project
3. Add all environment variables in Railway → Variables
4. Railway auto-deploys on every push to main

## Admin panel

Go to `/admin` — log in with your `ADMIN_PASSWORD`.

From there you can:
- Upload new items with a photo, title, category, and optional note
- See which items have been claimed and by whom
- Mark items as gone once picked up
- Delete items at any time
