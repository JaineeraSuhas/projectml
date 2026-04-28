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
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');
  :root {{
    --navy: #1A3C5E; --teal: #0D7377; --emerald: #14BDAC;
    --bg: #F0F7FA; --white: #ffffff; --text: #1a2332;
    --muted: #6b7a8d; --border: #dce8f0;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'DM Mono', monospace; background: var(--bg); color: var(--text); padding: 2rem; }}
  h1 {{ font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: var(--navy); }}
  h2 {{ font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 700; color: var(--navy); margin: 2rem 0 1rem; }}
  .header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; border-bottom: 3px solid var(--emerald); padding-bottom: 1rem; }}
  .subtitle {{ color: var(--muted); font-size: 0.85rem; margin-top: 0.25rem; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .card {{ background: var(--white); border-radius: 12px; padding: 1.25rem; border: 1px solid var(--border); }}
  .card-label {{ font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; }}
  .card-value {{ font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: var(--navy); }}
  .card-sub {{ font-size: 0.75rem; color: var(--emerald); }}
  .score-bar {{ background: #e2f0ed; border-radius: 99px; height: 8px; margin-top: 0.5rem; }}
  .score-fill {{ background: linear-gradient(90deg, var(--teal), var(--emerald)); border-radius: 99px; height: 8px; transition: width 1s; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--white); border-radius: 12px; overflow: hidden; margin-bottom: 1.5rem; border: 1px solid var(--border); }}
  th {{ background: var(--navy); color: white; padding: 0.75rem 1rem; text-align: left; font-family: 'Syne', sans-serif; font-size: 0.8rem; }}
  td {{ padding: 0.65rem 1rem; font-size: 0.82rem; border-bottom: 1px solid var(--border); }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f0f7fa; }}
  .badge {{ padding: 2px 8px; border-radius: 99px; font-size: 0.7rem; font-weight: 500; }}
  .badge-numeric {{ background: #dbeafe; color: #1d4ed8; }}
  .badge-categorical {{ background: #fce7f3; color: #be185d; }}
  .badge-datetime {{ background: #d1fae5; color: #065f46; }}
  .before-after {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }}
  .ba-card {{ background: var(--white); border-radius: 12px; padding: 1.5rem; border: 1px solid var(--border); }}
  .ba-card.before {{ border-top: 4px solid #ef4444; }}
  .ba-card.after {{ border-top: 4px solid var(--emerald); }}
  .ba-title {{ font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; margin-bottom: 1rem; }}
  .ba-stat {{ display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid var(--border); font-size: 0.83rem; }}
  .ba-stat:last-child {{ border-bottom: none; }}
  .fi-bar {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }}
  .fi-label {{ width: 180px; font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .fi-track {{ flex: 1; background: #e2f0ed; border-radius: 99px; height: 10px; }}
  .fi-fill {{ background: linear-gradient(90deg, var(--teal), var(--emerald)); border-radius: 99px; height: 10px; }}
  .fi-val {{ font-size: 0.75rem; color: var(--muted); width: 50px; text-align: right; }}
  footer {{ margin-top: 3rem; text-align: center; color: var(--muted); font-size: 0.75rem; border-top: 1px solid var(--border); padding-top: 1rem; }}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>IDCFSS Data Quality Report</h1>
    <div class="subtitle">Intelligent Data Cleaning & Feature Selection System</div>
  </div>
  <div style="text-align:right; font-size:0.78rem; color:var(--muted);">Generated by IDCFSS v1.0</div>
</div>

<div class="cards">
  <div class="card">
    <div class="card-label">Quality Score (Before)</div>
    <div class="card-value">{before_score}</div>
    <div class="score-bar"><div class="score-fill" style="width:{before_score}%"></div></div>
  </div>
  <div class="card">
    <div class="card-label">Quality Score (After)</div>
    <div class="card-value" style="color:var(--emerald)">{after_score}</div>
    <div class="score-bar"><div class="score-fill" style="width:{after_score}%"></div></div>
    <div class="card-sub">+{round(after_score - before_score, 1)} improvement</div>
  </div>
  <div class="card">
    <div class="card-label">Rows</div>
    <div class="card-value">{after_rows:,}</div>
    <div class="card-sub">of {before_rows:,} original</div>
  </div>
  <div class="card">
    <div class="card-label">Columns</div>
    <div class="card-value">{after_cols}</div>
    <div class="card-sub">of {before_cols} original</div>
  </div>
  <div class="card">
    <div class="card-label">Missing Cells</div>
    <div class="card-value">{cleaned_profile['missing_cells']}</div>
    <div class="card-sub">of {original_profile['missing_cells']} original</div>
  </div>
</div>

<h2>Before vs After</h2>
<div class="before-after">
  <div class="ba-card before">
    <div class="ba-title">Before Cleaning</div>
    <div class="ba-stat"><span>Rows</span><strong>{before_rows:,}</strong></div>
    <div class="ba-stat"><span>Columns</span><strong>{before_cols}</strong></div>
    <div class="ba-stat"><span>Missing Cells</span><strong>{original_profile['missing_cells']}</strong></div>
    <div class="ba-stat"><span>Missing %</span><strong>{original_profile['missing_pct']}%</strong></div>
    <div class="ba-stat"><span>Duplicates</span><strong>{original_profile['duplicate_rows']}</strong></div>
    <div class="ba-stat"><span>Quality Score</span><strong>{before_score}/100</strong></div>
  </div>
  <div class="ba-card after">
    <div class="ba-title">After Cleaning</div>
    <div class="ba-stat"><span>Rows</span><strong>{after_rows:,}</strong></div>
    <div class="ba-stat"><span>Columns</span><strong>{after_cols}</strong></div>
    <div class="ba-stat"><span>Missing Cells</span><strong>{cleaned_profile['missing_cells']}</strong></div>
    <div class="ba-stat"><span>Missing %</span><strong>{cleaned_profile['missing_pct']}%</strong></div>
    <div class="ba-stat"><span>Duplicates</span><strong>{cleaned_profile['duplicate_rows']}</strong></div>
    <div class="ba-stat"><span>Quality Score</span><strong>{after_score}/100</strong></div>
  </div>
</div>

<h2>Cleaning Log</h2>
<table>
  <thead><tr><th>Step</th><th>Column</th><th>Strategy</th><th>Detail</th></tr></thead>
  <tbody>{log_rows if log_rows else '<tr><td colspan="4" style="text-align:center;color:var(--muted)">No cleaning steps applied</td></tr>'}</tbody>
</table>

<h2>Column Summary (After Cleaning)</h2>
<table>
  <thead><tr><th>Column</th><th>Type</th><th>Missing</th><th>Missing %</th><th>Unique Values</th></tr></thead>
  <tbody>{col_rows}</tbody>
</table>

{'<h2>Feature Importance</h2><div id="fi-chart"></div>' if feature_importance else ''}
{'<h2>Selected Features</h2><p style="font-size:0.85rem;color:var(--muted)">' + ', '.join(selected_features) + '</p>' if selected_features else ''}

<script>
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
<footer>IDCFSS v1.0 &middot; Atria Institute of Technology, VTU Bangalore &middot; Jaineera</footer>
</body>
</html>"""
