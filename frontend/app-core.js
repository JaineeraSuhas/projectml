/* IDCFSS Core State & Utilities */
const S={step:0,maxStep:0,sessionId:null,filename:null,profile:null,columns:[],preview:[],cleanedProfile:null,cleanedColumns:[],cleanedPreview:[],featureImportance:{},selectedFeatures:[],cleaningLog:[],missingConfig:{},outlierConfig:{},encodingConfig:{},scalingConfig:{method:'standard',columns:[]},dropDuplicates:true,targetColumn:null,featureMethod:'random_forest',nFeatures:10,
  // Auto-detect API base: empty string when served from FastAPI, fallback for local dev
  apiBase: window.location.port === '8000' || window.location.port === '80' || window.location.port === '443' || window.location.port === '' ? '' : 'http://localhost:8000'
};
window.addEventListener('scroll',()=>{document.getElementById('app-bar').classList.toggle('scrolled',window.scrollY>4)});
function snack(msg,type='success'){const icons={success:'✓',error:'✕',info:'ℹ'};const c=document.getElementById('snackbar-container');const el=document.createElement('div');el.className=`snackbar ${type}`;el.innerHTML=`<span class="snack-icon" style="font-size:16px;font-weight:700">${icons[type]}</span><span style="flex:1">${msg}</span>`;c.appendChild(el);setTimeout(()=>{el.style.opacity='0';el.style.transition='opacity .3s';setTimeout(()=>el.remove(),300)},4000)}
let loadingInterval = null;
function showLoading(h='Processing…',b='Please wait'){
  document.getElementById('loading-headline').textContent=h;
  document.getElementById('loading-body').textContent=b;
  document.getElementById('loading').classList.add('visible');
  const progEl = document.getElementById('loading-progress');
  if (progEl) {
    progEl.textContent = '0%';
    let p = 0;
    if (loadingInterval) clearInterval(loadingInterval);
    loadingInterval = setInterval(() => {
      if (p < 95) {
        p += Math.random() * (100 - p) * 0.1;
        progEl.textContent = Math.floor(p) + '%';
      }
    }, 150);
  }
}
function hideLoading(){
  if (loadingInterval) { clearInterval(loadingInterval); loadingInterval = null; }
  const progEl = document.getElementById('loading-progress');
  if (progEl) progEl.textContent = '100%';
  setTimeout(() => {
    document.getElementById('loading').classList.remove('visible');
  }, 200);
}
function goStep(n){if(n>S.maxStep)return;S.step=n;renderNav();render()}
function advance(){S.step++;S.maxStep=Math.max(S.maxStep,S.step);renderNav();render()}
function renderNav(){document.querySelectorAll('.step-item').forEach((el,i)=>{el.className='step-item';if(i<S.step)el.classList.add('done');else if(i===S.step)el.classList.add('active');else if(i>S.maxStep)el.classList.add('disabled');});const chip=document.getElementById('session-chip');if(S.sessionId){chip.style.display='flex';document.getElementById('session-id-text').textContent=S.sessionId.slice(0,8)+'…'}}
function render(){const main=document.getElementById('main-content');main.innerHTML='';const wrap=document.createElement('div');wrap.className='page';switch(S.step){case 0:wrap.innerHTML=tplUpload();break;case 1:wrap.innerHTML=tplProfile();break;case 2:wrap.innerHTML=tplClean();break;case 3:wrap.innerHTML=tplFeatures();break;case 4:wrap.innerHTML=tplExport();break}main.appendChild(wrap);if(S.step===0)bindUpload()}
async function apiPost(path,body){const r=await fetch(S.apiBase+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok){const e=await r.json().catch(()=>({detail:r.statusText}));throw new Error(e.detail||'API Error')}return r.json()}
function startOver(){Object.assign(S,{step:0,maxStep:0,sessionId:null,filename:null,profile:null,columns:[],preview:[],cleanedProfile:null,cleanedColumns:[],cleanedPreview:[],featureImportance:{},selectedFeatures:[],cleaningLog:[],missingConfig:{},outlierConfig:{},encodingConfig:{},scalingConfig:{method:'standard',columns:[]},dropDuplicates:true,targetColumn:null,featureMethod:'random_forest',nFeatures:10});document.getElementById('session-chip').style.display='none';renderNav();render()}
function toggleAcc(id){const body=document.getElementById(`body-${id}`);const chevron=document.getElementById(`chevron-${id}`);const open=body.classList.toggle('open');chevron?.classList.toggle('open',open)}
function toggleFeat(feat,el){const i=S.selectedFeatures.indexOf(feat);if(i>-1)S.selectedFeatures.splice(i,1);else S.selectedFeatures.push(feat);el?.classList.toggle('selected',S.selectedFeatures.includes(feat));const cb=el?.querySelector('input[type=checkbox]');if(cb)cb.checked=S.selectedFeatures.includes(feat)}
function topN(){S.selectedFeatures=Object.entries(S.featureImportance).sort((a,b)=>b[1]-a[1]).slice(0,S.nFeatures).map(([k])=>k);render()}
function autoConfig(){const p=S.profile;S.missingConfig={};S.outlierConfig={};S.encodingConfig={};for(const[col,info]of Object.entries(p.columns)){if(info.missing>0)S.missingConfig[col]=info.inferred_type==='numeric'?'median':'mode';if(info.inferred_type==='numeric'&&info.outlier_count>0)S.outlierConfig[col]={method:'iqr',action:'cap'};if(info.inferred_type==='categorical')S.encodingConfig[col]=info.unique>50?'binary':info.unique<=10?'onehot':'label'}const numCols=Object.entries(p.columns).filter(([,v])=>v.inferred_type==='numeric').map(([k])=>k);S.scalingConfig={method:'standard',columns:numCols};S.nFeatures=Math.min(10,numCols.length||5)}
