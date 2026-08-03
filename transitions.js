document.addEventListener('DOMContentLoaded', () => {
  // --- Page Transitions ---
  const loader = document.getElementById('page-transition-loader');
  
  // Hide loader when page loads
  if (loader) {
    loader.classList.add('hidden');
  }

  window.addEventListener('load', () => {
    if (loader) {
      loader.classList.add('hidden');
    }
  });

  // Custom gold cursor
  const cursor = document.createElement('div');
  cursor.className = 'gold-cursor';
  document.body.appendChild(cursor);

  let cursorHideTimer = null;

  const updateCursor = (x, y) => {
    cursor.style.left = `${x}px`;
    cursor.style.top = `${y}px`;
  };

  const showCursor = () => {
    cursor.style.opacity = '1';
    cursor.style.transform = 'translate(-50%, -50%) scale(1)';
  };

  const hideCursor = () => {
    cursor.style.opacity = '0';
    cursor.style.transform = 'translate(-50%, -50%) scale(0.95)';
  };

  document.addEventListener('mousemove', (event) => {
    updateCursor(event.clientX, event.clientY);
    showCursor();

    if (cursorHideTimer) {
      clearTimeout(cursorHideTimer);
    }
    cursorHideTimer = setTimeout(hideCursor, 700);
  });

  document.querySelectorAll('a, button, .btn, input, textarea, select').forEach((element) => {
    element.addEventListener('mouseenter', () => {
      cursor.style.transform = 'translate(-50%, -50%) scale(1.6)';
      cursor.style.boxShadow = '0 0 32px rgba(212,175,55,1), 0 0 70px rgba(212,175,55,0.35)';
    });
    element.addEventListener('mouseleave', () => {
      cursor.style.transform = 'translate(-50%, -50%) scale(1)';
      cursor.style.boxShadow = '0 0 24px rgba(212,175,55,0.9), 0 0 50px rgba(212,175,55,0.35)';
    });
  });

  // Intercept links
  const links = document.querySelectorAll('a');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      const target = link.getAttribute('target');
      
      // Skip if external, new tab, anchor link, or empty
      if (!href || 
          href.startsWith('#') || 
          href.startsWith('mailto:') || 
          href.startsWith('tel:') || 
          target === '_blank' || 
          link.hostname !== window.location.hostname) {
        return;
      }

      // If it's the same page, let normal navigation happen
      if (href === window.location.pathname || href === window.location.pathname + window.location.search) {
          return;
      }

      // Check if user prefers reduced motion
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (prefersReducedMotion) return;

      e.preventDefault();
      
      if (loader) {
        loader.classList.remove('hidden');
        // Wait for the fade animation to complete before navigating
        setTimeout(() => {
          window.location.href = href;
        }, 500); // 500ms should match the CSS transition duration
      } else {
        window.location.href = href;
      }
    });
  });

  // Handle browser back/forward buttons (BFCache)
  window.addEventListener('pageshow', (event) => {
    // If the page was loaded from the back/forward cache, ensure the loader is hidden
    if (event.persisted && loader) {
      loader.classList.add('hidden');
    }
  });


  // --- Smooth Scrolling & Scroll Animations ---

  // Custom Slow Scroll for Contact buttons
  const contactLinks = document.querySelectorAll('a[href="#contact"], a[href$="index.html#contact"]');
  
  contactLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const targetElement = document.getElementById('contact');
      
      if (targetElement) {
        e.preventDefault();
        
        // Temporarily disable native CSS smooth scroll to prevent conflicts
        document.documentElement.style.scrollBehavior = 'auto';
        
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;
        
        // Duration for the slow scroll (1800ms = 1.8 seconds)
        const duration = 1800;
        
        // Very gentle ease-in-out function
        function ease(t, b, c, d) {
          t /= d / 2;
          if (t < 1) return c / 2 * t * t + b;
          t--;
          return -c / 2 * (t * (t - 2) - 1) + b;
        }
        
        function animation(currentTime) {
          if (startTime === null) startTime = currentTime;
          const timeElapsed = currentTime - startTime;
          const run = ease(timeElapsed, startPosition, distance, duration);
          window.scrollTo(0, run);
          
          if (timeElapsed < duration) {
            requestAnimationFrame(animation);
          } else {
            window.scrollTo(0, targetPosition);
            // Re-enable native CSS smooth scroll
            document.documentElement.style.scrollBehavior = '';
            // Update hash without jumping
            history.pushState(null, null, '#contact');
          }
        }
        
        requestAnimationFrame(animation);
      }
    });
  });

  // Back to Top Button
  const backToTopBtn = document.getElementById('back-to-top');
  
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }, { passive: true });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // Intersection Observer for scroll-triggered animations (.fade-up)
  const fadeElements = document.querySelectorAll('.fade-up');
  
  if (fadeElements.length > 0) {
    const fadeObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Only animate once
          fadeObserver.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -50px 0px',
      threshold: 0.1
    });

    fadeElements.forEach(el => fadeObserver.observe(el));
  }

  // Intersection Observer for active nav links
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  
  if (sections.length > 0 && navLinks.length > 0) {
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(`#${id}`)) {
              link.classList.add('active');
            }
          });
        }
      });
    }, {
      rootMargin: '-50% 0px -50% 0px' // Trigger when section is in the middle of viewport
    });

    sections.forEach(section => navObserver.observe(section));
  }
});
