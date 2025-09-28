from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import JobSeeker

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].error_messages = {'required': 'Email is required.'}
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autofocus': True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['phone', 'location', 'skills', 'experience', 'education']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'e.g., +1 234 567 8900',
                'class': 'form-control profile-input'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., New York, NY',
                'class': 'form-control profile-input'
            }),
            'skills': forms.Textarea(attrs={
                'placeholder': 'List your key skills, e.g., Python, Django, JavaScript...',
                'class': 'form-control profile-textarea',
                'rows': 3
            }),
            'experience': forms.Textarea(attrs={
                'placeholder': 'Describe your work experience, e.g., 3 years as Software Developer...',
                'class': 'form-control profile-textarea',
                'rows': 4
            }),
            'education': forms.Textarea(attrs={
                'placeholder': 'e.g., Bachelor\'s in Computer Science from XYZ University',
                'class': 'form-control profile-textarea',
                'rows': 3
            }),
        }
        help_texts = {
            'phone': 'Enter your contact number for job opportunities.',
            'location': 'Your current city and state for location-based job matches.',
            'skills': 'Highlight your technical and soft skills to attract employers.',
            'experience': 'Detail your professional background and achievements.',
            'education': 'Include degrees, certifications, and relevant coursework.',
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume']

class CombinedProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['phone', 'location', 'skills', 'experience', 'education', 'about', 'resume', 'profile_picture', 'linkedin_url', 'github_url']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'e.g., +1 234 567 8900',
                'class': 'form-control profile-input'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., New York, NY',
                'class': 'form-control profile-input'
            }),
            'skills': forms.Textarea(attrs={
                'placeholder': 'List your key skills, e.g., Python, Django, JavaScript...',
                'class': 'form-control profile-textarea',
                'rows': 3
            }),
            'experience': forms.Textarea(attrs={
                'placeholder': 'Describe your work experience, e.g., 3 years as Software Developer...',
                'class': 'form-control profile-textarea',
                'rows': 4
            }),
            'education': forms.Textarea(attrs={
                'placeholder': 'e.g., Bachelor\'s in Computer Science from XYZ University',
                'class': 'form-control profile-textarea',
                'rows': 3
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'Tell us about yourself, your career goals, and what makes you unique...',
                'class': 'form-control profile-textarea',
                'rows': 4
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'placeholder': 'https://linkedin.com/in/yourprofile',
                'class': 'form-control profile-input'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/yourprofile',
                'class': 'form-control profile-input'
            }),
        }
        help_texts = {
            'phone': 'Enter your contact number for job opportunities.',
            'location': 'Your current city and state for location-based job matches.',
            'skills': 'Highlight your technical and soft skills to attract employers.',
            'experience': 'Detail your professional background and achievements.',
            'education': 'Include degrees, certifications, and relevant coursework.',
            'about': 'Tell us about yourself, your career goals, and what makes you unique.',
            'resume': 'Upload your latest resume file.',
            'profile_picture': 'Upload your profile picture.',
            'linkedin_url': 'Your LinkedIn profile URL for professional networking.',
            'github_url': 'Your GitHub profile URL to showcase your projects and code.',
        }
