// Void Studio's continuous index → expanded ribbon.
function createFilmstrip(works, { reduced = false } = {}) {
  const stage = document.getElementById('film-stage');
  const section = document.getElementById('film');
  const track = document.getElementById('film-track');
  const ruler = document.getElementById('ruler');
  const heading = document.getElementById('film-title');
  const controls = document.querySelector('.film-detail-controls');
  const fitButton = document.getElementById('film-fit');
  const projectCopy = document.createElement('aside');
  projectCopy.className = 'film-project-copy';
  projectCopy.setAttribute('aria-live', 'polite');
  projectCopy.innerHTML = '<p class="film-project-kind"></p><p class="film-project-description"></p><p class="film-project-role"></p><a class="film-project-link" target="_blank" rel="noopener"></a>';
  const projectKind = projectCopy.querySelector('.film-project-kind');
  const projectDescription = projectCopy.querySelector('.film-project-description');
  const projectRole = projectCopy.querySelector('.film-project-role');
  const projectLink = projectCopy.querySelector('.film-project-link');
  const frameRail = document.createElement('div');
  frameRail.className = 'film-frame-rail';
  frameRail.setAttribute('aria-label', 'Кадры проекта');
  frameRail.hidden = true;
  frameRail.inert = true;
  projectCopy.setAttribute('aria-hidden', 'true');
  section.append(projectCopy, frameRail);
  const counter = document.createElement('span');
  counter.className = 'ruler-counter';
  const metadata = document.createElement('p');
  metadata.className = 'film-metadata';
  controls.prepend(metadata);
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = t => t < .5 ? 16 * t ** 5 : 1 - (-2 * t + 2) ** 5 / 2;
  const initialPosition = (works.length - 1) / 2;
  let active = false, width = 0, height = 0, position = initialPosition, target = initialPosition;
  let expansion = 0, expandFrom = 0, expandTo = 0, expandStart = 0;
  let pointerX = 0, pointerY = 0, followX = 0, hover = 0, hoverGoal = 0;
  let frame = 0, lastTime = 0, drag = null, suppressClick = false, wheelTimer = 0;
  let selected = -1, fit = 0, fitGoal = 0, titleAnimations = [], isTouch = false;
  const cards = [], ticks = [], images = [], videos = [], frameIndexes = [];
  const renderer = createRibbonRenderer(document.getElementById('film-canvas'));

  works.forEach((work, index) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'film-card';
    card.setAttribute('aria-label', `Рассмотреть: ${work.title}`);
    const image = new Image();
    image.alt = work.title;
    image.draggable = false;
    image.onload = () => { renderer?.upload(index, image); wake(); };
    image.src = work.poster || work.src;
    card.append(image);
    if (work.kind === 'video') {
      const video = document.createElement('video');
      video.dataset.src = work.src;
      video.poster = work.poster;
      video.muted = true;
      video.loop = true;
      video.preload = 'metadata';
      video.setAttribute('playsinline', '');
      video.setAttribute('aria-hidden', 'true');
      card.append(video);
      videos[index] = video;
    }
    card.addEventListener('click', event => {
      if (suppressClick && event.detail !== 0) return;
      if (!expandTo) open(index);
      else if (index !== Math.round(target)) goTo(index);
      else close();
    });
    // Keyboard focus scrolls an offscreen thumbnail into the viewport.
    card.addEventListener('focus', () => {
      if (card.matches(':focus-visible')) goTo(index);
    });
    track.append(card);
    cards.push(card);
    images.push(image);
    frameIndexes[index] = 0;
    const tick = document.createElement('button');
    tick.type = 'button';
    tick.setAttribute('aria-label', `Выбрать: ${work.title}`);
    tick.addEventListener('click', () => goTo(index));
    ruler.append(tick);
    ticks.push(tick);
  });
  ruler.append(counter);

  function syncVideoPlayback(index = -1) {
    videos.forEach((video, videoIndex) => {
      if (!video) return;
      const shouldPlay = expandTo && videoIndex === index && !reduced;
      if (shouldPlay) {
        if (!video.src) video.src = video.dataset.src;
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    });
  }

  function dimensions() {
    const mobile = width < 700;
    const smallWidth = mobile ? 34 : clamp(width * .0375, 42, 62);
    const smallHeight = mobile ? Math.min(156, height * .23) : clamp(height * .255, 145, 236);
    const bigWidth = width * (mobile ? .78 : .495);
    const bigHeight = mobile ? Math.min(height * .34, bigWidth * 1.05) : height * .5;
    return {
      w: lerp(smallWidth, bigWidth, expansion),
      h: lerp(smallHeight, bigHeight, expansion),
      gap: lerp(mobile ? 8 : 11, width * (mobile ? .11 : .095), expansion),
      y: height * .5
    };
  }

  function framesFor(work) {
    return work.frames?.length ? work.frames : [{ src: work.poster || work.src, label: work.title }];
  }

  function showFrame(workIndex, frameIndex) {
    const frames = framesFor(works[workIndex]);
    const frame = frames[frameIndex];
    if (!frame) return;
    frameIndexes[workIndex] = frameIndex;
    images[workIndex].alt = `${works[workIndex].title} — ${frame.label}`;
    images[workIndex].src = frame.src;
    frameRail.querySelectorAll('button').forEach((button, index) => {
      button.setAttribute('aria-current', String(index === frameIndex));
    });
    document.getElementById('film-announcement').textContent = `${works[workIndex].title}. Кадр ${frameIndex + 1} из ${frames.length}: ${frame.label}.`;
    wake();
  }

  function renderFrameRail(workIndex) {
    const work = works[workIndex];
    const frames = framesFor(work);
    frameRail.replaceChildren();
    frameRail.hidden = frames.length < 2;
    frameRail.setAttribute('aria-label', `Кадры проекта «${work.title}»`);
    if (frames.length < 2) return;
    frames.forEach((frame, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-label', `Показать кадр: ${frame.label}`);
      button.setAttribute('aria-current', String(index === frameIndexes[workIndex]));
      const preview = new Image();
      preview.src = frame.src;
      preview.alt = '';
      button.append(preview);
      button.addEventListener('pointerdown', event => event.stopPropagation());
      button.addEventListener('click', event => {
        event.stopPropagation();
        showFrame(workIndex, index);
      });
      frameRail.append(button);
    });
  }

  function setTitle(index, animate = true) {
    if (selected === index) return;
    const direction = selected < index ? 1 : -1;
    selected = index;
    const work = works[index];
    metadata.textContent = work.category || 'Void Studio';
    projectKind.textContent = work.category || 'Void Studio';
    projectDescription.textContent = work.description || '';
    projectRole.textContent = work.role || '';
    projectLink.href = work.url || '#';
    projectLink.textContent = work.urlLabel ? `${work.urlLabel} ↗` : 'Смотреть публикацию ↗';
    projectLink.hidden = !work.url;
    projectCopy.hidden = !work.description && !work.role && !work.url;
    renderFrameRail(index);
    counter.textContent = `${String(index + 1).padStart(2, '0')} / ${works.length}`;
    ticks.forEach((tick, i) => tick.setAttribute('aria-current', String(i === index)));
    cards.forEach((card, i) => card.setAttribute('aria-current', String(i === index)));
    titleAnimations.forEach(animation => animation.cancel());
    titleAnimations = [];
    heading.replaceChildren();
    const words = work.title.split(' ');
    // Balance long Russian titles over two rows, without substituting a new font.
    const lines = words.length > 1 ? (() => {
      let split = 1, difference = Infinity;
      for (let i = 1; i < words.length; i++) {
        const d = Math.abs(words.slice(0, i).join(' ').length - words.slice(i).join(' ').length);
        if (d < difference) { difference = d; split = i; }
      }
      return [words.slice(0, split).join(' '), words.slice(split).join(' ')];
    })() : words;
    let n = 0;
    for (const line of lines) {
      const row = document.createElement('span');
      row.className = 'film-title-line';
      for (const letter of line) {
        const span = document.createElement('span');
        span.className = 'film-title-letter';
        span.textContent = letter === ' ' ? '\u00a0' : letter;
        row.append(span);
        if (expandTo && animate && !reduced) {
          titleAnimations.push(span.animate([
            { opacity: 0, transform: `translate3d(${direction * 32}px,${45 + (n % 3) * 22}px,0)` },
            { opacity: 1, transform: 'translate3d(0,0,0)' }
          ], { duration: 900, delay: 90 + n * 17, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'both' }));
        }
        n++;
      }
      heading.append(row);
    }
    if (expandTo) {
      document.body.style.setProperty('--film-background', work.detailBackground || '#eeece6');
      document.body.style.setProperty('--film-ink', work.detailInk || '#252622');
      document.body.style.setProperty('--film-title', work.accent || work.color || '#7d5137');
      document.getElementById('film-announcement').textContent = `${work.title}. ${index + 1} из ${works.length}.`;
    }
    syncVideoPlayback(index);
  }

  function changeScale(value) {
    expandFrom = expansion;
    expandTo = value;
    expandStart = performance.now();
    section.dataset.view = value ? 'detail' : 'index';
    document.body.dataset.filmView = section.dataset.view;
    controls.inert = !value;
    frameRail.inert = !value;
    projectCopy.setAttribute('aria-hidden', String(!value));
    hoverGoal = 0;
    resetFit();
    if (!value) {
      syncVideoPlayback(-1);
      document.body.style.setProperty('--film-background', '#141414');
      document.body.style.setProperty('--film-ink', '#e4e5da');
      document.body.style.setProperty('--film-title', '#e4e5da');
      stage.focus({ preventScroll: true });
    }
    wake();
  }

  function open(index) {
    clearTimeout(wheelTimer);
    target = index;
    changeScale(1);
    selected = -1;
    setTitle(index);
  }
  function close() { if (expandTo) changeScale(0); }
  function goTo(index) {
    target = clamp(index, 0, works.length - 1);
    resetFit();
    wake();
  }
  function resetFit() {
    fitGoal = 0;
    section.dataset.fit = 'crop';
    if (fitButton) {
      fitButton.setAttribute('aria-pressed', 'false');
      fitButton.innerHTML = 'Рассмотреть <span>+</span>';
    }
  }
  function toggleFit() {
    if (!fitButton) return;
    fitGoal = fitGoal ? 0 : 1;
    section.dataset.fit = fitGoal ? 'full' : 'crop';
    fitButton.setAttribute('aria-pressed', String(Boolean(fitGoal)));
    fitButton.innerHTML = fitGoal ? 'Вернуть кадр <span>−</span>' : 'Рассмотреть <span>+</span>';
    wake();
  }

  function render(time) {
    frame = 0;
    if (!active || !width) return;
    const dt = Math.min(32, time - (lastTime || time - 16.67));
    lastTime = time;
    const ease = reduced ? 1 : 1 - Math.exp(-dt / (drag ? 42 : 125));
    const before = position;
    position = lerp(position, target, ease);
    if (Math.abs(target - position) < .0001) position = target;
    expansion = reduced ? expandTo : lerp(expandFrom, expandTo, smooth(clamp((time - expandStart) / 1100, 0, 1)));
    followX = lerp(followX, pointerX, reduced ? 1 : 1 - Math.exp(-dt / 85));
    hover = lerp(hover, hoverGoal, ease);
    fit = lerp(fit, fitGoal, ease);
    const layout = dimensions();
    const step = layout.w + layout.gap;
    const velocity = reduced ? 0 : (position - before) * step / Math.max(dt, 1);
    const current = clamp(Math.round(position), 0, works.length - 1);
    if (!expandTo || expansion > .95) setTitle(current);
    renderer?.begin(width, height);
    for (let i = 0; i < cards.length; i++) {
      const center = width / 2 + (i - position) * step;
      const visible = center + layout.w / 2 > -100 && center - layout.w / 2 < width + 100;
      const card = cards[i];
      card.style.visibility = visible ? 'visible' : 'hidden';
      const proximity = Math.exp(-Math.pow((center - followX) / (width < 700 ? 125 : 245), 2)) * hover;
      const highlight = Math.abs(center - pointerX) < layout.w / 2 + 6 ? hover : 0;
      const selectedness = Math.max(0, 1 - Math.abs(i - position));
      card.style.width = `${layout.w}px`;
      card.style.height = `${layout.h}px`;
      card.style.transform = `translate3d(${center - layout.w / 2}px,${layout.y - layout.h / 2}px,0)`;
      card.querySelectorAll('img,video').forEach(media => {
        media.style.objectFit = fit > .5 && i === current ? 'contain' : 'cover';
      });
      if (visible) renderer?.draw(i, {
        x: center, y: layout.y, w: layout.w, h: layout.h,
        pointer: followX, hover: reduced ? 0 : hover, expansion,
        velocity, highlight, selectedness, fit: i === current ? fit : 0
      });
      if (!renderer?.ready) {
        card.style.transform += ` scaleY(${1 + proximity * .22 * (1 - expansion)})`;
      }
    }
    if (renderer?.ready) stage.classList.add('has-webgl');
    else stage.classList.remove('has-webgl');
    if (Math.abs(position - target) > .0001 || Math.abs(expansion - expandTo) > .0001 ||
        Math.abs(hover - hoverGoal) > .001 || Math.abs(followX - pointerX) > .1 || Math.abs(fit - fitGoal) > .001) wake();
  }
  function wake() { if (active && !frame) frame = requestAnimationFrame(render); }
  function resize() {
    width = stage.clientWidth;
    height = stage.clientHeight;
    wake();
  }
  new ResizeObserver(resize).observe(stage);

  stage.addEventListener('wheel', event => {
    if (!active) return;
    event.preventDefault();
    const raw = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
    const delta = raw * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? width : 1);
    const layout = dimensions();
    target = clamp(target + delta * (expandTo ? 1.15 : .14) / (layout.w + layout.gap), 0, works.length - 1);
    resetFit();
    clearTimeout(wheelTimer);
    if (expandTo) wheelTimer = setTimeout(() => { target = Math.round(target); wake(); }, 160);
    wake();
  }, { passive: false });

  stage.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    isTouch = event.pointerType === 'touch';
    suppressClick = false;
    clearTimeout(wheelTimer);
    drag = { x: event.clientX, start: target, last: event.clientX, time: performance.now(), velocity: 0, moved: false };
  });
  stage.addEventListener('pointermove', event => {
    const bounds = stage.getBoundingClientRect();
    pointerX = event.clientX - bounds.left;
    pointerY = event.clientY - bounds.top;
    const layout = dimensions();
    hoverGoal = !expandTo && event.pointerType !== 'touch' && Math.abs(pointerY - layout.y) < layout.h * .85 ? 1 : 0;
    if (drag) {
      const distance = event.clientX - drag.x;
      if (Math.abs(distance) > 5 && !drag.moved) {
        drag.moved = true;
        stage.setPointerCapture(event.pointerId);
        stage.classList.add('dragging');
      }
      if (drag.moved) {
        target = clamp(drag.start - distance / (layout.w + layout.gap), 0, works.length - 1);
        const now = performance.now();
        drag.velocity = lerp(drag.velocity, (event.clientX - drag.last) / Math.max(8, now - drag.time), .65);
        drag.last = event.clientX;
        drag.time = now;
      }
    }
    wake();
  });
  function endDrag(event) {
    if (!drag) return;
    suppressClick = drag.moved;
    if (drag.moved) {
      const layout = dimensions();
      const freshVelocity = performance.now() - drag.time < 100 ? drag.velocity : 0;
      const fling = reduced || event.type === 'pointercancel' ? 0 : clamp(freshVelocity * 120 / (layout.w + layout.gap), -2.8, 2.8);
      target = clamp(target - fling, 0, works.length - 1);
      if (expandTo) target = Math.round(target);
      resetFit();
    }
    drag = null;
    stage.classList.remove('dragging');
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
    if (isTouch) hoverGoal = 0;
    wake();
  }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);
  window.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointerleave', () => { hoverGoal = 0; wake(); });
  window.addEventListener('blur', () => { drag = null; hoverGoal = 0; stage.classList.remove('dragging'); wake(); });
  document.getElementById('film-back').addEventListener('click', close);
  fitButton?.addEventListener('click', toggleFit);
  document.querySelector('.brand').addEventListener('click', event => {
    if (active && expandTo) { event.preventDefault(); close(); }
  });
  document.addEventListener('keydown', event => {
    if (!active || document.getElementById('viewer').open || event.target.closest('input,textarea,[contenteditable]')) return;
    if (event.key === 'Escape') close();
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      goTo(Math.round(target) + (event.key === 'ArrowRight' ? 1 : -1));
    }
    if (event.key === 'Enter' && event.target === stage) { event.preventDefault(); open(Math.round(position)); }
  });
  return {
    goTo,
    setActive(value) {
      active = value;
      lastTime = 0;
      if (active) { resize(); wake(); }
      else { drag = null; hoverGoal = 0; clearTimeout(wheelTimer); }
    }
  };
}

// A subdivided image plane: the curve deforms the pixels continuously across
// thumbnail boundaries, rather than rotating thirteen rigid DOM rectangles.
function createRibbonRenderer(canvas) {
  const gl = canvas.getContext('webgl', { alpha: true, antialias: true, premultipliedAlpha: true });
  if (!gl) { canvas.dataset.renderer = 'dom-no-webgl'; return null; }
  let ready = true;
  const textures = [], ratios = [];
  const vertex = `
    precision mediump float;
    attribute vec2 aUV;
    uniform vec2 uViewport, uCenter, uSize;
    uniform float uPointer, uHover, uExpansion, uVelocity;
    varying vec2 vUV;
    void main() {
      vec2 p = uCenter + (aUV - .5) * uSize;
      float distance = (p.x - uPointer) / 245.;
      float wave = exp(-distance * distance) * uHover * (1. - uExpansion);
      p.y = uCenter.y + (aUV.y - .5) * uSize.y * (1. + wave * .26);
      p.x += sin(aUV.y * 3.14159265) * clamp(uVelocity, -2., 2.) * 9. * (1. - uExpansion * .8);
      gl_Position = vec4(p.x / uViewport.x * 2. - 1., 1. - p.y / uViewport.y * 2., 0., 1.);
      vUV = aUV;
    }`;
  const fragment = `
    precision mediump float;
    varying vec2 vUV;
    uniform sampler2D uImage;
    uniform float uRatio, uFrameRatio, uExpansion, uHighlight, uSelected, uFit;
    void main() {
      vec2 cover = vec2(min(1., uFrameRatio / uRatio), min(1., uRatio / uFrameRatio));
      vec2 contain = vec2(max(1., uFrameRatio / uRatio), max(1., uRatio / uFrameRatio));
      vec2 uv = (vUV - .5) * mix(cover, contain, uFit) + .5;
      if (uv.x < 0. || uv.x > 1. || uv.y < 0. || uv.y > 1.) discard;
      vec4 color = texture2D(uImage, uv);
      float gray = dot(color.rgb, vec3(.299, .587, .114));
      color.rgb = mix(vec3(gray), color.rgb, mix(uHighlight * .9, 1., uExpansion));
      color.rgb *= mix(.48 + uHighlight * .35, 1., uExpansion);
      color.a *= mix(1., .25 + .75 * uSelected, uExpansion);
      gl_FragColor = color;
    }`;
  function shader(type, source) {
    const object = gl.createShader(type);
    gl.shaderSource(object, source);
    gl.compileShader(object);
    if (!gl.getShaderParameter(object, gl.COMPILE_STATUS)) {
      console.warn('Ribbon shader:', gl.getShaderInfoLog(object));
      canvas.dataset.renderer = 'dom-shader-fallback';
      return null;
    }
    return object;
  }
  const vs = shader(gl.VERTEX_SHADER, vertex), fs = shader(gl.FRAGMENT_SHADER, fragment);
  if (!vs || !fs) return null;
  const program = gl.createProgram();
  gl.attachShader(program, vs); gl.attachShader(program, fs); gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.warn('Ribbon program:', gl.getProgramInfoLog(program));
    canvas.dataset.renderer = 'dom-link-fallback';
    return null;
  }
  canvas.dataset.renderer = 'webgl';
  gl.useProgram(program);
  const points = [];
  const columns = 24, rows = 12;
  for (let x = 0; x < columns; x++) for (let y = 0; y < rows; y++) {
    const x0 = x / columns, x1 = (x + 1) / columns, y0 = y / rows, y1 = (y + 1) / rows;
    points.push(x0, y0, x1, y0, x0, y1, x0, y1, x1, y0, x1, y1);
  }
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(points), gl.STATIC_DRAW);
  const uv = gl.getAttribLocation(program, 'aUV');
  gl.enableVertexAttribArray(uv); gl.vertexAttribPointer(uv, 2, gl.FLOAT, false, 0, 0);
  const uniforms = {};
  for (const name of ['Viewport', 'Center', 'Size', 'Pointer', 'Hover', 'Expansion', 'Velocity', 'Ratio', 'FrameRatio', 'Highlight', 'Selected', 'Fit']) {
    uniforms[name] = gl.getUniformLocation(program, `u${name}`);
  }
  gl.enable(gl.BLEND);
  gl.blendFuncSeparate(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA, gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  canvas.addEventListener('webglcontextlost', () => {
    ready = false;
    canvas.parentElement.classList.remove('has-webgl');
  });
  return {
    get ready() { return ready; },
    upload(index, image) {
      if (!ready) return;
      const texture = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image); }
      catch { ready = false; canvas.parentElement.classList.remove('has-webgl'); return; }
      textures[index] = texture;
      ratios[index] = image.naturalWidth / image.naturalHeight;
    },
    begin(width, height) {
      if (!ready) return;
      const dpr = Math.min(devicePixelRatio || 1, 2);
      if (canvas.width !== Math.round(width * dpr) || canvas.height !== Math.round(height * dpr)) {
        canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
      }
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      gl.uniform2f(uniforms.Viewport, width, height);
    },
    draw(index, values) {
      if (!ready || !textures[index]) return;
      gl.bindTexture(gl.TEXTURE_2D, textures[index]);
      gl.uniform2f(uniforms.Center, values.x, values.y);
      gl.uniform2f(uniforms.Size, values.w, values.h);
      for (const [name, value] of Object.entries({
        Pointer: values.pointer, Hover: values.hover, Expansion: values.expansion,
        Velocity: values.velocity, Ratio: ratios[index], FrameRatio: values.w / values.h,
        Highlight: values.highlight, Selected: values.selectedness, Fit: values.fit
      })) gl.uniform1f(uniforms[name], value);
      gl.drawArrays(gl.TRIANGLES, 0, points.length / 2);
    }
  };
}
