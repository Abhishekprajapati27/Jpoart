# Dark Theme UI Implementation TODO

- [x] Update style.css: Add dark-specific CSS variables for inline elements (e.g., --hero-bg-dark, --cta-bg-dark); remove light mode :root variables since only dark UI is needed; ensure full dark coverage.
- [x] Update base.html: Change footer classes to use CSS variables instead of hardcoded 'bg-dark'.
- [x] Update home.html: Refactor inline styles to dark equivalents (e.g., dark gradients for hero-section and cta-section, dark card backgrounds).
- [ ] Check and update other templates (e.g., dashboard.html, job_list.html) for any inline styles causing light elements.
- [ ] Test dark UI: Run Django server and verify consistent dark theme on key pages using browser_action.
