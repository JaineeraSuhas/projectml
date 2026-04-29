/* IDCFSS Step 3 & 4 - Features and Export (Minimal Aesthetic) */

function tplFeatures() {
  const p = S.cleanedProfile || S.profile;
  const cols = Object.keys(p.columns);
  
  const hasFeatures = Object.keys(S.featureImportance).length > 0;
  
  let resultHtml = '';
  if (hasFeatures) {
    const sorted = Object.entries(S.featureImportance).sort((a,b)=>b[1]-a[1]);
    const maxVal = sorted[0]?.[1] || 1;
    
    const rows = sorted.map(([col, score], idx) => {
      const isSelected = S.selectedFeatures.includes(col);
      const pct = Math.max(1, (score / maxVal) * 100);
      return `
        <tr>
          <td style="width: 40px; color: ${isSelected ? 'var(--fg)' : 'var(--fg-muted)'}; font-weight: 600;">
            ${isSelected ? '✓' : ''}
          </td>
          <td style="font-weight: 600; color: ${isSelected ? 'var(--fg)' : 'var(--fg-muted)'};">${col}</td>
          <td>
            <div style="width: 100%; height: 4px; background: rgba(13,13,13,0.1);">
              <div style="width: ${pct}%; height: 100%; background: ${isSelected ? 'var(--fg)' : 'var(--fg-muted)'};"></div>
            </div>
          </td>
          <td style="text-align: right; font-family: var(--font-mono); font-size:12px;">
            ${score.toFixed(4)}
          </td>
        </tr>
      `;
    }).join('');
    
    resultHtml = `
      <div class="aesthetic-card mt-32">
        <div class="aesthetic-card-header">
          <div class="aesthetic-card-title">IMPORTANCE SCORES</div>
          <div class="aesthetic-card-subtitle">TOP ${S.selectedFeatures.length} FEATURES SELECTED</div>
        </div>
        <div class="table-wrap">
          <table style="table-layout: fixed;">
            <colgroup><col style="width:50px"><col style="width:25%"><col><col style="width:100px"></colgroup>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }

  return `
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px;">
      <div>
        <h2 class="font-disp" style="font-size:48px;">FEATURE SELECTION</h2>
        <div class="label-small">IDENTIFY THE MOST PREDICTIVE VARIABLES</div>
      </div>
      ${hasFeatures ? `<button class="btn" onclick="advance()">PROCEED TO EXPORT</button>` : ''}
    </div>
    
    <hr class="rule" style="margin-bottom:48px;">

    <div class="grid-2">
      <div class="aesthetic-card">
        <div class="form-group">
          <label>Target Variable (Y)</label>
          <select onchange="S.targetColumn = this.value">
            <option value="">-- Select Target (Optional) --</option>
            ${cols.map(c => `<option value="${c}" ${S.targetColumn===c?'selected':''}>${c}</option>`).join('')}
          </select>
        </div>
        
        <div class="form-group">
          <label>Selection Algorithm</label>
          <select onchange="S.featureMethod = this.value">
            <option value="random_forest" ${S.featureMethod==='random_forest'?'selected':''}>Random Forest Importance</option>
            <option value="xgboost" ${S.featureMethod==='xgboost'?'selected':''}>XGBoost Importance</option>
            <option value="lasso" ${S.featureMethod==='lasso'?'selected':''}>Lasso Regression (L1)</option>
            <option value="mutual_info" ${S.featureMethod==='mutual_info'?'selected':''}>Mutual Information</option>
            <option value="anova" ${S.featureMethod==='anova'?'selected':''}>ANOVA F-value</option>
            <option value="correlation" ${S.featureMethod==='correlation'?'selected':''}>Correlation Filter</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Features to Select</label>
          <input type="number" value="${S.nFeatures}" onchange="S.nFeatures = parseInt(this.value) || 10" min="1" max="${cols.length}" />
        </div>
        
        <button class="btn" style="width: 100%; justify-content: center;" onclick="runFeatureSelection()">RUN SELECTION ALGORITHM</button>
      </div>
      
      <div>
        ${resultHtml || `
          <div style="height: 100%; border: 1px dashed rgba(13,13,13,0.3); display: flex; align-items: center; justify-content: center; flex-direction: column; text-align: center; padding: 32px;">
            <div class="font-disp" style="font-size:24px; margin-bottom:8px; color:var(--fg-muted);">AWAITING CONFIGURATION</div>
            <div class="label-small">SELECT A TARGET VARIABLE AND ALGORITHM TO BEGIN</div>
          </div>
        `}
      </div>
    </div>
  `;
}

async function runFeatureSelection() {
  showLoading('ANALYZING FEATURES', 'CALCULATING IMPORTANCE SCORES');
  try {
    const payload = {
      session_id: S.sessionId,
      config: {
        target_column: S.targetColumn,
        method: S.featureMethod,
        n_features: S.nFeatures
      }
    };
    const r = await fetch(S.apiBase + '/features', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!r.ok) {
      const e = await r.json();
      throw new Error(e.detail);
    }
    const d = await r.json();
    S.featureImportance = d.feature_importance;
    S.selectedFeatures = d.selected_features;
    
    hideLoading();
    snack(`Selected top ${S.selectedFeatures.length} features`);
    render();
  } catch (e) {
    hideLoading();
    snack(e.message, 'error');
  }
}

function tplExport() {
  const repUrl = S.apiBase + '/report/' + S.sessionId;
  const csvUrl = S.apiBase + '/download/' + S.sessionId + '?format=csv';
  const xlsxUrl = S.apiBase + '/download/' + S.sessionId + '?format=xlsx';
  const pyUrl = S.apiBase + '/pipeline/' + S.sessionId + '?format=python';

  return `
    <div style="text-align:center; padding: 80px 0 40px;">
      <div class="label-small" style="margin-bottom: 16px;">PIPELINE COMPLETE</div>
      <h2 class="hero-title-huge">DATASET READY</h2>
    </div>

    <hr class="rule" style="margin-bottom:64px;">
    
    <div class="grid-2">
      <div class="aesthetic-card">
        <div class="aesthetic-card-header">
          <div class="aesthetic-card-title">CLEANED DATASET</div>
          <div class="aesthetic-card-subtitle">READY FOR MODEL TRAINING</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:16px;">
          <a href="${csvUrl}" class="btn" style="justify-content:center;">DOWNLOAD AS CSV</a>
          <a href="${xlsxUrl}" class="btn" style="justify-content:center;">DOWNLOAD AS EXCEL</a>
        </div>
      </div>
      
      <div class="aesthetic-card">
        <div class="aesthetic-card-header">
          <div class="aesthetic-card-title">ARTIFACTS & CODE</div>
          <div class="aesthetic-card-subtitle">REPRODUCIBILITY AND REPORTS</div>
        </div>
        <div style="display:flex; flex-direction:column; gap:16px;">
          <a href="${pyUrl}" class="btn" style="justify-content:center;">DOWNLOAD PYTHON SCRIPT</a>
          <a href="${repUrl}" target="_blank" class="btn" style="justify-content:center;">VIEW QUALITY REPORT</a>
        </div>
      </div>
    </div>
    
    <div style="text-align:center; margin-top:80px;">
      <button class="btn btn-text" onclick="startOver()">START NEW SESSION</button>
    </div>
  `;
}
