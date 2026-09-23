import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const publicPages = ['index.html', 'studio.html', 'projects.html', 'en/index.html', 'en/studio.html', 'en/projects.html'];
const indexablePages = [...publicPages];
const canonicalByPage = new Map([
  ['index.html', 'https://voidstudio.top/'],
  ['studio.html', 'https://voidstudio.top/studio.html'],
  ['projects.html', 'https://voidstudio.top/projects.html'],
  ['en/index.html', 'https://voidstudio.top/en/'],
  ['en/studio.html', 'https://voidstudio.top/en/studio.html'],
  ['en/projects.html', 'https://voidstudio.top/en/projects.html']
]);
const errors = [];
const warnings = [];

const exists = (relativePath) => fs.existsSync(path.join(root, relativePath));
const cleanLocalPath = (value) => {
  if (!value || /^(?:https?:|mailto:|tel:|data:|javascript:|#)/i.test(value)) return null;
  if (value.startsWith('/_vercel/')) return null;
  return decodeURIComponent(value.split('#')[0].split('?')[0]).replace(/^\.\//, '');
};

for (const page of publicPages) {
  if (!exists(page)) {
    errors.push(`Не найдена публичная страница: ${page}`);
    continue;
  }

  const html = fs.readFileSync(path.join(root, page), 'utf8');
  const seenIds = new Set();
  for (const match of html.matchAll(/\sid=["']([^"']+)["']/g)) {
    if (seenIds.has(match[1])) errors.push(`${page}: повторяется id="${match[1]}"`);
    seenIds.add(match[1]);
  }

  for (const match of html.matchAll(/\s(?:href|src)=["']([^"']+)["']/g)) {
    const localPath = cleanLocalPath(match[1]);
    if (!localPath) continue;
    const target = localPath.startsWith('/')
      ? localPath.slice(1)
      : path.normalize(path.join(path.dirname(page), localPath));
    if (!exists(target)) errors.push(`${page}: битая локальная ссылка ${match[1]}`);
  }

  if (indexablePages.includes(page) && /name=["']robots["'][^>]+noindex/i.test(html)) {
    warnings.push(`${page}: поисковая индексация отключена`);
  }

  if (indexablePages.includes(page)) {
    const canonical = canonicalByPage.get(page);
    if (!html.includes(`<link rel="canonical" href="${canonical}">`)) errors.push(`${page}: неверный canonical`);
    if (!/<title>[^<]{15,}[^<]*<\/title>/.test(html)) errors.push(`${page}: отсутствует содержательный title`);
    if (!/<meta name="description" content="[^\"]{50,}"/.test(html)) errors.push(`${page}: отсутствует содержательный meta description`);
    if ((html.match(/<h1(?:\s|>)/g) || []).length !== 1) errors.push(`${page}: должен быть ровно один H1 в исходном HTML`);
    for (const property of ['og:title', 'og:description', 'og:url', 'og:image']) {
      if (!html.includes(`property="${property}"`)) errors.push(`${page}: отсутствует ${property}`);
    }
    if (/name=["']keywords["']/i.test(html)) errors.push(`${page}: meta keywords не используется Google`);
    for (const match of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
      try { JSON.parse(match[1]); } catch { errors.push(`${page}: невалидный JSON-LD`); }
    }
  }
}

if (!exists('robots.txt')) errors.push('Не найден robots.txt');
if (!exists('sitemap.xml')) errors.push('Не найден sitemap.xml');
if (exists('robots.txt') && !fs.readFileSync(path.join(root, 'robots.txt'), 'utf8').includes('https://voidstudio.top/sitemap.xml')) {
  errors.push('robots.txt: не указана карта сайта');
}
if (exists('sitemap.xml')) {
  const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
  for (const canonical of canonicalByPage.values()) {
    if (!sitemap.includes(`<loc>${canonical}</loc>`)) errors.push(`sitemap.xml: нет ${canonical}`);
  }
}

const gallerySource = fs.readFileSync(path.join(root, 'assets/gallery-data.js'), 'utf8');
const context = { URL, location: { href: 'http://localhost/' } };
vm.createContext(context);
vm.runInContext(`${gallerySource}\n;globalThis.__galleryWorks = galleryWorks; globalThis.__suggestedGalleryIds = suggestedGalleryIds;`, context);
const works = context.__galleryWorks;
const ids = new Set();

for (const work of works) {
  if (ids.has(work.id)) errors.push(`gallery-data: повторяется id ${work.id}`);
  ids.add(work.id);
  if (!work.title?.trim()) errors.push(`gallery-data: у работы ${work.id} нет названия`);
  if (!work.description?.trim()) errors.push(`gallery-data: у работы ${work.id} нет описания`);
  if (!work.role?.trim()) errors.push(`gallery-data: у работы ${work.id} нет подписи о формате`);

  const mediaPaths = [work.src, work.poster, ...(work.frames || []).map((frame) => frame.src)].filter(Boolean);
  for (const mediaPath of mediaPaths) {
    if (!exists(mediaPath)) errors.push(`gallery-data: не найден файл ${mediaPath}`);
    const basename = path.basename(mediaPath, path.extname(mediaPath));
    if (/^\d+$/.test(basename)) errors.push(`gallery-data: числовое имя файла ${mediaPath}`);
    if (!/^[a-z0-9][a-z0-9._-]*$/i.test(path.basename(mediaPath))) {
      errors.push(`gallery-data: небезопасное имя файла ${mediaPath}`);
    }
  }
}

for (const id of context.__suggestedGalleryIds) {
  if (!ids.has(id)) {
    errors.push(`gallery-data: в подборке указан отсутствующий id ${id}`);
    continue;
  }
  const work = works.find((item) => item.id === id);
  const source = work.poster || work.src;
  const thumbnail = source.replace(/\/([^/.]+)\.[^/.]+$/, '/thumbs/$1.webp');
  if (!exists(thumbnail)) errors.push(`gallery-data: нет миниатюры ${thumbnail}`);
}

if (exists('site-preview.html')) warnings.push('Временное имя публичной страницы: site-preview.html');
if (exists('assets/gallery/after-celebration.mp4') || exists('assets/gallery/after-celebration-poster.webp')) {
  warnings.push('Остались файлы удалённой работы «После праздника»');
}
if (exists('assets/gallery/incoming')) warnings.push('В публикацию попадает папка с тяжёлыми исходниками assets/gallery/incoming');

if (errors.length) {
  console.error(`ОШИБКИ (${errors.length})`);
  for (const item of errors) console.error(`- ${item}`);
}
if (warnings.length) {
  console.warn(`ПРЕДУПРЕЖДЕНИЯ (${warnings.length})`);
  for (const item of warnings) console.warn(`- ${item}`);
}

if (!errors.length && !warnings.length) console.log('OK: публичные страницы, ссылки и галерея прошли аудит.');
process.exitCode = errors.length ? 1 : 0;
