/* IDCFSS Step 0 - Upload & Step 1 - Profile (Minimal Aesthetic) */
function tplUpload() {
  const galleryCards = SAMPLES.map(s => `
    <div class="sample-card" onclick="loadSampleById('${s.id}')">
      <div class="sample-card-name">${s.name}</div>
      <div class="sample-card-meta">${s.rows} rows / ${s.cols} cols / ${s.tag}</div>
      <div class="sample-card-desc">${s.desc}</div>
    </div>`).join('');

  return `
    <div class="hero" id="hero-section" style="position: relative; height: 90vh; min-height: 600px; overflow: hidden; border-bottom: 1px solid var(--fg); display: flex; flex-direction: column; justify-content: flex-start; padding: 40px 32px; background: var(--bg); transition: background 0.6s;">
      
      <!-- Flickering Grid Background (No Mask so it reaches the very top) -->
      <div style="position: absolute; inset: 0; z-index: 0;">
        <canvas id="flicker-bg" style="width: 100%; height: 100%; pointer-events: none;"></canvas>
      </div>

      <!-- Flickering Grid Logo -->
      <div id="flicker-logo-container" style="position: absolute; inset: 0; z-index: 0; transform: translateY(2vh); mask-size: 100vw; mask-position: center; mask-repeat: no-repeat; -webkit-mask-size: 100vw; -webkit-mask-position: center; -webkit-mask-repeat: no-repeat; opacity: 0.8; animation: pulseLogo 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;">
        <canvas id="flicker-logo" style="width: 100%; height: 100%; pointer-events: none;"></canvas>
      </div>

      <div style="position:relative; z-index:1; color: var(--fg); width: 100%; max-width: 1400px; margin: 0 auto; transition: color 0.6s;">
        <div class="prisma-grid">
          
          <div>
            <h1 class="hero-title-huge" style="color: var(--fg); text-align: left; margin: 0; line-height: 0.85; font-size: clamp(60px, 12vw, 200px); transition: color 0.6s;">
              <span class="pull-up" style="animation-delay: 0.1s; padding-right: 20px;">CLEAN</span>
              <span class="pull-up" style="animation-delay: 0.2s">DATA</span><span class="pull-up" style="animation-delay: 0.3s; color: var(--fg-muted); transition: color 0.6s;">*</span>
            </h1>
          </div>

          <div style="display: flex; flex-direction: column; gap: 24px; padding-bottom: 12px;">
            <div class="label-small pull-up" style="animation-delay: 0.4s; color: var(--fg); line-height: 1.6; text-transform: uppercase; transition: color 0.6s;">
              I.D.C.F.S.S is a powerful engine bound not by complex code, but by a seamless flow to detect issues, impute missing values, and unlock predictive potential through automated feature selection.
            </div>
            
            <div style="display: flex; gap: 16px;">
              <button class="theme-toggle-btn pull-up" onclick="toggleFlickerTheme()" style="animation-delay: 0.5s;" aria-label="Toggle Theme">
                <div class="theme-toggle-icon">
                  <!-- Sun SVG -->
                  <svg class="theme-sun" viewBox="0 0 25 25">
                    <path d="M12.4058 17.7625C15.1672 17.7625 17.4058 15.5239 17.4058 12.7625C17.4058 10.0011 15.1672 7.76251 12.4058 7.76251C9.64434 7.76251 7.40576 10.0011 7.40576 12.7625C7.40576 15.5239 9.64434 17.7625 12.4058 17.7625Z"/>
                    <path d="M12.4058 1.76251V3.76251"/>
                    <path d="M12.4058 21.7625V23.7625"/>
                    <path d="M4.62598 4.98248L6.04598 6.40248"/>
                    <path d="M18.7656 19.1225L20.1856 20.5425"/>
                    <path d="M1.40576 12.7625H3.40576"/>
                    <path d="M21.4058 12.7625H23.4058"/>
                    <path d="M4.62598 20.5425L6.04598 19.1225"/>
                    <path d="M18.7656 6.40248L20.1856 4.98248"/>
                  </svg>
                  <!-- Moon SVG -->
                  <svg class="theme-moon" viewBox="0 0 25 25">
                    <path d="M21.1918 13.2013C21.0345 14.9035 20.3957 16.5257 19.35 17.8781C18.3044 19.2305 16.8953 20.2571 15.2875 20.8379C13.6797 21.4186 11.9398 21.5294 10.2713 21.1574C8.60281 20.7854 7.07479 19.9459 5.86602 18.7371C4.65725 17.5283 3.81774 16.0003 3.4457 14.3318C3.07367 12.6633 3.18451 10.9234 3.76526 9.31561C4.346 7.70783 5.37263 6.29868 6.72501 5.25307C8.07739 4.20746 9.69959 3.56862 11.4018 3.41132C10.4052 4.75958 9.92564 6.42077 10.0503 8.09273C10.175 9.76469 10.8957 11.3364 12.0812 12.5219C13.2667 13.7075 14.8384 14.4281 16.5104 14.5528C18.1823 14.6775 19.8435 14.1979 21.1918 13.2013Z"/>
                  </svg>
                </div>
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
    
    <div class="upload-zone mb-24" id="upload-zone">
      <div class="font-disp" style="font-size:24px; margin-bottom:8px;">DROP DATASET HERE</div>
      <div class="label-small mb-24">SUPPORTS CSV AND EXCEL UP TO 100MB</div>
      <button class="btn" onclick="document.getElementById('file-input').click()">BROWSE FILES</button>
      <input type="file" id="file-input" accept=".csv,.xlsx,.xls"/>
    </div>
    
    <div class="testimonial-container" style="position: relative; width: 100%; max-width: 1024px; margin: 0 auto; min-height: 80vh; display: flex; align-items: center; justify-content: center; overflow: hidden; background: transparent; padding-top: 64px;">
      
      <div class="test-big-num" id="test-big-num" style="position: absolute; left: -2rem; top: 50%; transform: translateY(-50%); font-size: 28rem; font-weight: bold; color: rgba(13,13,13,0.03); user-select: none; pointer-events: none; line-height: 1; letter-spacing: -0.05em; transition: opacity 0.6s, filter 0.6s, transform 0.6s;">
        01
      </div>

      <div style="position: relative; display: flex; width: 100%; z-index: 10;">
        <!-- Left Col -->
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding-right: 4rem; border-right: var(--rule);">
          <span id="test-category" style="font-size: 12px; font-family: var(--font-sans); color: var(--fg); letter-spacing: 0.2em; text-transform: uppercase; writing-mode: vertical-rl; text-orientation: mixed; transition: opacity 0.4s;">EXPLORE</span>
          <div style="position: relative; height: 128px; width: 1px; background: rgba(13,13,13,0.15); margin-top: 32px;">
            <div id="test-progress" style="position: absolute; top: 0; left: 0; width: 100%; background: var(--fg); transform-origin: top; transition: height 0.5s cubic-bezier(0.22, 1, 0.36, 1); height: 11.11%;"></div>
          </div>
        </div>

        <!-- Right Col -->
        <div style="flex: 1; padding-left: 4rem; padding-top: 3rem; padding-bottom: 3rem;">
          <div id="test-badge" style="margin-bottom: 32px; transition: opacity 0.4s, transform 0.4s;">
            <span style="display: inline-flex; align-items: center; gap: 8px; font-size: 12px; font-family: var(--font-sans); color: var(--fg); border: 1px solid rgba(13,13,13,0.15); border-radius: 9999px; padding: 4px 12px; text-transform: uppercase;">
              <span style="width: 6px; height: 6px; border-radius: 50%; background: #000;"></span>
              <span id="test-company">Sample Dataset</span>
            </span>
          </div>

          <div style="position: relative; margin-bottom: 48px; min-height: 140px;">
            <blockquote id="test-quote" style="font-family: var(--font-disp); font-size: clamp(32px, 4vw, 48px); font-weight: 300; color: var(--fg); line-height: 1.15; letter-spacing: -0.02em; margin: 0; perspective: 1000px; text-transform: none;">
              <!-- Words inserted here -->
            </blockquote>
          </div>

          <div style="display: flex; align-items: flex-end; justify-content: space-between;">
            <div id="test-author-box" style="display: flex; align-items: center; gap: 16px; transition: opacity 0.4s, transform 0.4s; transition-delay: 0.2s;">
              <div id="test-author-line" style="width: 32px; height: 1px; background: var(--fg); transform-origin: left; transition: transform 0.6s; transition-delay: 0.3s;"></div>
              <div>
                <p id="test-author" style="font-size: 16px; font-weight: 500; color: var(--fg); margin: 0;">Titanic Survival</p>
                <p id="test-role" style="font-size: 14px; color: var(--fg-muted); margin: 0;">Classification | 25 rows</p>
              </div>
            </div>

            <div style="display: flex; align-items: center; gap: 16px;">
              <button id="test-action-btn" class="btn" style="border-radius: 99px; padding: 8px 16px; font-size: 10px; opacity: 1; transition: opacity 0.3s;" onclick="loadSampleById(window.testimonialsData[window.testActiveIndex].actionId)">
                LOAD DATASET
              </button>
              <button class="test-nav-btn" onclick="prevTestimonial()">
                <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10 12L6 8L10 4"/></svg>
              </button>
              <button class="test-nav-btn" onclick="nextTestimonial()">
                <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 4L10 8L6 12"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Ticker -->
      <div style="position: absolute; bottom: -40px; left: 0; right: 0; overflow: hidden; opacity: 0.04; pointer-events: none;">
        <div class="test-ticker" style="display: flex; white-space: nowrap; font-size: 60px; font-weight: bold; letter-spacing: -0.05em; color: var(--fg); font-family: var(--font-sans);">
          <!-- Ticker content -->
        </div>
      </div>
    </div>
  `;
}

function bindUpload() {
  const zone = document.getElementById('upload-zone');
  const input = document.getElementById('file-input');
  if(zone) {
    zone.addEventListener('click', e => { if (!e.target.closest('button, input')) input.click() });
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over') });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
      e.preventDefault(); zone.classList.remove('drag-over');
      if (e.dataTransfer.files[0]) doUpload(e.dataTransfer.files[0]);
    });
    input.addEventListener('change', () => {
      if (input.files[0]) doUpload(input.files[0]);
    });
  }

  // --- Vanilla JS Framer Motion & WordsPullUp Clone ---
  const titleContainer = document.getElementById('words-pull-up-title');
  if (titleContainer) {
    const text = "PRISMA"; // Matching the exact component request
    const words = text.split(" ");
    titleContainer.innerHTML = "";
    titleContainer.style.display = "inline-flex";
    titleContainer.style.flexWrap = "wrap";
    
    words.forEach((word, i) => {
      const isLast = i === words.length - 1;
      const span = document.createElement("span");
      span.className = "inline-block relative fm-anim";
      span.style.opacity = "0";
      span.style.transform = "translateY(20px)";
      span.style.transition = `opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1) ${i * 0.08}s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1) ${i * 0.08}s`;
      span.style.marginRight = isLast ? "0" : "0.25em";
      span.textContent = word;
      
      if (isLast) {
        const asterisk = document.createElement("span");
        asterisk.textContent = "*";
        asterisk.style.position = "absolute";
        asterisk.style.top = "0.65em";
        asterisk.style.right = "-0.3em";
        asterisk.style.fontSize = "0.31em";
        span.appendChild(asterisk);
      }
      titleContainer.appendChild(span);
    });
  }

  const desc = document.getElementById('fm-desc');
  if (desc) {
    desc.style.opacity = "0";
    desc.style.transform = "translateY(20px)";
    desc.style.transition = `opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s`;
  }
  
  const btn = document.getElementById('fm-btn');
  if (btn) {
    btn.style.opacity = "0";
    btn.style.transform = "translateY(20px)";
    btn.style.transition = `opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.7s, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.7s`;
  }

  // Exact replication of Framer Motion's useInView(ref, { once: true })
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (entry.target.id === 'words-pull-up-title') {
          entry.target.querySelectorAll('.fm-anim').forEach(span => {
            span.style.opacity = "1";
            span.style.transform = "translateY(0)";
          });
        }
        if (entry.target.id === 'fm-desc' || entry.target.id === 'fm-btn') {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Use requestAnimationFrame to ensure it plays flawlessly after DOM paint
  requestAnimationFrame(() => {
    if (titleContainer) observer.observe(titleContainer);
    if (desc) observer.observe(desc);
    if (btn) observer.observe(btn);
  });

  // --- Flickering Grid Logic ---
  const LOGO_BASE64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODQiIGhlaWdodD0iODQiIHZpZXdCb3g9IjAgMCA4NCA4NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTMgMzJDMTMgMjAuOTU0MyAyMS45NTQzIDEyIDMzIDEyQzQ0LjA0NTcgMTIgNTMgMjAuOTU0MyA1MyAzMkM1MyA0My4wNDU3IDQ0LjUgNDcuNSAzMyA1Mkg1M0M1MyA2My4wNDU3IDQ0LjA0NTcgNzIgMzMgNzJDMjEuOTU0MyA3MiAxMyA2My4wNDU3IDEzIDUyQzEzIDQwLjk1NDMgMjIuNSAzNCAzMyAzMkgxM1oiIGZpbGw9IndoaXRlIi8+PHBhdGggZD0iTTUzIDcyQzY0LjczMjQgNjcuMDk3NyA3MyA1NS41MTE3IDczIDQyQzczIDI4LjQ4ODMgNjQuNzMyNCAxNi45MDIzIDUzIDEyVjcyWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=";
  const logoContainer = document.getElementById('flicker-logo-container');
  if (logoContainer) {
    const ms = `url('${LOGO_BASE64}')`;
    logoContainer.style.webkitMaskImage = ms;
    logoContainer.style.maskImage = ms;
  }

  function initFlickeringGrid(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let { squareSize, gridGap, flickerChance, maxOpacity, r, g, b } = config;
    const colorPrefix = `rgba(${r}, ${g}, ${b}, `;

    let cols = 0, rows = 0;
    let squares = new Float32Array(0);
    
    function resize() {
      const parent = canvas.parentElement;
      const w = parent.clientWidth || window.innerWidth;
      const h = parent.clientHeight || window.innerHeight;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      
      cols = Math.floor(w / (squareSize + gridGap));
      rows = Math.floor(h / (squareSize + gridGap));
      squares = new Float32Array(cols * rows);
      for(let i=0; i<squares.length; i++) squares[i] = Math.random() * maxOpacity;
    }
    
    window.addEventListener('resize', resize);
    resize();
    
    let lastTime = performance.now();
    let animId;
    function animate(time) {
      const deltaTime = (time - lastTime) / 1000;
      lastTime = time;
      
      for(let i=0; i<squares.length; i++) {
        if(Math.random() < flickerChance * deltaTime) {
          squares[i] = Math.random() * maxOpacity;
        }
      }
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const dpr = window.devicePixelRatio || 1;
      for(let i=0; i<cols; i++) {
        for(let j=0; j<rows; j++) {
          const opacity = squares[i * rows + j];
          ctx.fillStyle = colorPrefix + opacity + ')';
          ctx.fillRect(
            i * (squareSize + gridGap) * dpr,
            j * (squareSize + gridGap) * dpr,
            squareSize * dpr,
            squareSize * dpr
          );
        }
      }
      animId = requestAnimationFrame(animate);
    }
    animId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animId);
  }

  window.flickerThemeDark = window.flickerThemeDark || false;

  window.toggleFlickerTheme = () => {
    window.flickerThemeDark = !window.flickerThemeDark;
    document.body.classList.toggle('dark-mode', window.flickerThemeDark);
    
    if (window.stopBgGrid) window.stopBgGrid();
    if (window.stopLogoGrid) window.stopLogoGrid();
    
    if (!window.flickerThemeDark) {
      window.stopBgGrid = initFlickeringGrid('flicker-bg', { squareSize: 4, gridGap: 4, flickerChance: 0.12, maxOpacity: 0.15, r: 0, g: 0, b: 0 });
      window.stopLogoGrid = initFlickeringGrid('flicker-logo', { squareSize: 3, gridGap: 6, flickerChance: 0.18, maxOpacity: 0.35, r: 0, g: 0, b: 0 });
    } else {
      window.stopBgGrid = initFlickeringGrid('flicker-bg', { squareSize: 4, gridGap: 4, flickerChance: 0.12, maxOpacity: 0.15, r: 109, g: 40, b: 217 });
      window.stopLogoGrid = initFlickeringGrid('flicker-logo', { squareSize: 3, gridGap: 6, flickerChance: 0.18, maxOpacity: 0.65, r: 124, g: 58, b: 237 });
    }
  };

  // Initial setup without toggling state
  if (!window.flickerThemeDark) {
    document.body.classList.remove('dark-mode');
    if (window.stopBgGrid) window.stopBgGrid();
    window.stopBgGrid = initFlickeringGrid('flicker-bg', { squareSize: 4, gridGap: 4, flickerChance: 0.12, maxOpacity: 0.15, r: 0, g: 0, b: 0 });
    if (window.stopLogoGrid) window.stopLogoGrid();
    window.stopLogoGrid = initFlickeringGrid('flicker-logo', { squareSize: 3, gridGap: 6, flickerChance: 0.18, maxOpacity: 0.35, r: 0, g: 0, b: 0 });
  } else {
    document.body.classList.add('dark-mode');
    if (window.stopBgGrid) window.stopBgGrid();
    window.stopBgGrid = initFlickeringGrid('flicker-bg', { squareSize: 4, gridGap: 4, flickerChance: 0.12, maxOpacity: 0.15, r: 109, g: 40, b: 217 });
    if (window.stopLogoGrid) window.stopLogoGrid();
    window.stopLogoGrid = initFlickeringGrid('flicker-logo', { squareSize: 3, gridGap: 6, flickerChance: 0.18, maxOpacity: 0.65, r: 124, g: 58, b: 237 });
  }


  // --- Testimonial Logic ---
  window.testimonialsData = [
    { category: "Explore", tag: "Sample Dataset", quote: "Passenger survival data — missing ages, categorical sex/embarked.", author: "Titanic Survival", role: "Classification | 25 rows / 10 cols", actionId: "titanic" },
    { category: "Explore", tag: "Sample Dataset", quote: "Classic flower dataset — 3 species, all numeric, clean baseline.", author: "Iris Flowers", role: "Classification | 30 rows / 5 cols", actionId: "iris" },
    { category: "Explore", tag: "Sample Dataset", quote: "Property pricing data — mixed types, missing values, outliers.", author: "House Prices", role: "Regression | 30 rows / 8 cols", actionId: "house" },
    { category: "Explore", tag: "Sample Dataset", quote: "Patient health data — outliers in glucose and BMI, binary target.", author: "Diabetes", role: "Classification | 30 rows / 9 cols", actionId: "diabetes" },
    { category: "Explore", tag: "Sample Dataset", quote: "HR dataset — job roles, departments, missing salary, churn target.", author: "Employee Attrition", role: "HR Analytics | 30 rows / 9 cols", actionId: "employees" },
    { category: "Explore", tag: "Sample Dataset", quote: "Physicochemical wine properties — numeric features, outliers in acidity.", author: "Wine Quality", role: "Regression | 30 rows / 12 cols", actionId: "wine" },
    { category: "Capabilities", tag: "Processing Engine", quote: "Mean, median, KNN, MICE, forward fill — choose per column.", author: "Missing Values", role: "Imputation & Handling", actionId: null },
    { category: "Capabilities", tag: "Quality Control", quote: "IQR, Z-Score, Isolation Forest — remove, cap, or impute.", author: "Outlier Detection", role: "Anomaly Management", actionId: null },
    { category: "Capabilities", tag: "Feature Eng.", quote: "Label, One-Hot, Binary, Target encoding.", author: "Smart Encoding", role: "Categorical Transformation", actionId: null }
  ];
  window.testActiveIndex = 0;
  
  if (window.testInterval) clearInterval(window.testInterval);

  window.renderTestimonial = function(index) {
    const t = window.testimonialsData[index];
    const bigNum = document.getElementById('test-big-num');
    const category = document.getElementById('test-category');
    const company = document.getElementById('test-company');
    const quote = document.getElementById('test-quote');
    const author = document.getElementById('test-author');
    const role = document.getElementById('test-role');
    const prog = document.getElementById('test-progress');
    const badge = document.getElementById('test-badge');
    const authorBox = document.getElementById('test-author-box');
    const actionBtn = document.getElementById('test-action-btn');
    
    if (!bigNum || !quote) return;

    bigNum.style.opacity = 0; bigNum.style.filter = "blur(10px)"; bigNum.style.transform = "translateY(-50%) scale(1.1)";
    badge.style.opacity = 0; badge.style.transform = "translateX(20px)";
    authorBox.style.opacity = 0; authorBox.style.transform = "translateY(-20px)";
    category.style.opacity = 0;
    if (actionBtn) actionBtn.style.opacity = 0;
    
    const words = quote.querySelectorAll('.test-word');
    words.forEach((w, i) => {
      w.style.opacity = 0; w.style.transform = "translateY(-10px)"; w.style.transitionDelay = (i * 0.02) + "s";
    });

    setTimeout(() => {
      bigNum.textContent = String(index + 1).padStart(2, '0');
      category.textContent = t.category;
      company.textContent = t.tag;
      author.textContent = t.author;
      role.textContent = t.role;
      prog.style.height = (((index + 1) / window.testimonialsData.length) * 100) + "%";
      
      if (actionBtn) {
        if (t.actionId) {
          actionBtn.style.display = "inline-flex";
          setTimeout(() => actionBtn.style.opacity = 1, 50);
        } else {
          actionBtn.style.display = "none";
        }
      }

      quote.innerHTML = t.quote.split(" ").map(w => `<span class="test-word">${w}</span>`).join("");
      
      bigNum.style.opacity = 1; bigNum.style.filter = "blur(0px)"; bigNum.style.transform = "translateY(-50%) scale(1)";
      badge.style.opacity = 1; badge.style.transform = "translateX(0)";
      authorBox.style.opacity = 1; authorBox.style.transform = "translateY(0)";
      category.style.opacity = 1;
      
      const newWords = quote.querySelectorAll('.test-word');
      requestAnimationFrame(() => {
        newWords.forEach((w, i) => {
          w.style.transitionDelay = (i * 0.05) + "s";
          w.classList.add('visible');
        });
      });
    }, 400); 
  };

  window.nextTestimonial = () => {
    window.testActiveIndex = (window.testActiveIndex + 1) % window.testimonialsData.length;
    window.renderTestimonial(window.testActiveIndex);
    window.resetTestInterval();
  };

  window.prevTestimonial = () => {
    window.testActiveIndex = (window.testActiveIndex - 1 + window.testimonialsData.length) % window.testimonialsData.length;
    window.renderTestimonial(window.testActiveIndex);
    window.resetTestInterval();
  };

  window.resetTestInterval = function() {
    clearInterval(window.testInterval);
    window.testInterval = setInterval(window.nextTestimonial, 8000);
  };

  setTimeout(() => {
    const quote = document.getElementById('test-quote');
    if(quote) {
      const t = window.testimonialsData[0];
      quote.innerHTML = t.quote.split(" ").map(w => `<span class="test-word">${w}</span>`).join("");
      
      const actionBtn = document.getElementById('test-action-btn');
      if (actionBtn && t.actionId) {
        actionBtn.style.display = "inline-flex";
        actionBtn.style.opacity = 1;
      } else if (actionBtn) {
        actionBtn.style.display = "none";
      }

      requestAnimationFrame(() => {
        quote.querySelectorAll('.test-word').forEach((w, i) => {
          w.style.transitionDelay = (i * 0.05) + "s";
          w.classList.add('visible');
        });
      });
      
      const ticker = document.querySelector('.test-ticker');
      if (ticker) {
        const text = window.testimonialsData.map(d => d.author).join(" • ") + " • ";
        ticker.innerHTML = Array(20).fill(`<span style="margin: 0 32px">${text}</span>`).join("");
      }

      window.resetTestInterval();

      const container = document.querySelector('.testimonial-container');
      const bigNum = document.getElementById('test-big-num');
      if (container && bigNum) {
        container.addEventListener('mousemove', (e) => {
          const rect = container.getBoundingClientRect();
          const centerX = rect.left + rect.width / 2;
          const centerY = rect.top + rect.height / 2;
          const moveX = (e.clientX - centerX) * 0.05;
          const moveY = (e.clientY - centerY) * 0.05;
          bigNum.style.marginLeft = moveX + 'px';
          bigNum.style.marginTop = moveY + 'px';
        });
        container.addEventListener('mouseleave', () => {
          bigNum.style.marginLeft = '0px';
          bigNum.style.marginTop = '0px';
          bigNum.style.transition = 'margin 0.5s cubic-bezier(0.25, 1, 0.5, 1)';
        });
        container.addEventListener('mouseenter', () => {
          bigNum.style.transition = 'margin 0.1s linear';
        });
      }
    }
  }, 100);
}

async function doUpload(file) {
  if (!file.name.match(/\.(csv|xlsx|xls)$/i)) {
    snack('Please upload a CSV or Excel file', 'error');
    return;
  }
  showLoading('UPLOADING DATASET', `PARSING ${file.name}`);
  try {
    const fd = new FormData();
    fd.append('file', file);
    const r = await fetch(S.apiBase + '/upload', { method: 'POST', body: fd });
    if (!r.ok) {
      const e = await r.json();
      throw new Error(e.detail);
    }
    const d = await r.json();
    S.sessionId = d.session_id;
    S.filename = d.filename;
    S.profile = d.profile;
    S.columns = d.columns;
    S.preview = d.preview;
    autoConfig();
    hideLoading();
    snack(`${file.name} loaded — ${d.profile.shape.rows.toLocaleString()} rows`);
    advance();
  } catch (e) {
    hideLoading();
    snack(e.message, 'error');
  }
}

function tplProfile() {
  const p = S.profile;
  const types = { numeric: 0, categorical: 0, datetime: 0 };
  Object.values(p.columns).forEach(c => types[c.inferred_type] = (types[c.inferred_type] || 0) + 1);

  const colRows = Object.entries(p.columns).map(([col, info]) => {
    const statsHtml = info.stats ? 
      `<span>M=${info.stats.mean} S=${info.stats.std}</span>` : 
      `<span class="text-muted">${Object.keys(info.top_values || {}).slice(0, 3).join(', ')}</span>`;
    
    const outlierHtml = info.inferred_type === 'numeric' ? 
      `<span>${info.outlier_count || 0}</span>` : 
      `<span class="text-muted">—</span>`;
      
    return `<tr>
      <td><span style="font-weight:600">${col}</span></td>
      <td><span style="text-transform:uppercase; font-size:10px; letter-spacing:0.1em;">${info.inferred_type}</span></td>
      <td>${info.missing > 0 ? `<span>${info.missing} (${info.missing_pct}%)</span>` : '<span class="text-muted">NONE</span>'}</td>
      <td style="font-size:12px">${info.unique}</td>
      <td style="font-size:12px">${statsHtml}</td>
      <td>${outlierHtml}</td>
    </tr>`;
  }).join('');

  const previewRows = S.preview.slice(0, 10).map(row => 
    `<tr>${S.columns.map(c => {
      const v = row[c];
      return v == null || v === '' ? `<td class="text-muted">null</td>` : `<td>${String(v).slice(0, 30)}</td>`;
    }).join('')}</tr>`
  ).join('');

  return `
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px;">
      <div>
        <h2 class="font-disp" style="font-size:48px;">DATASET PROFILE</h2>
        <div class="label-small">${S.filename} — AUTOMATIC QUALITY ANALYSIS</div>
      </div>
      <button class="btn" onclick="advance()">CONFIGURE CLEANING</button>
    </div>
    
    <hr class="rule" style="margin-bottom:48px;">
    
    <div class="grid-3" style="margin-bottom:64px;">
      <div style="border-right:1px solid rgba(13,13,13,0.15); padding-right:32px;">
        <div class="label-small">TOTAL ROWS</div>
        <div class="font-disp" style="font-size:32px;">${p.shape.rows.toLocaleString()}</div>
        <div class="text-muted" style="font-size:12px;">${p.shape.cols} COLUMNS</div>
      </div>
      <div style="border-right:1px solid rgba(13,13,13,0.15); padding-right:32px;">
        <div class="label-small">MISSING CELLS</div>
        <div class="font-disp" style="font-size:32px;">${p.missing_cells.toLocaleString()}</div>
        <div class="text-muted" style="font-size:12px;">${p.missing_pct}% OF DATASET</div>
      </div>
      <div>
        <div class="label-small">QUALITY SCORE</div>
        <div class="font-disp" style="font-size:32px;">${p.quality_score}/100</div>
        <div class="text-muted" style="font-size:12px;">${p.quality_score >= 80 ? 'GOOD' : 'NEEDS ATTENTION'}</div>
      </div>
    </div>
    
    <div class="aesthetic-card mb-32">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">COLUMN ANALYSIS</div>
        <div class="aesthetic-card-subtitle">${S.columns.length} COLUMNS DETECTED</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th>COLUMN</th><th>TYPE</th><th>MISSING</th><th>UNIQUE</th><th>STATS</th><th>OUTLIERS</th></tr>
          </thead>
          <tbody>${colRows}</tbody>
        </table>
      </div>
    </div>
    
    <div class="aesthetic-card">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">DATA PREVIEW</div>
        <div class="aesthetic-card-subtitle">FIRST 10 ROWS</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>${S.columns.map(c => `<th>${c}</th>`).join('')}</tr>
          </thead>
          <tbody>${previewRows}</tbody>
        </table>
      </div>
    </div>
  `;
}
