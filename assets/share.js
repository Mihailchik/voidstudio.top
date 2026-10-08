// Кнопка «Поделиться»: плавающая кнопка в углу и меню выбора площадки.
// Самодостаточный файл: стили внутри, зависимостей нет. Переносится в любой
// проект одной строкой <script src="share.js" defer></script>.
//
// Настройка — необязательна. Что можно задать до подключения:
//   window.shareConfig = {
//     url:      'https://…',   // по умолчанию — canonical страницы или её адрес
//     title:    '…',           // по умолчанию — <title>
//     text:     '…',           // по умолчанию — meta description
//     networks: ['telegram', …],
//     position: 'bottom-right' // 'bottom-left' | 'top-right' | 'top-left'
//   };
//
// Про телефон: там открывается СИСТЕМНАЯ шторка. Она не сообщает, куда человек
// отправил ссылку, поэтому в статистику уходит просто «system». Разбивка по
// площадкам есть только у своего меню, то есть в основном с компьютера.
(() => {
  'use strict';

  const cfg = Object.assign({ position: 'bottom-right' }, window.shareConfig || {});
  const lang = (document.documentElement.lang || 'ru').startsWith('ru') ? 'ru' : 'en';

  const canonical = document.querySelector('link[rel=canonical]');
  const url = cfg.url || (canonical && canonical.href) || location.href.split('#')[0];
  const title = cfg.title || document.title;
  const descr = document.querySelector('meta[name=description]');
  const text = cfg.text || (descr && descr.content) || '';

  const words = {
    ru: { open: 'Поделиться', heading: 'Поделиться', cancel: 'Отмена',
          copy: 'Скопировать ссылку', copied: 'Ссылка скопирована',
          hint: 'Для Instagram и YouTube скопируйте ссылку: вставить её можно в сторис или описание.' },
    en: { open: 'Share', heading: 'Share', cancel: 'Cancel',
          copy: 'Copy link', copied: 'Link copied',
          hint: 'Instagram and YouTube take no share links — copy the link and paste it into a story or a description.' },
  }[lang];

  // Площадки, у которых есть веб-адрес для публикации. Instagram и YouTube
  // такого адреса не дают вовсе, поэтому их здесь нет — для них «скопировать».
  const E = encodeURIComponent;
  const catalogue = {
    telegram: { name: 'Telegram', colour: '#2aabee',
      link: () => `https://t.me/share/url?url=${E(url)}&text=${E(title)}`,
      icon: '<path d="M21.7 4.3 2.9 11.5c-1 .4-1 1.1 0 1.4l4.7 1.5 1.8 5.5c.2.6.5.7 1 .3l2.6-2.1 4.5 3.3c.8.5 1.3.2 1.6-.8l3-14c.3-1.2-.4-1.7-1.4-1.3zM8.6 14.1l9.6-6c.4-.3.8-.1.5.2l-8 7.2-.3 3.3-1.8-4.7z"/>' },
    whatsapp: { name: 'WhatsApp', colour: '#25d366',
      link: () => `https://wa.me/?text=${E(title + ' ' + url)}`,
      icon: '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 2a8 8 0 1 1-4.1 14.8l-.4-.2-2.6.7.7-2.5-.2-.4A8 8 0 0 1 12 4zm-3 4c-.3 0-.6.1-.9.4-.3.4-1 1-1 2.3s1 2.7 1.2 2.9c.1.2 2 3.1 4.9 4.2 2.4.9 2.9.8 3.4.7.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4l-.9-.5-1.5-.7c-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1-.2-.1-1.1-.4-2-1.3-.7-.6-1.2-1.4-1.3-1.7-.1-.2 0-.3.1-.4l.4-.5.3-.5v-.5l-.7-1.7c-.2-.4-.4-.4-.5-.4z"/>' },
    x: { name: 'X', colour: '#111',
      link: () => `https://twitter.com/intent/tweet?url=${E(url)}&text=${E(title)}`,
      icon: '<path d="M17.7 3h3.3l-7.2 8.3L22 21h-6.4l-5-6.3L4.8 21H1.5l7.7-8.9L2 3h6.6l4.5 5.9zm-1.2 16h1.8L7.6 4.8H5.6z"/>' },
    vk: { name: 'VK', colour: '#07f',
      link: () => `https://vk.com/share.php?url=${E(url)}&title=${E(title)}`,
      icon: '<path d="M12.8 16.6c-5.4 0-8.8-3.8-9-10h2.8c.1 4.6 2.2 6.6 3.8 7V6.6h2.6v3.9c1.6-.2 3.3-2 3.9-3.9h2.6c-.5 2.3-2.2 4.1-3.4 4.8 1.2.6 3.2 2.2 3.9 5.2h-2.9c-.6-1.8-2.1-3.2-4.1-3.5v3.5z"/>' },
    facebook: { name: 'Facebook', colour: '#1877f2',
      link: () => `https://www.facebook.com/sharer/sharer.php?u=${E(url)}`,
      icon: '<path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12z"/>' },
    reddit: { name: 'Reddit', colour: '#ff4500',
      link: () => `https://www.reddit.com/submit?url=${E(url)}&title=${E(title)}`,
      icon: '<path d="M22 12a2 2 0 0 0-3.4-1.4c-1.4-.9-3.2-1.5-5.2-1.6l1-3.3 2.6.6a1.7 1.7 0 1 0 .2-1.3l-3-.7c-.3-.1-.5.1-.6.3l-1.2 4.4c-2 .1-3.9.7-5.3 1.6A2 2 0 1 0 4 15.2v.5c0 2.9 3.6 5.3 8 5.3s8-2.4 8-5.3v-.5c1.2-.5 2-1.7 2-3zM8.5 13.4a1.4 1.4 0 1 1 1.4 1.4 1.4 1.4 0 0 1-1.4-1.4zm7.6 4.3c-1 1-2.6 1.4-4.1 1.4s-3.1-.4-4.1-1.4a.5.5 0 0 1 .7-.7c.8.8 2.1 1.1 3.4 1.1s2.6-.3 3.4-1.1a.5.5 0 0 1 .7.7zm-.3-2.9a1.4 1.4 0 1 1 1.4-1.4 1.4 1.4 0 0 1-1.4 1.4z"/>' },
    linkedin: { name: 'LinkedIn', colour: '#0a66c2',
      link: () => `https://www.linkedin.com/sharing/share-offsite/?url=${E(url)}`,
      icon: '<path d="M20.4 3H3.6A.6.6 0 0 0 3 3.6v16.8c0 .3.3.6.6.6h16.8c.3 0 .6-.3.6-.6V3.6a.6.6 0 0 0-.6-.6zM8.3 18.3H5.6V9.8h2.7zM6.9 8.6a1.6 1.6 0 1 1 1.6-1.6 1.6 1.6 0 0 1-1.6 1.6zm11.4 9.7h-2.7v-4.1c0-1 0-2.3-1.4-2.3s-1.6 1.1-1.6 2.2v4.2h-2.7V9.8h2.6V11a2.9 2.9 0 0 1 2.6-1.4c2.7 0 3.2 1.8 3.2 4.1z"/>' },
    email: { name: 'Email', colour: '#5b6b5a',
      link: () => `mailto:?subject=${E(title)}&body=${E(text ? text + '\n\n' + url : url)}`,
      icon: '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 7.2 8-4.8V6H4v.4zM4 8.7V18h16V8.7l-7.5 4.5a1 1 0 0 1-1 0z"/>' },
  };

  const order = cfg.networks || ['telegram', 'whatsapp', 'x', 'vk', 'facebook', 'reddit', 'linkedin', 'email'];
  const networks = order.map(k => catalogue[k]).filter(Boolean);

  /* ── статистика ─────────────────────────────────────────────────────── */

  function track(where) {
    try { window.gtag && gtag('event', 'share', { method: where, content_type: 'page', item_id: url }); } catch {}
    try { window.va && va('event', { name: 'share', data: { network: where, page: location.pathname } }); } catch {}
    document.dispatchEvent(new CustomEvent('share:used', { detail: { network: where, url } }));
  }

  /* ── разметка ───────────────────────────────────────────────────────── */

  const style = document.createElement('style');
  style.textContent = `
.share-button{position:fixed;z-index:60;width:46px;height:46px;border-radius:50%;
  border:1px solid rgba(23,25,23,.18);background:#f6f6f2;color:#171917;cursor:pointer;
  display:grid;place-items:center;padding:0;box-shadow:0 6px 20px rgba(20,25,20,.12);
  transition:transform .2s,box-shadow .2s,background .2s}
.share-button svg{width:19px;height:19px;fill:currentColor}
.share-button[data-pos$="-right"]{right:22px}
.share-button[data-pos$="-left"]{left:22px}
.share-button[data-pos^="bottom"]{bottom:22px}
.share-button[data-pos^="top"]{top:84px}
@media(hover:hover){.share-button:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(20,25,20,.18)}}
.share-button:active{transform:scale(.95)}

.share-sheet{border:0;padding:0;margin:0;inset:0;background:none;max-width:100vw;
  max-height:none;width:auto;height:auto;color:#171917}
.share-sheet::backdrop{background:rgba(18,20,18,.28)}
.share-sheet .wrap{height:100%;position:relative}

/* Список выезжает от самой кнопки, а не из середины экрана. */
.share-list{position:absolute;width:268px;background:#fbfbf8;border-radius:14px;
  border:1px solid rgba(23,25,23,.1);box-shadow:0 16px 44px rgba(16,20,16,.22);
  padding:6px;overflow:hidden;animation:share-in .18s ease-out}
@keyframes share-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.share-list{animation:none}}
.share-list a,.share-list button{display:flex;align-items:center;gap:11px;width:100%;
  padding:9px 10px;border:0;border-radius:9px;background:none;font:inherit;font-size:14px;
  color:inherit;text-decoration:none;cursor:pointer;text-align:left;line-height:1.2}
.share-list i{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;
  color:#fff;flex:0 0 auto}
.share-list svg{width:15px;height:15px;fill:currentColor}
.share-list .divider{height:1px;background:rgba(23,25,23,.09);margin:6px 8px}
.share-list .copy i{background:#5b6b5a}
@media(hover:hover){.share-list a:hover,.share-list button:hover{background:rgba(23,25,23,.06)}}
.share-list a:active,.share-list button:active{background:rgba(23,25,23,.1)}
.share-note{margin:4px 10px 6px;font-size:11px;line-height:1.4;color:#8a8f88}

/* На телефоне тот же список, но снизу во всю ширину. */
@media(max-width:640px){
  .share-list{position:fixed;left:10px;right:10px;top:auto!important;width:auto;
    bottom:max(10px,env(safe-area-inset-bottom));border-radius:16px;padding:7px}
  .share-list a,.share-list button{padding:12px 11px;font-size:15px}
}
.share-toast{position:fixed;left:50%;bottom:30px;transform:translateX(-50%);z-index:70;
  background:#171917;color:#f6f6f2;font-size:13px;padding:11px 17px;border-radius:30px;
  box-shadow:0 10px 30px rgba(16,20,16,.3)}
@media(max-width:480px){.share-button{width:42px;height:42px}
  .share-button[data-pos$="-right"]{right:16px}.share-button[data-pos$="-left"]{left:16px}
  .share-button[data-pos^="bottom"]{bottom:16px}}`;
  document.head.append(style);

  const svg = d => `<svg viewBox="0 0 24 24" aria-hidden="true">${d}</svg>`;

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'share-button';
  button.dataset.pos = cfg.position;
  button.setAttribute('aria-label', words.open);
  // Симметричный значок: стрелка вверх из лотка. Центр рисунка совпадает с
  // центром холста 24×24, поэтому в круглой кнопке он не кажется смещённым.
  button.innerHTML = svg('<path d="M12 2.5a1 1 0 0 1 .7.3l3.5 3.5a1 1 0 0 1-1.4 1.4L13 5.9V15a1 1 0 0 1-2 0V5.9L9.2 7.7a1 1 0 0 1-1.4-1.4l3.5-3.5a1 1 0 0 1 .7-.3z"/><path d="M5 10a1 1 0 0 1 1 1v8h12v-8a1 1 0 1 1 2 0v8.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 19.5V11a1 1 0 0 1 1-1z"/>');
  document.body.append(button);

  const sheet = document.createElement('dialog');
  sheet.className = 'share-sheet';
  sheet.innerHTML = `<div class="wrap"><div class="share-list" role="menu">
    ${networks.map(n => `
      <a role="menuitem" href="${n.link()}" target="_blank" rel="noopener" data-net="${n.name.toLowerCase()}">
        <i style="background:${n.colour}">${svg(n.icon)}</i><span>${n.name}</span>
      </a>`).join('')}
    <div class="divider"></div>
    <button class="copy" type="button" role="menuitem">
      <i>${svg('<path d="M9 2h9a2 2 0 0 1 2 2v9h-2V4H9zM5 6h9a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2zm0 2v12h9V8z"/>')}</i>
      <span>${words.copy}</span>
    </button>
    <p class="share-note">${words.hint}</p>
  </div></div>`;
  document.body.append(sheet);

  /* ── поведение ──────────────────────────────────────────────────────── */

  button.addEventListener('click', async () => {
    // На телефоне отдаём системную шторку: там есть Instagram, YouTube и всё
    // остальное, что у человека установлено. Своё меню такого дать не может.
    if (navigator.share && matchMedia('(pointer:coarse)').matches) {
      try {
        await navigator.share({ title, text, url });
        track('system');
        return;
      } catch (e) {
        if (e && e.name === 'AbortError') { track('cancelled'); return; }
      }
    }
    placeList();
    sheet.showModal();
  });

  // Список встаёт рядом с кнопкой: над ней или под ней — смотря где больше места.
  function placeList() {
    const list = sheet.querySelector('.share-list');
    list.style.cssText = '';
    if (matchMedia('(max-width:640px)').matches) return;  // там он прижат к низу
    const b = button.getBoundingClientRect();
    const gap = 10;
    list.style.visibility = 'hidden';
    sheet.show();
    const h = list.offsetHeight, w = list.offsetWidth;
    sheet.close();
    list.style.visibility = '';
    const below = window.innerHeight - b.bottom - gap;
    list.style.top = (below > h || b.top < h + gap
      ? Math.min(b.bottom + gap, window.innerHeight - h - gap)
      : b.top - h - gap) + 'px';
    const right = cfg.position.endsWith('right');
    list.style.left = Math.max(gap, Math.min(
      right ? b.right - w : b.left, window.innerWidth - w - gap)) + 'px';
  }

  sheet.querySelectorAll('.share-list a').forEach(a => {
    a.addEventListener('click', () => { track(a.dataset.net); sheet.close(); });
  });

  sheet.querySelector('.share-list .copy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(url);
    } catch {
      const area = document.createElement('textarea');
      area.value = url; area.style.position = 'fixed'; area.style.opacity = '0';
      document.body.append(area); area.select();
      try { document.execCommand('copy'); } catch {}
      area.remove();
    }
    track('copy');
    sheet.close();
    toast(words.copied);
  });

  // Клик по тёмному полю вокруг панели тоже закрывает.
  sheet.addEventListener('click', e => {
    if (!e.target.closest('.share-list')) sheet.close();
  });

  function toast(message) {
    const el = document.createElement('div');
    el.className = 'share-toast';
    el.setAttribute('role', 'status');
    el.textContent = message;
    document.body.append(el);
    setTimeout(() => el.remove(), 2400);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
})();
