// Видео на странице проекта: сначала показывается обложка, сам файл
// подтягивается и запускается, только когда блок попал на экран.
// Так страница открывается мгновенно, а трафик тратится лишь на тех,
// кто до ролика доскроллил.
//
// Разметка: <video poster="..." muted loop playsinline preload="none" controls>
// Ничего настраивать не надо, скрипт сам находит такие видео в .project-reel.
(() => {
  'use strict';

  // Ищем по месту в разметке, а не по атрибуту preload: скрипт сам меняет его
  // на auto, и выборка по атрибуту переставала находить своё же видео.
  const reels = document.querySelectorAll('.hero-media video, .project-reel video');
  if (!reels.length) return;

  // Если человек выключил анимацию в системе, ролик не запускаем сам:
  // обложка и кнопка воспроизведения остаются на месте.
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Экономный режим и мобильный интернет: не тянем видео без спроса.
  const net = navigator.connection;
  const stingy = net && (net.saveData || /^([23]g|slow-2g)$/.test(net.effectiveType || ''));

  if (calm || stingy || !('IntersectionObserver' in window)) return;

  const watcher = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const video = entry.target;
      if (!entry.isIntersecting) {
        if (!video.paused) video.pause();
        continue;
      }
      if (!video.dataset.started) {
        video.dataset.started = 'yes';
        video.preload = 'auto';
        // Сразу после load() данных ещё нет, и play() в этот момент срывается.
        // Поэтому ждём первый читаемый кадр и только тогда запускаем.
        video.addEventListener('loadeddata', () => start(video), { once: true });
        video.load();
        continue;
      }
      start(video);
    }
  }, { threshold: 0.35 });

  // play() возвращает обещание и может отказать: политика автозапуска,
  // вкладка в фоне, экономия батареи. Отказ не ломает страницу —
  // человек нажмёт кнопку сам.
  function start(video) {
    if (video.paused) video.play().catch(() => {});
  }

  reels.forEach((video) => watcher.observe(video));

  // Если страницу открыли в фоновой вкладке, браузер не считает её видимой и
  // наблюдатель молчит. Когда человек переключится на вкладку, догоняем.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    reels.forEach((video) => {
      const box = video.getBoundingClientRect();
      const onScreen = box.top < innerHeight && box.bottom > 0;
      if (!onScreen) return;
      if (!video.dataset.started) {
        video.dataset.started = 'yes';
        video.preload = 'auto';
        video.addEventListener('loadeddata', () => start(video), { once: true });
        video.load();
        return;
      }
      start(video);
    });
  });
})();
