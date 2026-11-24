const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('file://'+process.env.G+'/index.html#home');await p.waitForTimeout(2500);const res=[];
const cats=await p.evaluate(()=>[...document.querySelectorAll('#catTabs [data-c]')].map(b=>[b.dataset.c,b.innerText.trim()]));
const grab=()=>p.evaluate(()=>{const t=[...document.querySelectorAll('#v-main table')].find(x=>x.offsetParent);if(!t)return {hd:[],rows:[]};
 const hd=[...t.rows[0].cells].map(c=>c.innerText.trim());const rows=[...t.rows].slice(1).map(r=>[...r.cells].map(c=>c.innerText.replace(/\s+/g,' ').trim())).filter(r=>r.length>2);return {hd,rows};});
for(const [c,cn] of cats){ await p.evaluate(c=>document.querySelector(`#catTabs [data-c="${c}"]`).click(),c); await p.waitForTimeout(800);
 await p.evaluate(()=>{const b=[...document.querySelectorAll('#v-main button')].find(x=>x.offsetParent&&x.innerText.trim()==='낮은가격순'); if(b) b.click();}); await p.waitForTimeout(300);
 const opts=await p.evaluate(()=>[...document.getElementById('rgSido').options].map(o=>[o.value,o.text]));
 for(const [sv,st] of opts){ if(sv==='') continue; await p.selectOption('#rgSido',sv); await p.waitForTimeout(400);
  res.push({c,cn,sd:st,gu:'',...await grab()});
  const gus=await p.evaluate(()=>[...document.getElementById('rgGu').options].map(o=>[o.value,o.text]));
  for(const [gv,gt] of gus){ if(gv==='') continue; await p.selectOption('#rgGu',gv); await p.waitForTimeout(250); res.push({c,cn,sd:st,gu:gt,...await grab()}); }
  await p.selectOption('#rgGu','').catch(()=>{});
 }
 console.error(c,res.length);
}
fs.writeFileSync(process.argv[2],JSON.stringify(res));await b.close()})()
