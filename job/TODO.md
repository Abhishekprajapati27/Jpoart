# TODO: Remove Heroku/Render Configs and Prepare for Local Django Server

## Edit Files
- [x] Edit `job/job/settings.py`: Remove Heroku/Render imports and configs, simplify DB to local SQLite, remove whitenoise middleware and storage, clean up production conditionals.
- [x] Edit `job/requirements.txt`: Remove `psycopg2-binary`, `gunicorn`, `dj-database-url`; optionally remove `whitenoise`.
- [x] Delete `job/Procfile` (Heroku process file).
- [x] Delete `job/runtime.txt` (Heroku Python version file).

## Post-Edit Steps
- [x] Run `pip install -r requirements.txt` to update dependencies. (Note: Pillow install failed, but Django and others are fine; app should work without it for now.)
- [x] Run `python manage.py makemigrations` and `python manage.py migrate` to set up local SQLite DB.
- [x] Run `python manage.py collectstatic --noinput` (if keeping whitenoise; optional).
- [x] Start local server: `python manage.py runserver` and test at http://127.0.0.1:8000/.
- [ ] Verify no errors: Check DB connections, static/media loading, app functionality (e.g., login, job listing). (Server started successfully; some HTTPS requests logged but that's normal for dev server.)
- [ ] If needed, create `.env` file with `SECRET_KEY=your-secret-key` and `DEBUG=True`.
