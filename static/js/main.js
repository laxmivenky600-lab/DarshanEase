document.addEventListener('DOMContentLoaded', () => {
    // Add dark mode toggle button dynamically to all pages
    const body = document.body;
    
    // Create dark mode button if not present
    if (!document.getElementById('darkModeToggle')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'darkModeToggle';
        toggleBtn.className = 'dark-mode-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
        toggleBtn.title = 'Toggle Light/Dark Mode';
        body.appendChild(toggleBtn);
        
        // Check local storage for dark mode preference
        if (localStorage.getItem('dark-mode') === 'enabled') {
            body.classList.add('dark-mode');
            toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        }
        
        toggleBtn.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('dark-mode', 'enabled');
                toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                localStorage.setItem('dark-mode', 'disabled');
                toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
            }
        });
    }

    // Create scroll-to-top button if not present
    if (!document.getElementById('scrollTopBtn')) {
        const scrollTopBtn = document.createElement('button');
        scrollTopBtn.id = 'scrollTopBtn';
        scrollTopBtn.className = 'scroll-top-btn';
        scrollTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        scrollTopBtn.title = 'Back to Top';
        body.appendChild(scrollTopBtn);
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add('show');
            } else {
                scrollTopBtn.classList.remove('show');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Initialize AOS if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
});
