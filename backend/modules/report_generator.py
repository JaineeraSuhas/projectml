"""
IDCFSS - Report Generator Module
Generates comprehensive HTML quality reports with before/after comparison.
"""
import json
from typing import Dict, Optional


def generate_html_report(
    original_profile: Dict,
    cleaned_profile: Dict,
    cleaning_log: list,
    feature_importance: Optional[Dict] = None,
    selected_features: Optional[list] = None,
    encoding_map: Optional[Dict] = None,
) -> str:
    before_rows = original_profile["shape"]["rows"]
    after_rows = cleaned_profile["shape"]["rows"]
    before_cols = original_profile["shape"]["cols"]
    after_cols = cleaned_profile["shape"]["cols"]
    before_score = original_profile.get("quality_score", 0)
    after_score = cleaned_profile.get("quality_score", 0)
    missing_before = original_profile.get("missing_cells", 0)
    missing_after = cleaned_profile.get("missing_cells", 0)

    fi_json = json.dumps(feature_importance or {})
    sf_json = json.dumps(selected_features or [])

    log_rows = ""
    for entry in cleaning_log:
        log_rows += f"<tr><td>{entry.get('step','')}</td><td>{entry.get('column','—')}</td><td>{entry.get('strategy','')}</td><td>{entry.get('detail','')}</td></tr>"

    col_rows = ""
    for col, info in cleaned_profile.get("columns", {}).items():
        col_rows += f"""<tr>
            <td>{col}</td>
            <td><span class="badge badge-{info['inferred_type']}">{info['inferred_type']}</span></td>
            <td>{info['missing']}</td>
            <td>{info['missing_pct']}%</td>
            <td>{info['unique']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IDCFSS - Data Quality Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:wght@300;400;500&display=swap');
  
  :root {{
    --bg: #ffffff;
    --fg: #0d0d0d;
    --fg-muted: rgba(13,13,13,0.45);
    --rule: 1px solid rgba(13,13,13,0.15);
    --font-disp: 'Playfair Display', 'Times New Roman', Georgia, serif;
    --font-sans: 'DM Sans', 'Helvetica Neue', Arial, sans-serif;
  }}

  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #030303;
      --fg: #ffffff;
      --fg-muted: rgba(255,255,255,0.45);
      --rule: 1px solid rgba(255,255,255,0.15);
    }}
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ 
    background: var(--bg); 
    color: var(--fg); 
    font-family: var(--font-sans); 
    font-size: 14px;
    line-height: 1.6;
    padding: 64px 32px;
    max-width: 1400px;
    margin: 0 auto;
    -webkit-font-smoothing: antialiased;
    transition: background 0.6s, color 0.6s;
  }}

  h1, h2, .font-disp {{
    font-family: var(--font-disp);
    font-weight: 900;
    letter-spacing: -0.02em;
    text-transform: uppercase;
  }}

  .label-small {{
    font-family: var(--font-sans);
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--fg-muted);
  }}

  .header {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 64px;
  }}

  .rule-line {{
    border: none;
    border-top: var(--rule);
    margin: 48px 0;
  }}

  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 32px;
    margin-bottom: 64px;
  }}

  .stat-block {{
    border-right: var(--rule);
    padding-right: 32px;
  }}
  .stat-block:last-child {{ border-right: none; }}

  .aesthetic-card {{
    border: var(--rule);
    padding: 32px;
    margin-bottom: 32px;
  }}
  .aesthetic-card-header {{
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: var(--rule);
  }}
  .aesthetic-card-title {{
    font-size: 24px;
  }}

  .table-wrap {{
    width: 100%;
    overflow-x: auto;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }}
  th {{
    font-family: var(--font-sans);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--fg-muted);
    padding: 16px 12px;
    border-bottom: var(--rule);
    font-weight: normal;
  }}
  td {{
    padding: 16px 12px;
    border-bottom: var(--rule);
    font-size: 13px;
  }}

  .badge {{
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid var(--fg-muted);
    padding: 2px 8px;
    border-radius: 99px;
  }}

  .fi-bar {{ display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }}
  .fi-label {{ width: 200px; font-weight: 500; font-family: var(--font-sans); font-size: 13px; }}
  .fi-track {{ flex: 1; height: 4px; background: rgba(13,13,13,0.1); position: relative; }}
  @media (prefers-color-scheme: dark) {{
    .fi-track {{ background: rgba(255,255,255,0.1); }}
  }}
  .fi-fill {{ background: var(--fg); height: 100%; position: absolute; left: 0; top: 0; }}
  .fi-val {{ font-family: var(--font-sans); font-size: 12px; width: 60px; text-align: right; }}

  footer {{
    margin-top: 64px;
    text-align: center;
    color: var(--fg-muted);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1 style="font-size: 48px; line-height: 1;">QUALITY REPORT</h1>
      <div class="label-small" style="margin-top: 12px;">I.D.C.F.S.S — AUTOMATED PROFILING & PIPELINE SUMMARY</div>
    </div>
    <div class="label-small">V 1.0</div>
  </div>

  <hr class="rule-line">

  <div class="grid-3">
    <div class="stat-block">
      <div class="label-small">QUALITY SCORE (AFTER)</div>
      <div class="font-disp" style="font-size: 48px;">{after_score}</div>
      <div class="label-small" style="text-transform:none;">Was {before_score} (+{round(after_score - before_score, 1)})</div>
    </div>
    <div class="stat-block">
      <div class="label-small">ROWS</div>
      <div class="font-disp" style="font-size: 48px;">{after_rows:,}</div>
      <div class="label-small" style="text-transform:none;">Original: {before_rows:,}</div>
    </div>
    <div class="stat-block">
      <div class="label-small">COLUMNS</div>
      <div class="font-disp" style="font-size: 48px;">{after_cols}</div>
      <div class="label-small" style="text-transform:none;">Original: {before_cols}</div>
    </div>
    <div class="stat-block" style="border-right: none;">
      <div class="label-small">MISSING CELLS</div>
      <div class="font-disp" style="font-size: 48px;">{cleaned_profile['missing_cells']}</div>
      <div class="label-small" style="text-transform:none;">Original: {original_profile['missing_cells']}</div>
    </div>
  </div>

  <div class="aesthetic-card">
    <div class="aesthetic-card-header">
      <div class="aesthetic-card-title font-disp">CLEANING PIPELINE LOG</div>
      <div class="label-small" style="margin-top: 8px;">RECORD OF TRANSFORMATIONS APPLIED</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>STEP</th><th>COLUMN</th><th>STRATEGY</th><th>DETAIL</th></tr>
        </thead>
        <tbody>
          {log_rows if log_rows else '<tr><td colspan="4" style="text-align:center;color:var(--fg-muted)">No cleaning steps applied</td></tr>'}
        </tbody>
      </table>
    </div>
  </div>

  <div class="aesthetic-card">
    <div class="aesthetic-card-header">
      <div class="aesthetic-card-title font-disp">COLUMN PROFILES (FINAL)</div>
      <div class="label-small" style="margin-top: 8px;">POST-PROCESSING STATISTICS</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>COLUMN</th><th>TYPE</th><th>MISSING</th><th>MISSING %</th><th>UNIQUE</th></tr>
        </thead>
        <tbody>
          {col_rows}
        </tbody>
      </table>
    </div>
  </div>

  <div class="aesthetic-card">
    <div class="aesthetic-card-header">
      <div class="aesthetic-card-title font-disp">PERFORMANCE RATE & DIFFERENCE</div>
      <div class="label-small" style="margin-top: 8px;">DATA QUALITY METRICS COMPARISON</div>
    </div>
    <div id="perf-chart"></div>
  </div>

  {'<div class="aesthetic-card"><div class="aesthetic-card-header"><div class="aesthetic-card-title font-disp">FEATURE IMPORTANCE</div><div class="label-small" style="margin-top: 8px;">PREDICTIVE POWER ANALYSIS</div></div><div id="fi-chart"></div></div>' if feature_importance else ''}
  
  {'<div class="aesthetic-card"><div class="aesthetic-card-header"><div class="aesthetic-card-title font-disp">SELECTED FEATURES</div><div class="label-small" style="margin-top: 8px;">SUBSET FOR MODELING</div></div><p style="font-family: var(--font-sans); font-size: 14px; font-weight: 500;">' + ', '.join(selected_features) + '</p></div>' if selected_features else ''}

<script>
const perfData = [
  { label: 'Quality Score', before: {before_score}, after: {after_score} },
  { label: 'Missing Cells', before: {missing_before}, after: {missing_after} },
  { label: 'Rows Retained', before: {before_rows}, after: {after_rows} }
];

const perfContainer = document.getElementById('perf-chart');
if (perfContainer) {{
  perfContainer.innerHTML = perfData.map(d => {{
    const maxVal = Math.max(d.before, d.after, 1);
    const beforePct = Math.max(1, (d.before / maxVal) * 100);
    const afterPct = Math.max(1, (d.after / maxVal) * 100);
    const diff = d.after - d.before;
    const diffSign = diff > 0 ? '+' : '';
    let diffColor = 'var(--fg-muted)';
    if (d.label === 'Missing Cells') {{
      diffColor = diff < 0 ? '#4caf50' : (diff > 0 ? '#f44336' : 'var(--fg-muted)');
    }} else {{
      diffColor = diff > 0 ? '#4caf50' : (diff < 0 ? '#f44336' : 'var(--fg-muted)');
    }}
    
    return `
    <div style="margin-bottom: 24px;">
      <div style="display:flex; justify-content:space-between; margin-bottom: 8px;">
        <div class="fi-label" style="font-size:14px;">${{d.label}}</div>
        <div style="font-size:12px; font-weight:600; color:${{diffColor}}; font-family: var(--font-sans);">${{diffSign}}${{d.label === 'Quality Score' ? diff.toFixed(1) : diff.toFixed(0)}} difference</div>
      </div>
      <div class="fi-bar" style="margin-bottom: 4px;">
        <span style="width: 60px; font-size:12px; color:var(--fg-muted);">Before</span>
        <div class="fi-track"><div class="fi-fill" style="width:${{beforePct}}%; background:var(--fg-muted);"></div></div>
        <span class="fi-val">${{d.label === 'Quality Score' ? d.before.toFixed(1) : Math.round(d.before).toLocaleString()}}</span>
      </div>
      <div class="fi-bar">
        <span style="width: 60px; font-size:12px;">After</span>
        <div class="fi-track"><div class="fi-fill" style="width:${{afterPct}}%;"></div></div>
        <span class="fi-val">${{d.label === 'Quality Score' ? d.after.toFixed(1) : Math.round(d.after).toLocaleString()}}</span>
      </div>
    </div>
    `;
  }}).join('');
}}

const fi = {fi_json};
const container = document.getElementById('fi-chart');
if (container && Object.keys(fi).length > 0) {{
  const sorted = Object.entries(fi).sort((a,b) => b[1]-a[1]).slice(0,20);
  const maxVal = sorted[0][1];
  container.innerHTML = sorted.map(([k,v]) => `
    <div class="fi-bar">
      <span class="fi-label" title="${{k}}">${{k}}</span>
      <div class="fi-track"><div class="fi-fill" style="width:${{Math.round(v/maxVal*100)}}%"></div></div>
      <span class="fi-val">${{v.toFixed(4)}}</span>
    </div>
  `).join('');
}}
</script>

  <footer>
    IDCFSS V1.0 &middot; AUTOMATED PIPELINE &middot; DATA QUALITY ASSURED
  </footer>
</body>
</html>"""
