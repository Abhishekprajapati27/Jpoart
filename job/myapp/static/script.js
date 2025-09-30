document.addEventListener("DOMContentLoaded", () => {
    // Theme Toggle Functionality
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;

    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark' && themeIcon) {
        body.classList.add('dark-theme');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    // Theme toggle event listener
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-theme');
            const isDark = body.classList.contains('dark-theme');

            // Update icon
            if (isDark) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
                localStorage.setItem('theme', 'dark');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Add 'active' class to the current nav item
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });

    // Signup Form Enhancements
    const signupForm = document.querySelector('.signup-form');
    if (signupForm) {
        const inputs = signupForm.querySelectorAll('.form-control');
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        const emailInput = document.getElementById('id_email');
        const usernameInput = document.getElementById('id_username');

        // Focus and blur effects for all inputs
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.style.transform = 'scale(1.02)';
                this.style.boxShadow = '0 5px 15px rgba(0, 123, 255, 0.2)';
            });

            input.addEventListener('blur', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            });
        });

        // Password strength indicator
        if (password1) {
            const strengthContainer = document.createElement('div');
            strengthContainer.className = 'password-strength-container';
            const strengthDiv = document.createElement('div');
            strengthDiv.className = 'password-strength';
            strengthContainer.appendChild(strengthDiv);
            password1.parentNode.appendChild(strengthContainer);

            password1.addEventListener('input', function() {
                const password = this.value;
                let strength = 'weak';
                strengthDiv.className = 'password-strength strength-' + strength;

                if (password.length >= 12 && /[A-Z]/.test(password) && /\d/.test(password) && /[^a-zA-Z\d]/.test(password)) {
                    strength = 'strong';
                } else if (password.length >= 8) {
                    strength = 'medium';
                }

                strengthDiv.className = 'password-strength strength-' + strength;
            });
        }

        // Password confirmation check
        if (password1 && password2) {
            password2.addEventListener('input', function() {
                if (password1.value && password1.value !== this.value) {
                    this.style.borderColor = '#dc3545';
                    this.classList.add('is-invalid');
                } else {
                    this.style.borderColor = '#28a745';
                    this.classList.remove('is-invalid');
                }
            });
        }

        // Basic email validation
        if (emailInput) {
            emailInput.addEventListener('input', function() {
                const email = this.value;
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (email && !emailRegex.test(email)) {
                    this.style.borderColor = '#dc3545';
                    this.classList.add('is-invalid');
                } else {
                    this.style.borderColor = '#ced4da';
                    this.classList.remove('is-invalid');
                }
            });
        }

        // Basic username validation (alphanumeric, @/./+/-/_ only, max 150 chars)
        if (usernameInput) {
            usernameInput.addEventListener('input', function() {
                const username = this.value;
                const usernameRegex = /^[a-zA-Z0-9@./+_-]{0,150}$/;
                if (username && !usernameRegex.test(username)) {
                    this.style.borderColor = '#dc3545';
                    this.classList.add('is-invalid');
                } else {
                    this.style.borderColor = '#ced4da';
                    this.classList.remove('is-invalid');
                }
            });
        }
    }

    // Home Page Enhancements
    // Time since function for job cards
    function timeSince(date) {
        const seconds = Math.floor((new Date() - new Date(date)) / 1000);
        let interval = Math.floor(seconds / 31536000);
        if (interval >= 1) return interval + " year" + (interval > 1 ? "s" : "") + " ago";
        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) return interval + " month" + (interval > 1 ? "s" : "") + " ago";
        interval = Math.floor(seconds / 86400);
        if (interval >= 1) return interval + " day" + (interval > 1 ? "s" : "") + " ago";
        interval = Math.floor(seconds / 3600);
        if (interval >= 1) return interval + " hour" + (interval > 1 ? "s" : "") + " ago";
        interval = Math.floor(seconds / 60);
        if (interval >= 1) return interval + " minute" + (interval > 1 ? "s" : "") + " ago";
        return "Just now";
    }

    // Apply time since to job cards
    document.querySelectorAll('small[data-created-at]').forEach(function(elem) {
        const dateStr = elem.getAttribute('data-created-at');
        elem.textContent = timeSince(dateStr);
    });

    // Stats counter animation
    const stats = document.querySelectorAll('.stat-item h3');
    stats.forEach(stat => {
        const target = parseInt(stat.textContent);
        let current = 0;
        const increment = target / 50;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target + '+';
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current) + '+';
            }
        }, 20);
    });

    // Scroll animations for cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe category and job cards
    document.querySelectorAll('.category-card, .job-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Category fetch and update
    async function fetchCategories() {
        try {
            const response = await fetch("/api/categories/"); // Assuming API endpoint
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const categories = await response.json();
            updateCategories(categories);
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    }

    function updateCategories(categories) {
        categories.forEach(category => {
            const container = document.querySelector(`.category-card-container[data-category-id='${category.id}']`);
            if (container) {
                const jobCountElem = container.querySelector('.category-job-count');
                if (jobCountElem) {
                    jobCountElem.textContent = `${category.job_count} jobs available`;
                }
            }
        });
    }

    // Initial fetch and poll
    if (document.querySelector('.category-card-container')) {
        fetchCategories();
        setInterval(fetchCategories, 30000);
    }
});
