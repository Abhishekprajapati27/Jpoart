from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Job, Employer, JobSeeker, JobApplication, Category
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class JobPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_email = "testuser@example.com"
        self.user_password = "testpassword123"
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password, username="testuser")
        self.client.login(email=self.user_email, password=self.user_password)

        self.category = Category.objects.create(name="IT & Software")
        self.employer = Employer.objects.create(user=self.user, company_name="Test Company")
        self.job = Job.objects.create(
            title="Test Job",
            description="Job description",
            requirements="Job requirements",
            location="Test Location",
            job_type="full_time",
            salary="1000",
            category=self.category,
            employer=self.employer,
            application_deadline=timezone.now().date() + timedelta(days=10),
            is_active=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Job")

    def test_job_list(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Job")

    def test_apply_job(self):
        response = self.client.get(reverse('apply_job', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'cover_letter': 'This is my cover letter.',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful application

        # Check if application exists
        job_seeker = JobSeeker.objects.get(user=self.user)
        application_exists = JobApplication.objects.filter(job=self.job, job_seeker=job_seeker).exists()
        self.assertTrue(application_exists)

    def test_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Job")

    def test_signup_and_login(self):
        self.client.logout()
        signup_response = self.client.post(reverse('signup'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(signup_response.status_code, 302)  # Redirect after signup

        login_response = self.client.post(reverse('login'), {
            'username': 'newuser@example.com',
            'password': 'newpassword123',
        })
        self.assertEqual(login_response.status_code, 302)  # Redirect after login
