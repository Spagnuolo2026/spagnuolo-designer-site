(() => {
  document.documentElement.dataset.scriptVersion = '4';
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-menu]');

  const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 20);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  const closeMenu = () => {
    toggle?.setAttribute('aria-expanded', 'false');
    menu?.classList.remove('open');
    header?.classList.remove('menu-active');
    document.body.classList.remove('menu-open');
  };

  toggle?.addEventListener('click', () => {
    const willOpen = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(willOpen));
    menu?.classList.toggle('open', willOpen);
    header?.classList.toggle('menu-active', willOpen);
    document.body.classList.toggle('menu-open', willOpen);
  });

  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
  window.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });

  const gallery = document.querySelector('[data-gallery-dialog]');
  const galleryImage = document.querySelector('[data-gallery-image]');
  const galleryCaption = document.querySelector('[data-gallery-caption]');
  const galleryCount = document.querySelector('[data-gallery-count]');
  const galleryItems = [...document.querySelectorAll('[data-gallery-src]')];
  let galleryIndex = 0;
  let touchStartX = 0;

  const showGalleryItem = index => {
    if (!galleryItems.length || !galleryImage) return;
    galleryIndex = (index + galleryItems.length) % galleryItems.length;
    const item = galleryItems[galleryIndex];
    galleryImage.src = item.dataset.gallerySrc;
    galleryImage.alt = item.dataset.galleryAlt;
    galleryCaption.textContent = item.dataset.galleryLabel;
    galleryCount.textContent = `${String(galleryIndex + 1).padStart(2, '0')} / ${String(galleryItems.length).padStart(2, '0')}`;
    galleryItems.forEach((thumb, position) => thumb.classList.toggle('active', position === galleryIndex));
    item.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  };

  document.querySelectorAll('[data-gallery-open]').forEach(button => {
    button.addEventListener('click', () => {
      showGalleryItem(Number(button.dataset.galleryOpen));
      gallery?.showModal();
    });
  });
  galleryItems.forEach((item, index) => item.addEventListener('click', () => showGalleryItem(index)));
  document.querySelector('[data-gallery-prev]')?.addEventListener('click', () => showGalleryItem(galleryIndex - 1));
  document.querySelector('[data-gallery-next]')?.addEventListener('click', () => showGalleryItem(galleryIndex + 1));
  document.querySelector('[data-gallery-close]')?.addEventListener('click', () => gallery?.close());
  gallery?.addEventListener('click', event => { if (event.target === gallery) gallery.close(); });
  gallery?.addEventListener('touchstart', event => { touchStartX = event.changedTouches[0].screenX; }, { passive: true });
  gallery?.addEventListener('touchend', event => {
    const delta = event.changedTouches[0].screenX - touchStartX;
    if (Math.abs(delta) > 45) showGalleryItem(galleryIndex + (delta < 0 ? 1 : -1));
  }, { passive: true });
  window.addEventListener('keydown', event => {
    if (!gallery?.open) return;
    if (event.key === 'ArrowRight') showGalleryItem(galleryIndex + 1);
    if (event.key === 'ArrowLeft') showGalleryItem(galleryIndex - 1);
  });

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = [...document.querySelectorAll('.reveal')];
  const progress = document.querySelector('[data-scroll-progress]');
  const heroParallax = document.querySelector('[data-hero-parallax]');
  const parallaxItems = [...document.querySelectorAll('[data-parallax]')];
  let motionFrame = 0;

  const updateMotion = () => {
    motionFrame = 0;
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
    if (progress) progress.style.transform = `scaleX(${ratio})`;

    if (!reduceMotion) {
      revealItems.forEach(item => {
        const rect = item.getBoundingClientRect();
        if (rect.top < window.innerHeight * .94 && rect.bottom > 0) item.classList.add('visible');
      });
      if (heroParallax) heroParallax.style.setProperty('--hero-scroll', `${Math.min(window.scrollY * 0.045, 24)}px`);
      parallaxItems.forEach(item => {
        const rect = item.getBoundingClientRect();
        const depth = Number(item.dataset.parallax || 0);
        const offset = Math.max(-1, Math.min(1, (window.innerHeight / 2 - (rect.top + rect.height / 2)) / window.innerHeight));
        item.style.transform = `translate3d(0, ${offset * depth}px, 0)`;
      });
    }
  };

  const requestMotionUpdate = () => {
    if (!motionFrame) motionFrame = window.requestAnimationFrame(updateMotion);
  };
  updateMotion();
  window.addEventListener('scroll', updateMotion, { passive: true });
  window.addEventListener('resize', requestMotionUpdate);

  const heroVisual = document.querySelector('[data-hero-reel]');
  if (heroVisual && heroParallax && !reduceMotion && window.matchMedia('(pointer:fine)').matches) {
    heroVisual.addEventListener('pointermove', event => {
      const rect = heroVisual.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width - .5) * 12;
      const y = ((event.clientY - rect.top) / rect.height - .5) * 10;
      heroParallax.style.setProperty('--hero-x', `${x}px`);
      heroParallax.style.setProperty('--hero-y', `${y}px`);
    });
    heroVisual.addEventListener('pointerleave', () => {
      heroParallax.style.setProperty('--hero-x', '0px');
      heroParallax.style.setProperty('--hero-y', '0px');
    });
  }

  const heroShots = [...document.querySelectorAll('[data-hero-shot]')];
  const heroControls = [...document.querySelectorAll('[data-hero-go]')];
  const heroNumber = document.querySelector('[data-hero-number]');
  const heroLabel = document.querySelector('[data-hero-label]');
  const heroLabels = ['Alessandra Spagnuolo', 'Nude rosado com glitter', 'Cromado rosa e dourado', 'Vermelho clássico'];
  let heroIndex = 0;
  let heroTimer = 0;

  const showHeroShot = index => {
    if (!heroShots.length) return;
    heroIndex = (index + heroShots.length) % heroShots.length;
    heroShots.forEach((shot, position) => shot.classList.toggle('active', position === heroIndex));
    heroControls.forEach((control, position) => {
      const active = position === heroIndex;
      control.classList.toggle('active', active);
      control.setAttribute('aria-pressed', String(active));
    });
    if (heroNumber) heroNumber.textContent = `${String(heroIndex + 1).padStart(2, '0')} / ${String(heroShots.length).padStart(2, '0')}`;
    if (heroLabel) heroLabel.textContent = heroLabels[heroIndex] || '';
  };

  const stopHeroReel = () => window.clearInterval(heroTimer);
  const startHeroReel = () => {
    stopHeroReel();
    if (!reduceMotion && heroShots.length > 1) heroTimer = window.setInterval(() => showHeroShot(heroIndex + 1), 4800);
  };
  heroControls.forEach(control => control.addEventListener('click', () => {
    showHeroShot(Number(control.dataset.heroGo));
    startHeroReel();
  }));
  heroVisual?.addEventListener('mouseenter', stopHeroReel);
  heroVisual?.addEventListener('mouseleave', startHeroReel);
  heroVisual?.addEventListener('focusin', stopHeroReel);
  heroVisual?.addEventListener('focusout', startHeroReel);
  showHeroShot(0);
  startHeroReel();

  const testimonialTrack = document.querySelector('[data-testimonial-track]');
  const testimonialSlides = [...document.querySelectorAll('.testimonial-slide')];
  const testimonialCount = document.querySelector('[data-testimonial-count]');
  const updateTestimonialCount = () => {
    if (!testimonialTrack || !testimonialSlides.length || !testimonialCount) return;
    const first = testimonialSlides[0];
    const gap = parseFloat(getComputedStyle(testimonialTrack).gap) || 0;
    const step = first.getBoundingClientRect().width + gap;
    const index = Math.min(testimonialSlides.length - 1, Math.max(0, Math.round(testimonialTrack.scrollLeft / step)));
    testimonialCount.textContent = `${String(index + 1).padStart(2, '0')} / ${String(testimonialSlides.length).padStart(2, '0')}`;
    testimonialSlides.forEach((slide, position) => {
      slide.classList.toggle('current', position === index);
      if (position !== index) slide.querySelector('video')?.pause();
    });
  };
  const moveTestimonials = direction => {
    if (!testimonialTrack || !testimonialSlides.length) return;
    const gap = parseFloat(getComputedStyle(testimonialTrack).gap) || 0;
    const distance = testimonialSlides[0].getBoundingClientRect().width + gap;
    testimonialTrack.scrollLeft += direction * distance;
    updateTestimonialCount();
  };
  document.querySelector('[data-testimonial-prev]')?.addEventListener('click', () => moveTestimonials(-1));
  document.querySelector('[data-testimonial-next]')?.addEventListener('click', () => moveTestimonials(1));
  testimonialTrack?.addEventListener('scroll', () => window.requestAnimationFrame(updateTestimonialCount), { passive: true });
  updateTestimonialCount();

  const ambientAudio = document.querySelector('#ambient-audio');
  const audioToggle = document.querySelector('[data-audio-toggle]');
  const audioLabel = document.querySelector('[data-audio-label]');
  const audioIcon = document.querySelector('[data-audio-icon]');

  const updateAudioControl = () => {
    if (!ambientAudio || !audioToggle || !audioLabel || !audioIcon) return;
    const playing = !ambientAudio.paused;
    audioToggle.setAttribute('aria-pressed', String(playing));
    audioToggle.classList.toggle('playing', playing);
    audioLabel.textContent = playing ? 'Pausar ambiente' : 'Ativar ambiente';
    audioIcon.textContent = playing ? 'Ⅱ' : '♫';
  };

  if (ambientAudio && audioToggle) {
    ambientAudio.volume = 0.09;
    audioToggle.addEventListener('click', async () => {
      if (ambientAudio.paused) {
        try {
          await ambientAudio.play();
        } catch (error) {
          console.warn('O navegador não permitiu iniciar o áudio.', error);
        }
      } else {
        ambientAudio.pause();
      }
      updateAudioControl();
    });
    ambientAudio.addEventListener('play', updateAudioControl);
    ambientAudio.addEventListener('pause', updateAudioControl);
    updateAudioControl();
  }

  document.querySelectorAll('video').forEach(video => {
    const frame = video.closest('.feet-video');
    video.addEventListener('play', () => {
      frame?.classList.add('is-playing');
      if (ambientAudio && !ambientAudio.paused) ambientAudio.pause();
    });
    const restoreFrame = () => frame?.classList.remove('is-playing');
    video.addEventListener('pause', restoreFrame);
    video.addEventListener('ended', restoreFrame);
  });

  if ('IntersectionObserver' in window && !reduceMotion) {
    revealItems.forEach(item => {
      if (item.getBoundingClientRect().top < window.innerHeight * .94) item.classList.add('visible');
    });
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -7% 0px', threshold: 0.08 });
    revealItems.filter(item => !item.classList.contains('visible')).forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add('visible'));
  }
})();
