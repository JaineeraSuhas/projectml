/* IDCFSS Step 2 - Clean Configuration (Minimal Aesthetic) */

function autoConfig() {
  const p = S.profile;
  S.missingConfig = {};
  S.outlierConfig = {};
  S.encodingConfig = {};
  S.scalingConfig = { method: 'standard', columns: [] };
  
  Object.entries(p.columns).forEach(([col, info]) => {
    if (info.missing > 0) {
      if (info.inferred_type === 'numeric') S.missingConfig[col] = info.missing_pct > 30 ? 'drop_column' : 'median';
      else S.missingConfig[col] = info.missing_pct > 30 ? 'drop_column' : 'mode';
    }
    if (info.inferred_type === 'numeric' && info.outlier_count > 0) {
      S.outlierConfig[col] = { method: 'iqr', action: 'cap' };
    }
    if (info.inferred_type === 'categorical') {
      S.encodingConfig[col] = info.unique <= 5 ? 'onehot' : 'label';
    }
    if (info.inferred_type === 'numeric' && !col.toLowerCase().includes('id')) {
      S.scalingConfig.columns.push(col);
    }
  });
}

function updateMissing(col, val) { if (val === 'none') delete S.missingConfig[col]; else S.missingConfig[col] = val; }
function updateOutlier(col, key, val) {
  if (val === 'none') { delete S.outlierConfig[col]; return; }
  if (!S.outlierConfig[col]) S.outlierConfig[col] = { method: 'iqr', action: 'cap' };
  S.outlierConfig[col][key] = val;
}
function updateEncoding(col, val) { if (val === 'none') delete S.encodingConfig[col]; else S.encodingConfig[col] = val; }

function tplClean() {
  const p = S.profile;
  const missingCols = Object.entries(p.columns).filter(([, i]) => i.missing > 0);
  const numCols = Object.entries(p.columns).filter(([, i]) => i.inferred_type === 'numeric');
  const catCols = Object.entries(p.columns).filter(([, i]) => i.inferred_type === 'categorical');

  const missingHtml = missingCols.map(([col, i]) => `
    <tr>
      <td style="font-weight:600">${col}</td>
      <td>${i.missing} (${i.missing_pct}%)</td>
      <td>
        <select onchange="updateMissing('${col}', this.value)">
          <option value="none">Ignore</option>
          <option value="mean" ${S.missingConfig[col] === 'mean' ? 'selected' : ''}>Mean Imputation</option>
          <option value="median" ${S.missingConfig[col] === 'median' ? 'selected' : ''}>Median Imputation</option>
          <option value="mode" ${S.missingConfig[col] === 'mode' ? 'selected' : ''}>Mode (Most Frequent)</option>
          <option value="knn" ${S.missingConfig[col] === 'knn' ? 'selected' : ''}>KNN Imputation</option>
          <option value="drop_row" ${S.missingConfig[col] === 'drop_row' ? 'selected' : ''}>Drop Rows</option>
          <option value="drop_column" ${S.missingConfig[col] === 'drop_column' ? 'selected' : ''}>Drop Column</option>
        </select>
      </td>
    </tr>
  `).join('');

  const outlierHtml = numCols.filter(([, i]) => i.outlier_count > 0).map(([col, i]) => `
    <tr>
      <td style="font-weight:600">${col}</td>
      <td>${i.outlier_count} detected</td>
      <td>
        <div style="display:flex; gap:12px;">
          <select onchange="updateOutlier('${col}', 'method', this.value)" style="width:140px">
            <option value="none">Ignore</option>
            <option value="iqr" ${(S.outlierConfig[col]?.method || 'iqr') === 'iqr' ? 'selected' : ''}>IQR</option>
            <option value="zscore" ${(S.outlierConfig[col]?.method) === 'zscore' ? 'selected' : ''}>Z-Score</option>
            <option value="isolation_forest" ${(S.outlierConfig[col]?.method) === 'isolation_forest' ? 'selected' : ''}>Iso. Forest</option>
          </select>
          <select onchange="updateOutlier('${col}', 'action', this.value)" style="width:140px">
            <option value="cap" ${(S.outlierConfig[col]?.action || 'cap') === 'cap' ? 'selected' : ''}>Cap</option>
            <option value="remove" ${(S.outlierConfig[col]?.action) === 'remove' ? 'selected' : ''}>Remove</option>
          </select>
        </div>
      </td>
    </tr>
  `).join('');

  const encodingHtml = catCols.map(([col, i]) => `
    <tr>
      <td style="font-weight:600">${col}</td>
      <td>${i.unique} unique</td>
      <td>
        <select onchange="updateEncoding('${col}', this.value)">
          <option value="none">Ignore</option>
          <option value="label" ${S.encodingConfig[col] === 'label' ? 'selected' : ''}>Label Encoding</option>
          <option value="onehot" ${S.encodingConfig[col] === 'onehot' ? 'selected' : ''}>One-Hot</option>
          <option value="binary" ${S.encodingConfig[col] === 'binary' ? 'selected' : ''}>Binary Encoding</option>
        </select>
      </td>
    </tr>
  `).join('');

  return `
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px;">
      <div>
        <h2 class="font-disp" style="font-size:48px;">CLEANING CONFIGURATION</h2>
        <div class="label-small">ADJUST PREPROCESSING STRATEGIES BEFORE EXECUTION</div>
      </div>
      <button class="btn" onclick="executeCleaning()">APPLY CLEANING</button>
    </div>
    
    <hr class="rule" style="margin-bottom:48px;">

    <div class="aesthetic-card mb-32">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">MISSING VALUES</div>
        <div class="aesthetic-card-subtitle">${missingCols.length} COLUMNS AFFECTED</div>
      </div>
      ${missingCols.length ? `
        <div class="table-wrap">
          <table><thead><tr><th>COLUMN</th><th>MISSING</th><th>STRATEGY</th></tr></thead><tbody>${missingHtml}</tbody></table>
        </div>
      ` : `<div class="text-muted" style="padding: 16px 0;">NO MISSING VALUES DETECTED.</div>`}
    </div>

    <div class="aesthetic-card mb-32">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">OUTLIER DETECTION</div>
        <div class="aesthetic-card-subtitle">NUMERIC COLUMNS WITH ANOMALIES</div>
      </div>
      ${outlierHtml ? `
        <div class="table-wrap">
          <table><thead><tr><th>COLUMN</th><th>OUTLIERS (IQR)</th><th>STRATEGY & ACTION</th></tr></thead><tbody>${outlierHtml}</tbody></table>
        </div>
      ` : `<div class="text-muted" style="padding: 16px 0;">NO SIGNIFICANT OUTLIERS DETECTED.</div>`}
    </div>

    <div class="aesthetic-card mb-32">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">CATEGORICAL ENCODING</div>
        <div class="aesthetic-card-subtitle">TRANSFORM TEXT TO NUMBERS</div>
      </div>
      ${catCols.length ? `
        <div class="table-wrap">
          <table><thead><tr><th>COLUMN</th><th>UNIQUE VALUES</th><th>STRATEGY</th></tr></thead><tbody>${encodingHtml}</tbody></table>
        </div>
      ` : `<div class="text-muted" style="padding: 16px 0;">NO CATEGORICAL COLUMNS DETECTED.</div>`}
    </div>

    <div class="aesthetic-card">
      <div class="aesthetic-card-header">
        <div class="aesthetic-card-title">FEATURE SCALING</div>
        <div class="aesthetic-card-subtitle">NORMALIZE NUMERIC RANGES</div>
      </div>
      <div style="padding: 16px 0;">
        <select onchange="S.scalingConfig.method = this.value" style="max-width:300px">
          <option value="none" ${S.scalingConfig.method === 'none' ? 'selected' : ''}>No Scaling</option>
          <option value="standard" ${S.scalingConfig.method === 'standard' ? 'selected' : ''}>Standard Scaler (Mean 0, Var 1)</option>
          <option value="minmax" ${S.scalingConfig.method === 'minmax' ? 'selected' : ''}>MinMax Scaler (0 to 1)</option>
          <option value="robust" ${S.scalingConfig.method === 'robust' ? 'selected' : ''}>Robust Scaler (Outlier resistant)</option>
        </select>
        <div class="text-muted" style="font-size:12px; margin-top:12px;">
          Applies to all numeric columns not excluded.
        </div>
      </div>
    </div>
  `;
}

async function executeCleaning() {
  showLoading('APPLYING CLEANING', 'EXECUTING PREPROCESSING PIPELINE');
  try {
    const payload = {
      session_id: S.sessionId,
      config: {
        missing: S.missingConfig,
        outliers: S.outlierConfig,
        encoding: S.encodingConfig,
        scaling: S.scalingConfig,
        drop_duplicates: S.dropDuplicates,
        target_column: S.targetColumn
      }
    };
    const r = await fetch(S.apiBase + '/clean', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!r.ok) {
      const e = await r.json();
      throw new Error(e.detail);
    }
    const d = await r.json();
    S.cleanedProfile = d.cleaned_profile;
    S.cleanedColumns = d.columns;
    S.cleanedPreview = d.preview;
    S.cleaningLog = d.cleaning_log;
    
    hideLoading();
    snack(`Dataset cleaned successfully`);
    advance();
  } catch (e) {
    hideLoading();
    snack(e.message, 'error');
  }
}
