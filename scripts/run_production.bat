@echo off
cd /d "%~dp0\..\job"
echo Starting local production server with Waitress on http://127.0.0.1:8000 ...
waitress-serve --host=127.0.0.1 --port=8000 job.wsgi:application
