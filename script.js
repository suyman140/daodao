(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const audio = $('#background-music');
  const musicButton = $('#music-toggle');
  const musicLabel = $('#music-label');
  const player = $('.music-player');
  let musicHasBeenRequested = false;
  let musicPending = false;
  let playbackRequest = 0;
  audio.volume = 0.4;

  function updateMusic() {
    const playing = !audio.paused;
    player.classList.toggle('playing', playing);
    musicButton.setAttribute('aria-pressed', String(playing));
    musicButton.setAttribute('aria-label', playing ? 'Tạm dừng nhạc Một chút nắng' : 'Bật nhạc Một chút nắng');
    musicLabel.textContent = playing ? 'Một chút nắng ♫' : 'Bật nhạc vui';
  }

  async function startMusic() {
    if (musicPending || !audio.paused) return;
    musicHasBeenRequested = true;
    musicPending = true;
    const request = ++playbackRequest;
    musicLabel.textContent = 'Đang mở nhạc…';
    try { await audio.play(); }
    catch {
      if (request === playbackRequest) {
        updateMusic();
        musicLabel.textContent = 'Chạm để thử lại';
      }
    }
    finally { if (request === playbackRequest) musicPending = false; }
  }
  musicButton.addEventListener('click', () => {
    musicHasBeenRequested = true;
    if (musicPending || !audio.paused) {
      playbackRequest += 1;
      musicPending = false;
      audio.pause();
      updateMusic();
    } else startMusic();
  });
  audio.addEventListener('play', updateMusic);
  audio.addEventListener('pause', updateMusic);
  audio.addEventListener('error', () => {
    playbackRequest += 1;
    musicPending = false;
    updateMusic();
    musicLabel.textContent = 'Chạm để thử lại';
  });
  $('#music-volume').addEventListener('input', (event) => { audio.volume = Number(event.target.value); });
  $('#volume-toggle').addEventListener('click', () => {
    const panel = $('#volume-panel');
    panel.hidden = !panel.hidden;
    $('#volume-toggle').setAttribute('aria-expanded', String(!panel.hidden));
  });
  document.addEventListener('click', (event) => {
    if (!player.contains(event.target)) {
      $('#volume-panel').hidden = true;
      $('#volume-toggle').setAttribute('aria-expanded', 'false');
    }
  });
  $('#open-gift').addEventListener('click', () => { if (!musicHasBeenRequested) startMusic(); });

  const petalLayer = $('#petal-layer');
  let petalTimer;
  function flowers(count = 65) {
    if (reducedMotion.matches) return;
    clearTimeout(petalTimer);
    petalLayer.replaceChildren();
    const fragment = document.createDocumentFragment();
    const colors = ['#e76551', '#f1c850', '#ac96c4', '#ed9b88', '#72926a', '#f1b950', '#fff6d7'];
    for (let i = 0; i < count; i += 1) {
      const petal = document.createElement('span');
      petal.className = 'petal';
      petal.style.setProperty('--x', `${Math.random() * 100}%`);
      petal.style.setProperty('--y', `${-12 - Math.random() * 10}%`);
      petal.style.setProperty('--size', `${8 + Math.random() * 13}px`);
      petal.style.setProperty('--petal-color', colors[i % colors.length]);
      petal.style.setProperty('--duration', `${3.2 + Math.random() * 2.7}s`);
      petal.style.setProperty('--delay', `${Math.random() * 1.3}s`);
      petal.style.setProperty('--drift', `${(Math.random() - 0.5) * 320}px`);
      petal.style.setProperty('--rotation', `${180 + Math.random() * 640}deg`);
      fragment.appendChild(petal);
    }
    petalLayer.appendChild(fragment);
    petalTimer = setTimeout(() => petalLayer.replaceChildren(), 7500);
  }

  const bloomMessages = ['Hoa đã tới tay em. Mong em hôm nay thật vui! ✿', 'Thêm một chút nắng, thêm một chút yêu đời. ☀', 'Một bó nữa nè. Niềm vui thì không giới hạn! ✿'];
  let blooms = 0;
  let bloomTimer;
  $('#bloom-button').addEventListener('click', () => {
    const stage = $('#bouquet-stage');
    clearTimeout(bloomTimer);
    stage.classList.remove('blooming');
    void stage.offsetWidth;
    stage.classList.add('blooming');
    $('#flower-status').textContent = bloomMessages[blooms % bloomMessages.length];
    blooms += 1;
    $('#bloom-button').innerHTML = 'Thêm một lần hoa nở <span aria-hidden="true">✿</span>';
    flowers();
    if (!musicHasBeenRequested) startMusic();
    bloomTimer = setTimeout(() => stage.classList.remove('blooming'), 1400);
  });
  $('#letter-card').addEventListener('toggle', (event) => { if (event.target.open) flowers(30); });

  const wishes = [
    'Chúc em hôm nay có đồ ăn ngon, chuyện vui và một giấc ngủ thật ngon. ☀',
    'Mong điều em đang cố gắng sẽ sớm nở hoa. Cứ từ từ, em nhé. ✿',
    'Gửi em một ngày nhẹ tênh: bớt lo một chút, cười nhiều một chút.',
    'Một lời nhắc nhỏ: em xứng đáng được quý mến và trân trọng mỗi ngày. ♡',
    'Chúc em đủ tự tin để làm điều mình thích, đủ thảnh thơi để tận hưởng điều mình có.'
  ];
  let wishIndex = 0;
  $('#more-joy').addEventListener('click', () => {
    $('#joy-message').textContent = wishes[wishIndex % wishes.length];
    wishIndex += 1;
    flowers(45);
  });

  const photoLinks = Array.from(document.querySelectorAll('[data-photo]'));
  const photos = photoLinks.filter((link, i) => photoLinks.findIndex((other) => other.href === link.href) === i);
  const dialog = $('#photo-dialog');
  let activePhoto = 0;
  let lastPhotoTrigger;
  function showPhoto(index) {
    activePhoto = (index + photos.length) % photos.length;
    const link = photos[activePhoto];
    const image = link.querySelector('img');
    $('#lightbox-image').src = link.href;
    $('#lightbox-image').alt = image.alt;
    $('#lightbox-caption').textContent = link.dataset.caption;
    $('#lightbox-count').textContent = `${String(activePhoto + 1).padStart(2, '0')} / ${String(photos.length).padStart(2, '0')}`;
  }
  photoLinks.forEach((link) => link.addEventListener('click', (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    lastPhotoTrigger = link;
    showPhoto(photos.findIndex((photo) => photo.href === link.href));
    dialog.showModal();
    document.body.classList.add('modal-open');
    $('#close-photo').focus();
  }));
  $('#close-photo').addEventListener('click', () => dialog.close());
  $('#previous-photo').addEventListener('click', () => showPhoto(activePhoto - 1));
  $('#next-photo').addEventListener('click', () => showPhoto(activePhoto + 1));
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    lastPhotoTrigger?.focus();
    $('#lightbox-image').removeAttribute('src');
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      $('#volume-panel').hidden = true;
      $('#volume-toggle').setAttribute('aria-expanded', 'false');
    }
    if (!dialog.open) return;
    if (event.key === 'ArrowRight') { event.preventDefault(); showPhoto(activePhoto + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); showPhoto(activePhoto - 1); }
  });

  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    }), { threshold: 0.08 });
    document.querySelectorAll('.bouquet-copy, .section-heading, .letter-intro, .closing').forEach((element) => {
      element.classList.add('reveal-ready');
      observer.observe(element);
    });
  }
})();
