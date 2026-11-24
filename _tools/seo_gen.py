# 동네값 지역·분야별 정적 페이지(SEO) 생성: sc/*.json(사이트 화면에서 뽑은 목록) → out/<분야>/<시도>/<시군구>/index.html
import json,glob,os,re,html,sys,collections,datetime,shutil
SC,OUT=sys.argv[1],sys.argv[2]
TODAY=datetime.date.today().isoformat()
E_=lambda s:html.escape(str(s or ''),quote=True)
# 해시 → (주소용 이름, 제목 명사, 설명 꼬리, 의료 여부)
CAT={
 'oil':('주유소','주유소 기름값','휘발유·경유 가격이 싼 순서',0),
 'pharm':('약국','약국','운영시간·비급여 가격',1),
 'swim':('수영장','수영장','공공 수영장 강습료와 수영장 목록',0),
 'gym':('헬스장','헬스장','헬스장 목록과 넓이',0),
 'pila':('필라테스','필라테스·요가','필라테스·요가 시설 목록',0),
 'golf':('골프연습장','골프연습장','골프연습장 목록',0),
 'study':('스터디카페','스터디카페','스터디카페 목록',0),
 'dojo':('태권도','태권도·체육도장','태권도장·체육도장 목록',0),
 'kids':('어린이집','어린이집','정원·현원과 남은 자리',0),
 'kinder':('유치원','유치원','학급·원아 수와 남은 자리',0),
 'aca':('학원','학원·교습소','교습비(수강료) 공개 정보',0),
 'elem':('초등학교','초등학교','학생 수·학급당 학생 수',0),
 'mid':('중학교','중학교','학생 수·학급당 학생 수',0),
 'high':('고등학교','고등학교','학생 수·학급당 학생 수',0),
 'obgy':('산부인과','산부인과','산부인과 목록',1),
 'ped':('소아과','소아청소년과','진료시간·야간·휴일 진료',1),
 'ent':('이비인후과','이비인후과','진료시간·야간·휴일 진료',1),
 'im':('내과','내과','진료시간·야간·휴일 진료',1),
 'vet':('동물병원','동물병원','동물병원 목록과 진료비 공개 정보',0),
 'vpharm':('동물약국','동물약국','동물약국 목록',0),
 'vgroom':('애견미용','애견미용','애견미용업체 목록',0),
 'vhotel':('애견호텔','애견호텔·위탁','동물위탁관리업체 목록',0),
 'care':('요양원','요양원','요양시설 비용·정원',0),
 'nhome':('주야간보호','주야간보호','주야간보호센터 목록',0),
 'visit':('방문요양','방문요양','방문요양기관 목록',0),
 'funeral':('장례식장','장례식장','장례식장 이용료',0),
 'campg':('캠핑장','캠핑장','캠핑장 요금',0),
 'mart':('마트','마트 가격','생필품 가격 비교',0),
 'apt':('아파트관리비','아파트 관리비','아파트 관리비 공개 정보',0),
 'camp':('자연휴양림','자연휴양림·야영장','숙박·야영 요금',0),
 'wed':('웨딩홀','웨딩홀','웨딩홀 대관·식대 공개 가격',0),
}
MAINCAT={'isa':('이사','이사 가격·업체'),'move':('입주청소','입주청소 가격'),'ac':('에어컨청소','에어컨청소 가격'),'wash':('세탁기청소','세탁기청소 가격'),
 'mat':('매트리스청소','매트리스청소 가격'),'grout':('줄눈시공','줄눈시공 가격'),'pest':('소독방역','소독·방역 업체'),'tan':('탄성코트','탄성코트 업체'),'build':('준공청소','준공·미화 업체')}
FULL={'서울특별시':'서울','부산광역시':'부산','대구광역시':'대구','인천광역시':'인천','광주광역시':'광주','대전광역시':'대전','울산광역시':'울산','세종특별자치시':'세종','경기도':'경기','강원특별자치도':'강원','강원도':'강원','충청북도':'충북','충청남도':'충남','전북특별자치도':'전북','전라북도':'전북','전라남도':'전남','경상북도':'경북','경상남도':'경남','제주특별자치도':'제주'}
def clean(t): return re.sub(r'\s*\([\d,]+\)\s*$','',t or '').strip()
def sdn(t):
    t=clean(t); return FULL.get(t,t)
def slug(t): return re.sub(r'[\s/·]+','-',t.strip()).strip('-')
pages={}   # path -> dict
GRP={'oil':['oil','pharm','swim','gym','pila'],'golf':['golf','study','dojo','kids','kinder'],'aca':['aca','elem','mid','high','obgy','ped'],
 'ent':['ent','im','vet','vpharm','vgroom','vhotel'],'care':['care','nhome','visit','funeral','campg','mart','apt','camp','wed']}
def segs(f,L):
    seg=-1; seen=set(); out=[]; ph=None
    for r in json.load(open(f)):
        if r['gu']=='' and (seg<0 or r['sd'] in seen or r['h']!=ph): seg+=1; seen=set()
        ph=r['h']
        if r['gu']=='': seen.add(r['sd'])
        r['h']=L[seg] if seg<len(L) else '?'; out.append(r)
    return out
for f in glob.glob(SC+'/*.json'):
    nm=os.path.basename(f)[:-5]
    if nm not in GRP: continue
    for r in segs(f,GRP[nm]):
        h=r['h']; 
        if h not in CAT: continue
        sd=sdn(r['sd']); gu=clean(r['gu'])
        if h=='oil' and not gu: continue
        it=r['it']
        if len(it)<3: continue
        # 이름에서 뒤에 붙은 표시(태그) 떼기
        for x in it:
            n=x['n']; T=[t for t in x.get('t',[]) if t]
            tail=''.join(T)
            if tail and n.endswith(tail): n=n[:-len(tail)].rstrip()
            else:
                for t in reversed(T):
                    if n.endswith(t): n=n[:-len(t)].rstrip()
            n=re.sub(r'\s*(N|↗)$','',n).strip()
            x['n']=n; x['t']=[t for t in T if t not in ('N','↗')]; x['m']=re.sub(r'\s+',' ',x.get('m') or '')
        key=(h,sd,gu); pages[key]={'kind':'v','h':h,'sd':sd,'gu':gu,'it':it}
mp=SC+'/main.json'
if os.path.exists(mp):
    for r in json.load(open(mp)):
        c=r['c']
        if c not in MAINCAT or len(r['rows'])<3: continue
        sd=sdn(r['sd']); gu=clean(r['gu'])
        if gu: continue   # 업체 출장지역이 시·도 단위라 시·군·구 페이지는 중복이 됨
        pages[('m:'+c,sd,gu)]={'kind':'m','c':c,'sd':sd,'gu':gu,'hd':r['hd'],'rows':r['rows']}
def cinfo(k):
    if k.startswith('m:'):
        a,b=MAINCAT[k[2:]]; return a,b,'공개된 가격이 낮은 순서',0,'#home'
    a,b,c,m=CAT[k]; return a,b,c,m,'#'+k
def url(k,sd,gu): 
    a=cinfo(k)[0]; return '/'+'/'.join(slug(x) for x in [a,sd,gu] if x)+'/'
def place(sd,gu): return (sd+' '+gu).strip()
CSS='''*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;color:#1a1d21;background:#f6f7f9;line-height:1.55}
a{color:#0b7a4b}header{background:#fff;border-bottom:1px solid #e5e7eb}header .in,main,footer .in{max-width:880px;margin:0 auto;padding:0 16px}header .in{display:flex;align-items:center;gap:12px;height:56px}
.logo{font-weight:800;font-size:20px;color:#0b7a4b;text-decoration:none}.bc{font-size:13px;color:#6b7280;margin:16px 0 6px}.bc a{color:#6b7280;text-decoration:none}
h1{font-size:22px;margin:4px 0 8px}.lead{color:#374151;margin:0 0 14px}.cta{display:block;text-align:center;background:#0b7a4b;color:#fff;font-weight:700;padding:13px;border-radius:10px;text-decoration:none;margin:14px 0}
.stat{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.stat div{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:10px 12px;flex:1;min-width:140px}.stat b{display:block;font-size:18px}.stat span{font-size:12px;color:#6b7280}
ol.li{list-style:none;margin:0;padding:0}ol.li li{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:12px 14px;margin:8px 0;display:flex;justify-content:space-between;gap:12px}
.nm{font-weight:700}.tg{display:inline-block;font-size:11px;background:#eef6f1;color:#0b7a4b;border-radius:6px;padding:1px 6px;margin-left:6px;font-weight:600}.ad{font-size:13px;color:#4b5563}.pr{text-align:right;white-space:pre-line;font-size:13px;color:#374151;min-width:96px}.pr b{font-size:15px;color:#111}
table{width:100%;border-collapse:collapse;background:#fff;font-size:13px}th,td{border-bottom:1px solid #e5e7eb;padding:8px 6px;text-align:left;vertical-align:top}th{background:#f3f4f6}
h2{font-size:17px;margin:26px 0 8px}.chips a{display:inline-block;background:#fff;border:1px solid #e5e7eb;border-radius:999px;padding:5px 11px;margin:3px;font-size:13px;text-decoration:none;color:#1f2937}
.note{font-size:12px;color:#6b7280;background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:10px 12px;margin:18px 0}footer{margin-top:30px;background:#fff;border-top:1px solid #e5e7eb;font-size:12px;color:#6b7280;padding:16px 0}
@media(max-width:600px){ol.li li{flex-direction:column}.pr{text-align:left}th:nth-child(n+4),td:nth-child(n+4){display:none}}'''
def won(s):
    m=re.findall(r'([\d,]{3,})\s*원',s or ''); return [int(x.replace(',','')) for x in m]
def page(key,P,body,title,desc,crumbs):
    ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":"https://dongnegap.com"+u} for i,(n,u) in enumerate(crumbs)]}
    bc=' › '.join(f'<a href="{E_(u)}">{E_(n)}</a>' for n,u in crumbs)
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E_(title)}</title><meta name="description" content="{E_(desc)}"><link rel="canonical" href="https://dongnegap.com{E_(crumbs[-1][1])}">
<meta property="og:type" content="website"><meta property="og:site_name" content="동네값"><meta property="og:title" content="{E_(title)}"><meta property="og:description" content="{E_(desc)}"><meta property="og:url" content="https://dongnegap.com{E_(crumbs[-1][1])}">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script><link rel="stylesheet" href="/seo.css"></head><body>
<header><div class="in"><a class="logo" href="/">동네값</a><span style="font-size:13px;color:#6b7280">공개된 가격만 모았습니다</span></div></header>
<main><div class="bc">{bc}</div>{body}
<div class="note">동네값은 정부·공공기관이 공개한 자료와 업체가 스스로 공개한 가격만 옮겨 보여 드리는 정보 사이트입니다. 중개하지 않고 연락처를 받지 않습니다. 가격·운영 정보는 바뀔 수 있으니 이용 전에 해당 업체·기관에 꼭 확인하세요. 기준일 {TODAY}.</div></main>
<footer><div class="in">동네값 · 운영 (주)지오크린 · <a href="/#terms">이용약관</a> · <a href="/#privacy">개인정보처리방침</a> · <a href="/#fix">정보 수정·삭제 요청</a></div></footer></body></html>'''
# 인덱스: 같은 시도의 시군구, 같은 지역의 다른 분야
bysd=collections.defaultdict(set); byplace=collections.defaultdict(set)
for (k,sd,gu) in pages:
    if gu: bysd[(k,sd)].add(gu)
    byplace[(sd,gu)].add(k)
written=[]
def W(path,txt):
    fp=OUT+path+'index.html'; os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,'w',encoding='utf-8').write(txt); written.append(path)
for key,P in pages.items():
    k,sd,gu=key; a,b,c,med,hs=cinfo(k); pl=place(sd,gu)
    crumbs=[('동네값','/'),(a,'/'+slug(a)+'/'),(sd,url(k,sd,''))]+([(gu,url(k,sd,gu))] if gu else [])
    if P['kind']=='v':
        it=P['it']; prices=[v for x in it for v in won(x['p'])[:1]]
        lis=''.join(f'<li><div><div class="nm">{E_(x["n"])}'+''.join(f'<span class="tg">{E_(t)}</span>' for t in x.get('t',[])[:2] if t!='N' and len(t)<24)+'</div>'+''.join(f'<div class="ad">{E_(l)}</div>' for l in x['a'][:3])+(f'<div class="ad">{E_(x["m"][:120])}</div>' if x.get('m') else '')+f'</div><div class="pr">{E_(x["p"].strip())}</div></li>' for x in it)
        stat=''
        if len(prices)>=3 and k in ('oil','swim','campg','camp','wed'):
            ps=sorted(prices); stat=f'<div class="stat"><div><b>{ps[0]:,}원</b><span>목록 중 가장 낮은 값</span></div><div><b>{ps[len(ps)//2]:,}원</b><span>가운데 값</span></div><div><b>{len(it)}곳</b><span>이 페이지 목록</span></div></div>'
        lead=f'{pl} {b} — {c}. 정부·공공기관과 업체가 공개한 자료만 정리했습니다.'
        body=f'<h1>{E_(pl)} {E_(b)}</h1><p class="lead">{E_(lead)}</p>{stat}<a class="cta" href="/{hs}">동네값에서 지도·전체 목록 보기 →</a><ol class="li">{lis}</ol>'
        title=f'{pl} {b} - 동네값'; desc=f'{pl} {b}: {c}. 정부·업체가 공개한 정보만 모았습니다. '+', '.join(x['n'] for x in it[:3])+' 등.'
    else:
        hd=P['hd'][1:] if P['hd'] and P['hd'][0]=='번호' else P['hd']; rows=[r[1:] if P['hd'] and P['hd'][0]=='번호' else r for r in P['rows']]
        rows=[[re.sub(r'(사업자 확인)+','',x).strip() for x in r] for r in rows]
        for r in rows: r[0]=re.sub(r'(\s+(이사|입주|줄눈|세탁기|소독|청소도 함|운영사 관련|이사 허가|가맹))+$','',r[0]).strip()
        keep=[i for i in range(len(hd)) if len({r[i] for r in rows if i<len(r)})>1 or i==0]
        hd=[hd[i] for i in keep]; rows=[[r[i] for i in keep if i<len(r)] for r in rows]
        tb='<table><tr>'+''.join(f'<th>{E_(x)}</th>' for x in hd)+'</tr>'+''.join('<tr>'+''.join(f'<td>{E_(x[:160])}</td>' for x in r)+'</tr>' for r in rows)+'</table>'
        body=f'<h1>{E_(pl)} {E_(b)}</h1><p class="lead">{E_(pl)}에 출장 가능한 업체 중 홈페이지·블로그에 가격을 공개한 곳을 {E_(c)}로 보여 드립니다.</p><a class="cta" href="/#home">동네값에서 전체 업체·가격 계산기 보기 →</a>{tb}'
        title=f'{pl} {b} - 공개된 가격 비교 | 동네값'; desc=f'{pl} {b}: 업체가 공개한 가격을 낮은 순으로 모았습니다. '+', '.join(r[0][:20] for r in rows[:3])+' 등.'
    # 내부 링크
    if gu:
        sib=sorted(bysd[(k,sd)]-{gu})
        if sib: body+=f'<h2>{E_(sd)} 다른 지역 {E_(b)}</h2><div class="chips">'+''.join(f'<a href="{E_(url(k,sd,g))}">{E_(g)}</a>' for g in sib)+'</div>'
    else:
        sub=sorted(bysd[(k,sd)])
        if sub: body+=f'<h2>{E_(sd)} 시·군·구별 {E_(b)}</h2><div class="chips">'+''.join(f'<a href="{E_(url(k,sd,g))}">{E_(g)}</a>' for g in sub)+'</div>'
    oth=sorted(byplace[(sd,gu)]-{k},key=lambda x:cinfo(x)[0])
    if oth: body+=f'<h2>{E_(pl)}의 다른 생활비 정보</h2><div class="chips">'+''.join(f'<a href="{E_(url(x,sd,gu))}">{E_(cinfo(x)[1])}</a>' for x in oth)+'</div>'
    W(url(k,sd,gu),page(key,P,body,title,desc,crumbs))
# 분야 첫 페이지
for k in sorted({k for k,_,_ in pages}):
    a,b,c,med,hs=cinfo(k); sds=sorted({sd for kk,sd,_ in pages if kk==k})
    body=f'<h1>지역별 {E_(b)}</h1><p class="lead">시·도와 시·군·구를 골라 보세요 — {E_(c)}.</p><a class="cta" href="/{hs}">동네값에서 지도로 보기 →</a>'
    for sd in sds:
        gl=sorted(bysd[(k,sd)])
        body+=f'<h2><a href="{E_(url(k,sd,""))}">{E_(sd)}</a></h2>'+('<div class="chips">'+''.join(f'<a href="{E_(url(k,sd,g))}">{E_(g)}</a>' for g in gl)+'</div>' if gl else '')
    W('/'+slug(a)+'/',page((k,'',''),None,body,f'지역별 {b} - 동네값',f'전국 시·군·구별 {b}: {c}. 정부·업체가 공개한 정보만 모았습니다.',[('동네값','/'),(a,'/'+slug(a)+'/')]))
# 전체 목록(사이트맵 겸 안내 페이지)
ks=sorted({k for k,_,_ in pages},key=lambda x:cinfo(x)[0])
body='<h1>지역별 생활비 정보 전체 보기</h1><div class="chips">'+''.join(f'<a href="/{E_(slug(cinfo(k)[0]))}/">{E_(cinfo(k)[1])}</a>' for k in ks)+'</div>'
W('/지역별/',page(('','',''),None,body,'지역별 생활비 정보 - 동네값','주유소·약국·수영장·어린이집·학원·청소·이사 등 지역별 생활비 정보를 정부·업체 공개 자료로 모았습니다.',[('동네값','/'),('지역별','/지역별/')]))
from urllib.parse import quote
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://dongnegap.com/</loc><lastmod>'+TODAY+'</lastmod></url>\n'+''.join(f'<url><loc>https://dongnegap.com{quote(p)}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in written)+'</urlset>\n'
open(OUT+'/sitemap.xml','w').write(sm); open(OUT+'/seo.css','w').write(CSS)
print('pages',len(written))
