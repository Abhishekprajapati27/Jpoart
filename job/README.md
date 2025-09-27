# Job Portal

A Django-based job portal application that allows employers to post jobs and job seekers to apply for positions.

## Features

- User registration and authentication
- Employer dashboard for posting jobs
- Job seeker dashboard for applying to jobs
- Resume upload functionality
- Job search and filtering
- Application tracking
- Email notifications

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/job-portal.git
   cd job-portal
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `SECRET_KEY` to a secure random key.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and go to `http://127.0.0.1:8000/`

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS` in `.env` with your domain(s), e.g., `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
3. For PostgreSQL (recommended for production):
   - Install PostgreSQL on your server
   - Create a database and user
   - Update `.env` with:
     ```
     DB_ENGINE=django.db.backends.postgresql
     DB_NAME=your_database_name
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_HOST=localhost
     DB_PORT=5432
     ```
   - Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Use a WSGI server like Gunicorn or Waitress (see `run_production.bat` for example)
6. Configure a web server (e.g., Nginx) as reverse proxy
7. Set up SSL/TLS certificates

## Important Notes

- Replace SECRET_KEY in .env with a secure Django key before production
- For production deployment, set DEBUG=False and configure ALLOWED_HOSTS
- Media files (resumes, images) are excluded from git - users will upload their own
- Database is SQLite for demo; consider PostgreSQL for production

## Usage

- Register as an employer or job seeker
- Employers can post jobs from their dashboard
- Job seekers can browse and apply to jobs
- Upload resumes and manage applications

## Technologies Used

- Django 5.2.5
- Python 3.x
- SQLite (default database)
- HTML/CSS/JavaScript
- Bootstrap (for styling)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
