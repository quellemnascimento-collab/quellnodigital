// Scroll-triggered animations
const animatedEls = document.querySelectorAll(
  '.card, .module-card, .number-item, .faq__item, .before-after__col, .pricing__card'
);

animatedEls.forEach(el => el.classList.add('animate-in'));

const observer = new IntersectionObserver(
  entries => entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  }),
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

animatedEls.forEach(el => observer.observe(el));

// Smooth nav background on scroll
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
  nav.style.borderBottomColor = window.scrollY > 20
    ? 'rgba(255,255,255,.1)'
    : 'rgba(255,255,255,.06)';
}, { passive: true });
