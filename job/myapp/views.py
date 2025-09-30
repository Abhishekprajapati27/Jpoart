from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileSettingsForm, CombinedProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from .models import Job, JobApplication, JobSeeker, Employer, ProfileView, SavedJob, ApplicationNotification, Category
from django.utils import timezone

from django.db.models import Count, Q
from django.http import JsonResponse

import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_protect

logger = logging.getLogger(__name__)

def home(request):
    try:
        # Query categories dynamically with count of active jobs
        categories = Category.objects.annotate(
            job_count=Count('job')  # Removed is_active filter temporarily
        ).values('id', 'name', 'job_count')

        # Query latest jobs with deadline not passed (removed is_active filter temporarily)
        latest_jobs_qs = Job.objects.filter(
            application_deadline__gte=timezone.now().date()
        ).order_by('-created_at')[:5]

        # Prepare jobs list with get_job_type_display and created_at_iso for template
        job_type_display = dict(Job.JOB_TYPE_CHOICES)
        latest_jobs = []
        for job in latest_jobs_qs:
            latest_jobs.append({
                'id': job.id,
                'title': job.title,
                'employer': {'company_name': job.employer.company_name},
                'job_type': job.job_type,
                'get_job_type_display': job_type_display.get(job.job_type, job.job_type),
                'location': job.location,
                'description': job.description,
                'salary': job.salary,
                'created_at_iso': job.created_at.isoformat(),
            })

        context = {
            'categories': categories,
            'latest_jobs': latest_jobs
        }
        return render(request, 'home.html', context)
    except Exception as e:
        logger.error(f"Error in home view: {e}", exc_info=True)
        return render(request, 'home.html', {'categories': [], 'latest_jobs': [], 'error': 'Error loading jobs. Please try again later.'})

def categories_api(request):
    categories = Category.objects.annotate(
        job_count=Count('job', filter=Q(job__is_active=True))
    ).values('id', 'name', 'job_count')
    return JsonResponse(list(categories), safe=False)

def about(request):
    return render(request, 'about.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Normalize email to lowercase for authentication
            email = email.lower() if email else email
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def job_list(request):
    try:
        jobs = Job.objects.filter(application_deadline__gte=timezone.now().date())  # Removed is_active filter temporarily
        query = request.GET.get('q')
        if query:
            jobs = jobs.filter(title__icontains=query)
        return render(request, 'job_list.html', {'jobs': jobs})
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}", exc_info=True)
        return render(request, 'job_list.html', {'error': 'Error fetching jobs. Please try again later.', 'jobs': []})

@login_required
def post_job(request):
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        category_value = request.POST.get('category')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        contact_email = request.POST.get('contact_email')

        # Validate required fields
        if not all([title, company, location, job_type, category_value, deadline, description, requirements]):
            return render(request, 'post_job.html', {'error': 'All required fields must be filled.'})

        # Map category form value to category name
        category_mapping = {
            'it': 'IT & Software',
            'marketing': 'Marketing',
            'design': 'Design',
            'finance': 'Finance',
            'healthcare': 'Healthcare',
            'education': 'Education',
            'engineering': 'Engineering',
            'sales': 'Sales'
        }
        category_name = category_mapping.get(category_value)
        if not category_name:
            return render(request, 'post_job.html', {'error': 'Invalid category selected.'})

        # Get or create Category
        category, created = Category.objects.get_or_create(name=category_name)

        # Get or create Employer
        employer, created = Employer.objects.get_or_create(
            user=request.user,
            defaults={'company_name': company, 'location': location}
        )
        # Update employer company name if it was created or if it's different
        if employer.company_name != company:
            employer.company_name = company
            employer.save()

        # Create Job
        job = Job(
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            job_type=job_type,
            salary=salary,
            category=category,
            employer=employer,
            application_deadline=deadline,
            contact_email=contact_email
        )
        job.save()

        # Redirect to dashboard or job list
        return redirect('dashboard')

    return render(request, 'post_job.html')

@login_required
def dashboard(request):
    try:
        user = request.user
        context = {
            'is_job_seeker': hasattr(user, 'jobseeker'),
            'is_employer': hasattr(user, 'employer'),
        }

        # Data for Job Seekers
        if context['is_job_seeker']:
            job_seeker = user.jobseeker
            context['job_seeker'] = job_seeker
            context['jobs_applied_count'] = JobApplication.objects.filter(job_seeker=job_seeker).count()
            context['profile_views_count'] = ProfileView.objects.filter(job_seeker=job_seeker).count()
            context['saved_jobs_count'] = SavedJob.objects.filter(job_seeker=job_seeker).count()

            # Enhanced dashboard data
            # Skills data for progress bars
            context['user_skills'] = [
                {'name': 'Python', 'level': 85, 'color': 'bg-success'},
                {'name': 'JavaScript', 'level': 70, 'color': 'bg-warning'},
                {'name': 'Project Management', 'level': 90, 'color': 'bg-info'},
                {'name': 'Communication', 'level': 95, 'color': 'bg-primary'},
            ]

            # Career goals
            context['career_goals'] = [
                {'goal': 'Get promoted to Senior Developer', 'progress': 65, 'deadline': 'Dec 2024'},
                {'goal': 'Learn React Framework', 'progress': 40, 'deadline': 'Mar 2024'},
                {'goal': 'Complete 5 certifications', 'progress': 80, 'deadline': 'Jun 2024'},
            ]

            # Quick stats for sidebar
            context['quick_stats'] = {
                'interviews_scheduled': 3,
                'offers_received': 1,
                'network_connections': 45,
                'profile_completeness': 85
            }

            # Recent achievements
            context['recent_achievements'] = [
                {'title': 'Profile 100% Complete', 'icon': 'fas fa-star', 'color': 'text-warning'},
                {'title': '10 Job Applications', 'icon': 'fas fa-paper-plane', 'color': 'text-primary'},
                {'title': 'First Interview', 'icon': 'fas fa-users', 'color': 'text-success'},
            ]

            # Trending jobs in user's category
            user_category = job_seeker.skills.split(',')[0] if job_seeker.skills else 'Technology'
            context['trending_jobs'] = Job.objects.filter(
                category__name__icontains=user_category
            ).order_by('-created_at')[:3]

            # Career insights
            context['career_insights'] = [
                'Your profile has been viewed 15 times this week - great engagement!',
                'Consider updating your skills section with recent certifications',
                'You have 3 pending applications - follow up with employers',
                'Your resume matches 85% of job requirements on average'
            ]

            recent_activity = []
            # Get recent job applications
            recent_applications = JobApplication.objects.filter(job_seeker=job_seeker).order_by('-applied_at')[:3]
            for app in recent_applications:
                recent_activity.append({
                    'title': f'Applied for {app.job.title}',
                    'company': app.job.employer.company_name,
                    'time_ago': app.applied_at.strftime('%B %d, %Y'),
                    'time_obj': app.applied_at,
                    'icon': 'fas fa-paper-plane',
                    'icon_bg': 'bg-primary'
                })
            recent_activity.sort(key=lambda x: x['time_obj'], reverse=True)
            context['recent_activity'] = recent_activity[:7]
            for activity in context['recent_activity']:
                activity.pop('time_obj', None)

        # Data for Employers
        if context['is_employer']:
            employer = user.employer
            user_jobs = list(Job.objects.filter(employer=employer))
            job_ids = [job.id for job in user_jobs]
            
            all_applicants = list(JobApplication.objects.filter(job_id__in=job_ids).select_related('job_seeker__user'))
            
            applicants_by_job = {job_id: [] for job_id in job_ids}
            for app in all_applicants:
                applicants_by_job[app.job_id].append(app)

            user_jobs_with_applicants = []
            for job in user_jobs:
                user_jobs_with_applicants.append({
                    'job': job,
                    'applicants': applicants_by_job.get(job.id, [])
                })

            context['user_jobs_with_applicants'] = user_jobs_with_applicants
            context['total_applicants_count'] = len(all_applicants)

            # Applications summary for dashboard box
            applications_summary = []
            for job in user_jobs:
                applicant_count = len(applicants_by_job.get(job.id, []))
                applications_summary.append({
                    'job': job,
                    'applicant_count': applicant_count
                })
            context['applications_summary'] = applications_summary

            # Workaround for djongo bug: filter in Python instead of in the database
            try:
                all_notifications = ApplicationNotification.objects.filter(
                    employer=employer
                ).select_related(
                    'job_application__job_seeker__user'
                ).order_by('-created_at')
                context['unread_notifications'] = [n for n in all_notifications if not n.is_read]
            except Exception:
                context['unread_notifications'] = [] # Gracefully fail

        return render(request, 'dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in dashboard view: {e}", exc_info=True)
        # Re-raise the exception to get a full debug page
        raise

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def delete_job(request, job_id):
    try:
        user = request.user
        employer = Employer.objects.get(user=user)
        job = get_object_or_404(Job, id=job_id, employer=employer)
        job.delete()
        messages.success(request, "Job post deleted successfully.")
    except Employer.DoesNotExist:
        messages.error(request, "You do not have permission to delete this job.")
    except Exception as e:
        messages.error(request, f"Error deleting job post: {e}")
    return HttpResponseRedirect(reverse('dashboard'))

class ResumeForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume']

class JobApplicationForm(forms.ModelForm):
    resume = forms.FileField(required=False)
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume']
        labels = {
            'cover_letter': 'write about as',
        }

@login_required
@csrf_protect
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Removed is_active filter to avoid DatabaseError
    user = request.user
    job_seeker, created = JobSeeker.objects.get_or_create(user=user)

    # Get application history for the user
    application_history = JobApplication.objects.filter(job_seeker=job_seeker).select_related('job__employer').order_by('-applied_at')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if already applied
            existing_application = JobApplication.objects.filter(job=job, job_seeker=job_seeker).first()
            if existing_application:
                messages.warning(request, "You have already applied for this job.")
                return HttpResponseRedirect(reverse('apply_job', args=[job_id]))

            application = form.save(commit=False)
            application.job = job
            application.job_seeker = job_seeker
            application.save()

            # Create application notification for employer
            try:
                from .models import ApplicationNotification
                ApplicationNotification.objects.create(
                    employer=job.employer,
                    job_application=application,
                    is_read=False
                )
            except Exception as e:
                logger.error(f"Failed to create application notification: {e}")

            # Send email to company email on job application
            company_email = job.employer.user.email if job.employer and job.employer.user else None
            if company_email:
                subject = f"New Job Application for {job.title}"
                message = f"Dear {job.employer.company_name},\n\nYou have received a new application for the job '{job.title}'.\n\nPlease check the admin panel for details."
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [company_email]
                try:
                    send_mail(subject, message, from_email, recipient_list)
                except Exception as e:
                    logger.error(f"Failed to send email notification: {e}")

            # Prepare messages for user and employer
            messages.success(request, "Your application has been submitted successfully. You can view your profile page.")
            # Fix: CustomUser model does not have get_full_name, use first_name and last_name or username
            full_name = f"{user.first_name} {user.last_name}".strip()
            if not full_name:
                full_name = user.username
            employer_message = f"{full_name} has applied to your company. View applicant profile: {request.build_absolute_uri(reverse('view_profile', args=[user.pk]))}"

            # Optionally, send email to employer with profile link
            if company_email:
                try:
                    send_mail(
                        f"New Application from {full_name}",
                        employer_message,
                        from_email,
                        [company_email]
                    )
                except Exception as e:
                    logger.error(f"Failed to send detailed email notification: {e}")

            # Redirect to dashboard after successful application
            return redirect('dashboard')
    else:
        form = JobApplicationForm()

    return render(request, 'apply_job.html', {'form': form, 'job': job, 'application_history': application_history})

@login_required
def update_resume(request):
    user = request.user
    job_seeker, created = JobSeeker.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = CombinedProfileForm(request.POST, request.FILES, instance=job_seeker)
        if form.is_valid():
            form.save()

            # Handle LinkedIn and GitHub URLs separately since they're not in the form
            linkedin_url = request.POST.get('linkedin_url', '').strip()
            github_url = request.POST.get('github_url', '').strip()

            job_seeker.linkedin_url = linkedin_url
            job_seeker.github_url = github_url
            job_seeker.save()

            messages.success(request, "Profile updated successfully.")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = CombinedProfileForm(instance=job_seeker)
    return render(request, 'update_resume.html', {'form': form, 'job_seeker': job_seeker})

@login_required
def profile_settings(request):
    user = request.user
    job_seeker, created = JobSeeker.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=job_seeker)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile settings updated successfully.")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = ProfileSettingsForm(instance=job_seeker)
    return render(request, 'profile_settings.html', {'form': form})

@login_required
def view_applicant(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    # Security check: ensure the logged-in user is the employer for this job
    if request.user != application.job.employer.user:
        messages.error(request, "You don't have permission to view this applicant.")
        return redirect('dashboard')
    return render(request, 'view_applicant.html', {'application': application})

@login_required
def view_profile(request, user_id):
    try:
        # Get the applicant user
        applicant = get_object_or_404(get_user_model(), id=user_id)
        job_seeker = get_object_or_404(JobSeeker, user=applicant)

        # Check if the current user is an employer who has received an application from this user
        try:
            employer = Employer.objects.get(user=request.user)
            # Check if there is an application from this job_seeker to any job posted by this employer
            has_application = JobApplication.objects.filter(
                job_seeker=job_seeker,
                job__employer=employer
            ).exists()
            if not has_application:
                messages.error(request, "You do not have permission to view this profile.")
                return HttpResponseRedirect(reverse('dashboard'))
        except Employer.DoesNotExist:
            messages.error(request, "Only employers can view applicant profiles.")
            return HttpResponseRedirect(reverse('dashboard'))

        # Render the profile using the update_resume template
        return render(request, 'update_resume.html', {'job_seeker': job_seeker, 'view_only': True})
    except Exception as e:
        logger.error(f"Error in view_profile: {e}", exc_info=True)
        messages.error(request, "An error occurred while loading the profile.")
        return HttpResponseRedirect(reverse('dashboard'))
