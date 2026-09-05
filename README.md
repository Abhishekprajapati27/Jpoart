# JPORT - Modern Job Portal Platform

A complete, production-ready Django job portal web application connecting employers and job seekers. Features modern UI/UX, responsive dashboards, instant job applications, profile management, and multi-cloud deployment readiness (Render, Heroku, Railway).

---

## Architecture & Directory Structure

`	ext
jport1/
├── .env.example                   # Environment configuration template
├── .gitignore                     # Unified gitignore for python, venv, env, media
├── build.sh                       # Production build script for PaaS platforms
├── Procfile                       # Root Procfile for web dynos (gunicorn)
├── README.md                      # Project documentation
├── render.yaml                    # Render blueprint for one-click deployment
├── requirements.txt               # Dependencies for cloud buildpacks
├── runtime.txt                    # Python runtime version (3.10.11)
├── scripts/                       # Local helper scripts & SSL tools
│   ├── run_production.bat         # Local production server launcher (Waitress)
│   ├── setup_mkcert.ps1           # Local SSL setup helper
│   └── mkcert_setup_instructions.txt
└── job/                           # Django Project Root
    ├── manage.py                  # Django management CLI
    ├── .env.example               # Subdirectory environment template
    ├── requirements.txt           # Subdirectory requirements
    ├── Procfile                   # Subdirectory Procfile
    ├── media/                     # Uploaded user media (resumes, profile pictures)
    ├── staticfiles/               # Collected production static assets
    ├── job/                       # Django project configuration package
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py            # Hardened, environment-based settings
    │   ├── urls.py                # Main routing & media serving
    │   └── wsgi.py
    └── myapp/                     # Core Job Portal Application
        ├── admin.py               # Django Admin registrations
        ├── apps.py                # App configuration
        ├── forms.py               # Custom auth and profile forms
        ├── models.py              # CustomUser, Job, JobSeeker, Employer, etc.
        ├── tests.py               # Automated unit and integration test suite
        ├── urls.py                # App URL routing
        ├── views.py               # Authentication, search, application & profile views
        ├── migrations/            # Database schema migrations
        ├── templatetags/          # Custom Django template filters
        ├── static/                # CSS styling, dashboard themes, client JS
        └── templates/             # Jinja/Django HTML templates
`

---

## Features

- **Authentication & Roles**: Custom user model supporting both **Job Seekers** and **Employers**.
- **Job Seeker Features**:
  - Browse and search jobs by title, company, location, keywords, or categories.
  - One-click job application with optional custom cover letter & resume upload (automatically uses profile resume as fallback).
  - Track application history and application statuses.
  - Interactive profile management (About, Skills tags, Education, Experience, LinkedIn & GitHub links).
- **Employer Features**:
  - Post, edit, and delete job listings with deadlines and compensation details.
  - Real-time employer dashboard displaying active postings and applicant counts.
  - Review applicant submissions, cover letters, and download submitted resumes.
  - Securely inspect applicant public profiles.
- **Enterprise Ready**:
  - **WhiteNoise** static asset compression.
  - Automated PostgreSQL connection via DATABASE_URL (falls back to SQLite for local development).
  - Reverse proxy SSL headers (SECURE_PROXY_SSL_HEADER) and secure cookie controls.

---

## Quickstart (Local Development)

### 1. Clone & Set Up Virtual Environment

`ash
git clone https://github.com/Abhishekprajapati27/Jpoart.git
cd Jpoart

# Create and activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux / macOS:
source venv/bin/activate
`

### 2. Install Dependencies

`ash
pip install -r requirements.txt
`

### 3. Configure Environment

`ash
cp .env.example job/.env
`

### 4. Run Migrations & Start Server

`ash
cd job
python manage.py migrate
python manage.py runserver
`

Visit http://127.0.0.1:8000/ in your browser.

---

## Running Tests

Run the full automated test suite anytime:

`ash
cd job
python manage.py test
`

---

## Deployment Guide

### Option 1: Deploy to Render (Recommended)

1. Connect your repository to **[Render](https://render.com/)**.
2. Click **New +** -> **Blueprint**, and select this repository. Render will automatically read ender.yaml and provision:
   - A Web Service running gunicorn --chdir job job.wsgi:application
   - A free PostgreSQL database
3. Or manually create a **Web Service**:
   - **Build Command**: ./build.sh
   - **Start Command**: gunicorn --chdir job job.wsgi:application
   - Add environment variables:
     - PYTHON_VERSION: 3.10.11
     - DEBUG: False
     - SECRET_KEY: <generate-a-secure-random-key>
     - ALLOWED_HOSTS: * (or your custom domain)
     - DATABASE_URL: <your-postgresql-internal-url>

### Option 2: Deploy to Heroku

1. Create a new Heroku app:
   `ash
   heroku create my-jport-app
   heroku addons:create heroku-postgresql:essential-0
   `
2. Set configuration:
   `ash
   heroku config:set DEBUG=False SECRET_KEY="your-secret-key" ALLOWED_HOSTS="my-jport-app.herokuapp.com"
   `
3. Push to deploy:
   `ash
   git push heroku master
   heroku run python job/manage.py migrate
   `

### Option 3: Deploy to Railway

1. Click **Deploy from GitHub repo** on [Railway](https://railway.app/).
2. Add a PostgreSQL plugin.
3. Railway automatically detects equirements.txt and Procfile.
4. Set DEBUG=False and ALLOWED_HOSTS=* in Railway Variables.

---

## Environment Variables Reference

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| SECRET_KEY | unsafe-secret-key | Django cryptographic signing key |
| DEBUG | True | Toggle debug mode (False in production) |
| ALLOWED_HOSTS | * | Comma-separated list of allowed hostnames |
| DATABASE_URL | sqlite:///db.sqlite3 | PostgreSQL connection string |
| SECURE_SSL_REDIRECT | True (when DEBUG=False) | Force HTTPS redirects |
| EMAIL_BACKEND | console | Django email delivery backend |
| DEFAULT_FROM_EMAIL| 
oreply@jobportal.com | From header on notification emails |

---

## License

This project is licensed under the [MIT License](job/LICENSE).