// Funções de animação e scroll para LMFIT
document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
    initSmoothScroll();
    initParallaxEffect();
});

function initAnimations() {
    // Observer para animações de entrada
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
    
    // Observar elementos com animação
    document.querySelectorAll('.animate-fadeInUp, .animate-fadeInLeft, .animate-fadeInRight, .animate-scaleIn').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        
        // Adicionar delay sequencial para cards de produtos
        if (el.classList.contains('product-card')) {
            el.style.animationDelay = `${index * 0.1}s`;
        }
        
        observer.observe(el);
    });
}

function initSmoothScroll() {
    // Scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initParallaxEffect() {
    // Efeito parallax removido para evitar problemas de rolagem
    // A seção de categorias agora fica fixa durante a rolagem
}

// Função para animar elementos ao scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('animate-fadeInUp');
        }
    });
}

// Adicionar listener de scroll para animações
window.addEventListener('scroll', animateOnScroll);
