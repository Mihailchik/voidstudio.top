(() => {
  const mediaHost = 'http://127.0.0.1:4191/';
  const initialSelection = [1, 37, 38, 63];
  const saved = localStorage.getItem('void-studio-site-selection-v2');
  let savedSelection = initialSelection;
  try {
    if (saved) savedSelection = JSON.parse(saved);
  } catch (_) {
    localStorage.removeItem('void-studio-site-selection-v2');
  }
  const selected = new Set(savedSelection);
  const grid = document.getElementById('catalog-grid');
  const template = document.getElementById('media-card-template');
  const search = document.getElementById('catalog-search');
  const count = document.getElementById('selected-count');
  const filterCount = document.getElementById('selected-filter-count');
  const currentHomepage = new Set(initialSelection);
  let filter = 'all';

  const mediaUrl = path => `${mediaHost}${path}`;
  const persist = () => localStorage.setItem('void-studio-site-selection-v2', JSON.stringify([...selected].sort((a,b) => a-b)));

  function updateCount() {
    count.textContent = selected.size;
    filterCount.textContent = selected.size;
  }

  function createCard(item) {
    const card = template.content.firstElementChild.cloneNode(true);
    card.dataset.id = item.id;
    card.dataset.kind = item.kind;
    card.dataset.search = `${item.id} ${item.title}`.toLocaleLowerCase('ru');
    const preview = card.querySelector('.media-preview');
    if (item.kind === 'image') {
      const image = new Image();
      image.loading = 'lazy';
      image.alt = item.title;
      image.src = mediaUrl(item.path);
      preview.append(image);
    } else {
      const video = document.createElement('video');
      video.dataset.src = mediaUrl(item.path);
      if (item.poster) video.poster = mediaUrl(item.poster);
      video.controls = true;
      video.muted = true;
      video.loop = true;
      video.preload = 'metadata';
      video.setAttribute('playsinline', '');
      video.setAttribute('aria-label', item.title);
      preview.append(video);
      const mark = document.createElement('span');
      mark.className = 'video-mark';
      mark.textContent = 'VIDEO';
      preview.append(mark);
    }
    if (currentHomepage.has(item.id)) {
      const mark = document.createElement('span');
      mark.className = 'current-mark';
      mark.textContent = 'СЕЙЧАС НА ГЛАВНОЙ';
      preview.append(mark);
    }
    card.querySelector('.media-meta').textContent = `ID ${String(item.id).padStart(3,'0')} · ${item.kind === 'video' ? 'видео' : 'изображение'}`;
    card.querySelector('h2').textContent = item.title;
    const checkbox = card.querySelector('input');
    checkbox.checked = selected.has(item.id);
    card.classList.toggle('is-selected', checkbox.checked);
    checkbox.addEventListener('change', () => {
      if (checkbox.checked) selected.add(item.id); else selected.delete(item.id);
      card.classList.toggle('is-selected', checkbox.checked);
      persist();
      updateCount();
      applyFilter();
    });
    return card;
  }

  mediaCatalog.forEach(item => grid.append(createCard(item)));

  const videoObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const video = entry.target;
      if (!video.src) video.src = video.dataset.src;
      videoObserver.unobserve(video);
    });
  }, {rootMargin: '500px 0px'});
  grid.querySelectorAll('video').forEach(video => videoObserver.observe(video));

  function applyFilter() {
    const query = search.value.trim().toLocaleLowerCase('ru');
    let visible = 0;
    grid.querySelectorAll('.media-card').forEach(card => {
      const typeMatches = filter === 'all' || card.dataset.kind === filter || (filter === 'selected' && selected.has(Number(card.dataset.id)));
      const searchMatches = !query || card.dataset.search.includes(query);
      card.hidden = !(typeMatches && searchMatches);
      if (!card.hidden) visible++;
      const video = card.querySelector('video');
      if (video && card.hidden) video.pause();
    });
    grid.querySelector('.empty')?.remove();
    if (!visible) {
      const empty = document.createElement('p');
      empty.className = 'empty';
      empty.textContent = 'Ничего не найдено';
      grid.append(empty);
    }
  }

  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    applyFilter();
  }));
  search.addEventListener('input', applyFilter);

  document.getElementById('copy-selection').addEventListener('click', async event => {
    const lines = mediaCatalog.filter(item => selected.has(item.id)).map(item => `${String(item.id).padStart(3,'0')} · ${item.kind === 'video' ? 'Видео' : 'Изображение'} · ${item.title}`);
    await navigator.clipboard.writeText(lines.join('\n'));
    const button = event.currentTarget;
    const previous = button.textContent;
    button.textContent = 'Скопировано';
    setTimeout(() => { button.textContent = previous; }, 1400);
  });

  updateCount();
})();
