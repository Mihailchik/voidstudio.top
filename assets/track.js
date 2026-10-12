// Нажатия на «Написать в Telegram» уходят в Google Analytics событием contact_click:
// по нему видно, с какой страницы приходят обращения.
document.addEventListener('click',e=>{
  const link=e.target.closest&&e.target.closest('a[href^="https://t.me/LuchkoOlga"]');
  if(!link||typeof gtag!=='function')return;
  gtag('event','contact_click',{method:'telegram',link_text:(link.textContent||'').trim().slice(0,60),page_path:location.pathname});
});
