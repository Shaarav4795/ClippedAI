// Mobile Navigation Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if(targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if(targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// FAQ Accordion
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    
    question.addEventListener('click', () => {
        // Close all other FAQ items
        faqItems.forEach(otherItem => {
            if(otherItem !== item) {
                otherItem.classList.remove('active');
            }
        });
        
        // Toggle current FAQ item
        item.classList.toggle('active');
    });
});

// Sticky header effect with background change on scroll
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Add scrolled class when user scrolls down
    if (scrollTop > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    // Hide navbar when scrolling down and show when scrolling up
    if(scrollTop > lastScrollTop && scrollTop > 100) {
        // Scrolling down
        navbar.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        navbar.style.transform = 'translateY(0)';
    }
    
    lastScrollTop = scrollTop;
});

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Add animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                // Add fade-in-up animation class
                entry.target.classList.add('fade-in-up');
                
                // Add staggered delay for elements in the same container
                if (entry.target.classList.contains('feature-card') || 
                    entry.target.classList.contains('step') || 
                    entry.target.classList.contains('setup-step') ||
                    entry.target.classList.contains('faq-item')) {
                    
                    const items = Array.from(entry.target.parentNode.children);
                    const index = items.indexOf(entry.target);
                    entry.target.style.transitionDelay = `${index * 0.1}s`;
                }
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate in
    document.querySelectorAll('.feature-card, .step, .setup-step, .faq-item').forEach(el => {
        observer.observe(el);
    });
    
    // Add floating animation to hero image
    const heroImage = document.querySelector('.hero-img');
    if (heroImage) {
        heroImage.style.animation = 'float 6s ease-in-out infinite';
    }
});

// Update scroll behavior for smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});