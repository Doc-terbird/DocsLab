document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const mobileToggle = document.getElementById('mobile-toggle');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const closeMobileMenu = document.getElementById('close-mobile-menu');

    // Initialize from localStorage for desktop sidebar
    if (window.innerWidth > 768) {
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed) {
            sidebar.classList.add('w-[70px]');
            mainContent.classList.add('collapsed');
            sidebarToggle.classList.add('rotate-180');
            document.querySelectorAll('.transition-opacity').forEach(el => {
                el.classList.add('opacity-0');
            });
        }
    }

    // Desktop sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', (e) => {
            e.preventDefault();
            const isNowCollapsed = !sidebar.classList.contains('w-[70px]');
            
            sidebar.classList.toggle('w-[70px]');
            mainContent.classList.toggle('collapsed');
            sidebarToggle.classList.toggle('rotate-180');
            
            document.querySelectorAll('.transition-opacity').forEach(el => {
                el.classList.toggle('opacity-0');
            });
            
            localStorage.setItem('sidebarCollapsed', isNowCollapsed);
        });
    }

    // Mobile menu toggle
    if (mobileToggle && mobileMenuOverlay) {
        mobileToggle.addEventListener('click', (e) => {
            e.preventDefault();
            mobileMenuOverlay.style.display = 'block';
            document.body.classList.add('overflow-hidden');
        });
    }

    // Close mobile menu
    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', () => {
            mobileMenuOverlay.style.display = 'none';
            document.body.classList.remove('overflow-hidden');
        });
    }

    // Close mobile menu when clicking outside
    if (mobileMenuOverlay) {
        mobileMenuOverlay.addEventListener('click', (e) => {
            if (e.target === mobileMenuOverlay) {
                mobileMenuOverlay.style.display = 'none';
                document.body.classList.remove('overflow-hidden');
            }
        });
    }
});