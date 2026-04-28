/* IDCFSS — Intro Loading Animation (Vanilla JS Port) */

class TextScramble {
  constructor(el) {
    this.el = el;
    this.chars = '!<>-_\\/[]{}—=+*^?#';
    this.update = this.update.bind(this);
  }
  setText(newText) {
    const oldText = this.el.innerText;
    const length = Math.max(oldText.length, newText.length);
    const promise = new Promise((resolve) => this.resolve = resolve);
    this.queue = [];
    for (let i = 0; i < length; i++) {
      const from = oldText[i] || '';
      const to = newText[i] || '';
      const start = Math.floor(Math.random() * 40);
      const end = start + Math.floor(Math.random() * 40);
      this.queue.push({ from, to, start, end });
    }
    cancelAnimationFrame(this.frameRequest);
    this.frame = 0;
    this.update();
    return promise;
  }
  update() {
    let output = '';
    let complete = 0;
    for (let i = 0, n = this.queue.length; i < n; i++) {
      let { from, to, start, end, char } = this.queue[i];
      if (this.frame >= end) {
        complete++;
        output += to;
      } else if (this.frame >= start) {
        if (!char || Math.random() < 0.28) {
          char = this.chars[Math.floor(Math.random() * this.chars.length)];
          this.queue[i].char = char;
        }
        output += `<span class="dud" style="opacity:0.4;">${char}</span>`;
      } else {
        output += from;
      }
    }
    this.el.innerHTML = output;
    if (complete === this.queue.length) {
      this.resolve();
    } else {
      this.frameRequest = requestAnimationFrame(this.update);
      this.frame++;
    }
  }
}

function initIntroLoader() {
  const loader = document.createElement('div');
  loader.id = 'intro-loader';
  loader.style.cssText = `
    position: fixed; inset: 0; z-index: 100000;
    background: var(--bg); color: var(--fg);
    overflow: hidden; display: flex; align-items: center; justify-content: center;
    transition: opacity 1.2s cubic-bezier(0.76, 0, 0.24, 1), transform 1.2s cubic-bezier(0.76, 0, 0.24, 1);
  `;
  document.body.appendChild(loader);

  const rainContainer = document.createElement('div');
  rainContainer.style.cssText = 'position: absolute; inset: 0; overflow: hidden; z-index: 1;';
  loader.appendChild(rainContainer);

  const title = document.createElement('h1');
  title.style.cssText = `
    position: relative; z-index: 2;
    font-family: var(--font-disp);
    font-size: clamp(32px, 8vw, 80px);
    font-weight: 900;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
  `;
  loader.appendChild(title);

  // 1. Text Scramble Logic
  const fx = new TextScramble(title);
  const phrases = [
    'I.D.C.F.S.S.',
    'INITIALISING',
    'CLEANING DATA',
    'SMARTER MODELS'
  ];
  let counter = 0;
  let scrambleTimeout;
  const next = () => {
    fx.setText(phrases[counter]).then(() => {
      scrambleTimeout = setTimeout(next, 1200);
    });
    counter = (counter + 1) % phrases.length;
  };
  next();

  // 2. Raining Letters Logic
  const allChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?";
  const charCount = 150; // Optimized for DOM
  const characters = [];
  const spans = [];

  for (let i = 0; i < charCount; i++) {
    const char = allChars[Math.floor(Math.random() * allChars.length)];
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const speed = 0.1 + Math.random() * 0.3;
    
    characters.push({ char, x, y, speed });
    
    const span = document.createElement('span');
    span.textContent = char;
    span.style.cssText = `
      position: absolute;
      font-family: var(--font-sans);
      font-size: 14px;
      color: var(--fg);
      opacity: 0.15;
      transform: translate(-50%, -50%);
      will-change: transform, top;
      transition: opacity 0.1s, transform 0.1s, text-shadow 0.1s;
    `;
    spans.push(span);
    rainContainer.appendChild(span);
  }

  let activeIndices = new Set();
  const flickerInterval = setInterval(() => {
    activeIndices.clear();
    const numActive = Math.floor(Math.random() * 3) + 3;
    for (let i = 0; i < numActive; i++) {
      activeIndices.add(Math.floor(Math.random() * charCount));
    }
  }, 50);

  let rainFrameId;
  const updatePositions = () => {
    for (let i = 0; i < charCount; i++) {
      let c = characters[i];
      c.y += c.speed;
      if (c.y >= 100) {
        c.y = -5;
        c.x = Math.random() * 100;
        c.char = allChars[Math.floor(Math.random() * allChars.length)];
        spans[i].textContent = c.char;
      }
      const span = spans[i];
      span.style.left = c.x + '%';
      span.style.top = c.y + '%';
      
      if (activeIndices.has(i)) {
        span.style.opacity = '0.8';
        span.style.transform = 'translate(-50%, -50%) scale(1.5)';
        span.style.fontWeight = '700';
      } else {
        span.style.opacity = '0.15';
        span.style.transform = 'translate(-50%, -50%) scale(1)';
        span.style.fontWeight = '400';
      }
    }
    rainFrameId = requestAnimationFrame(updatePositions);
  };
  rainFrameId = requestAnimationFrame(updatePositions);

  // 3. Smooth Transition Out
  setTimeout(() => {
    clearTimeout(scrambleTimeout);
    clearInterval(flickerInterval);
    cancelAnimationFrame(rainFrameId);
    
    fx.setText('SYSTEM READY').then(() => {
      setTimeout(() => {
        loader.style.opacity = '0';
        loader.style.transform = 'scale(1.05)';
        loader.style.pointerEvents = 'none';
        
        // Trigger main content animations
        document.body.classList.add('ready');
        
        setTimeout(() => {
          loader.remove();
        }, 1200);
      }, 800);
    });
  }, 4500); // Intro lasts ~4.5 seconds
}

// Run immediately on script load
initIntroLoader();
