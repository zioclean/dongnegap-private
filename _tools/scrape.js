const {chromium}=require('playwright');const fs=require('fs');
const H=(process.argv[2]||'').split(',');const OUT=process.argv[3];const LIM=+process.argv[4]||1e9;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('file://'+process.env.G+'/index.html#hub');await p.waitForTimeout(1500);
await p.evaluate(()=>{try{localStorage.setItem('ckDay',new Date().toDateString())}catch(e){}});
const res=[];
for(const h of H){await p.evaluate(h=>{location.hash='#'+h},h);await p.waitForTimeout(3500);
 const meta=await p.evaluate(()=>{const v=[...document.querySelectorAll('main[id^=v-]')].find(x=>!x.hidden&&x.offsetParent);const S=[...v.querySelectorAll('select')].filter(s=>s.offsetParent);
  const sd=S.find(s=>/Sido$|Reg$|Rg$/.test(s.id)), gu=S.find(s=>/Gu$/.test(s.id));return {v:v.id,sd:sd&&sd.id,gu:gu&&gu.id,opts:sd?[...sd.options].map(o=>[o.value,o.text]):[]};});
 const grab=async()=>p.evaluate(()=>{const v=[...document.querySelectorAll('main[id^=v-]')].find(x=>!x.hidden&&x.offsetParent);
  const uls=[...v.querySelectorAll('ul')].filter(u=>u.offsetParent).sort((a,b)=>b.children.length-a.children.length);const u=uls[0];
  const it=u?[...u.children].slice(0,30).map(li=>{const nm=li.querySelector('.nm');return {n:nm?nm.innerText.split('\n')[0].trim():'',t:nm?[...nm.querySelectorAll('span,em')].map(x=>x.innerText.trim()).filter(Boolean):[],a:[...li.querySelectorAll('.ad')].map(x=>x.innerText.trim()).filter(Boolean),p:(li.querySelector('.pr')||{}).innerText||'',m:(li.querySelector('.kmid')||{}).innerText||''}}).filter(x=>x.n):[];
  const sum=[...v.querySelectorAll('.sumc,.sum div,.cards .card,.stat')].filter(x=>x.offsetParent).slice(0,6).map(x=>x.innerText.replace(/\s+/g,' ').trim());
  return {it,sum,h:(v.querySelector('h1,h2')||{}).innerText||''};});
 let n=0;
 for(const [sv,st] of meta.opts){ if(sv===''||/고르세요|전국/.test(st)) continue; if(n++>=LIM) break;
  await p.selectOption('#'+meta.sd,sv); await p.waitForTimeout(350);
  const r0=await grab(); res.push({h,sd:st,gu:'',...r0});
  if(meta.gu){ const gus=await p.evaluate(id=>[...document.getElementById(id).options].map(o=>[o.value,o.text]),meta.gu);
   for(const [gv,gt] of gus){ if(gv==='') continue; await p.selectOption('#'+meta.gu,gv); await p.waitForTimeout(250); const r=await grab(); res.push({h,sd:st,gu:gt,...r}); } }
 }
 console.error(h,meta.v,meta.sd,meta.gu,res.length);
}
fs.writeFileSync(OUT,JSON.stringify(res));await b.close()})()
