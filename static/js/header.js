
/**
 * Header JavaScript - Language Dropdown & Navigation
 * NovaHaus Website
 */

// Language Dropdown funktionality
function toggleLanguageDropdown() {
    const dropdown = document.getElementById('languageDropdown');
    const dropdownBtn = document.querySelector('.language-dropdown-btn');
    const dropdownContainer = document.querySelector('.language-dropdown');

    if (dropdown && dropdownContainer) {
        dropdown.classList.toggle('show');
        dropdownContainer.classList.toggle('open');
    }
}

// Switch Language Function
function switchLanguage(langCode) {
    // Close dropdown first
    const dropdown = document.getElementById('languageDropdown');
    const dropdownContainer = document.querySelector('.language-dropdown');

    if (dropdown) {
        dropdown.classList.remove('show');
    }
    if (dropdownContainer) {
        dropdownContainer.classList.remove('open');
    }

    // Create form to submit language change
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/set_language/';

    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                     document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);
    }

    // Add language input
    const langInput = document.createElement('input');
    langInput.type = 'hidden';
    langInput.name = 'language';
    langInput.value = langCode;
    form.appendChild(langInput);

    // Add next page input (current page)
    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = window.location.pathname;
    form.appendChild(nextInput);

    // Submit form
    document.body.appendChild(form);
    form.submit();
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.language-dropdown');
    const dropdownMenu = document.getElementById('languageDropdown');

    if (dropdown && dropdownMenu && !dropdown.contains(event.target)) {
        dropdownMenu.classList.remove('show');
        dropdown.classList.remove('open');
    }
});

// Active Navigation Link Highlighting
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.classList.remove('active');

        // Get the href without domain
        const href = link.getAttribute('href');

        // Check if current path matches or starts with the link href
        if (href === currentPath ||
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }

        // Special case for home page
        if (currentPath === '/' && href === '/') {
            link.classList.add('active');
        }
    });
}

// Mobile Navigation Toggle (if needed)
function toggleMobileNav() {
    const mobileNav = document.querySelector('.mobile-nav');
    const overlay = document.querySelector('.nav-overlay');

    if (mobileNav) {
        mobileNav.classList.toggle('active');
    }

    if (overlay) {
        overlay.classList.toggle('active');
    }

    // Prevent body scroll when menu is open
    document.body.classList.toggle('nav-open');
}

// Smooth scrolling for anchor links in navigation
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Header scroll effects
function initHeaderScrollEffects() {
    const header = document.querySelector('.header');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Add/remove scrolled class for styling
        if (scrollTop > 50) {
            header?.classList.add('scrolled');
        } else {
            header?.classList.remove('scrolled');
        }

        // Hide/show header on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            // Scrolling down
            header?.classList.add('header-hidden');
        } else {
            // Scrolling up
            header?.classList.remove('header-hidden');
        }

        lastScrollTop = scrollTop;
    });
}

// Logo animation on load
function initLogoAnimation() {
    const logo = document.querySelector('.logo img');

    if (logo) {
        logo.addEventListener('load', function() {
            this.style.opacity = '0';
            this.style.transform = 'scale(0.8)';

            setTimeout(() => {
                this.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                this.style.opacity = '1';
                this.style.transform = 'scale(1)';
            }, 100);
        });
    }
}

// Keyboard navigation support
function initKeyboardNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const languageBtn = document.querySelector('.language-dropdown-btn');

    // Add keyboard support for language dropdown
    if (languageBtn) {
        languageBtn.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleLanguageDropdown();
            }
        });
    }

    // Add focus handling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('focus', function() {
            this.classList.add('focused');
        });

        link.addEventListener('blur', function() {
            this.classList.remove('focused');
        });
    });
}

// Initialize all header functionality
function initHeader() {
    highlightActiveNavLink();
    initSmoothScrolling();
    initHeaderScrollEffects();
    initLogoAnimation();
    initKeyboardNavigation();

    console.log('✅ Header JavaScript initialized');
}

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', initHeader);

// Export functions for global use
window.toggleLanguageDropdown = toggleLanguageDropdown;
window.switchLanguage = switchLanguage;
window.toggleMobileNav = toggleMobileNav;