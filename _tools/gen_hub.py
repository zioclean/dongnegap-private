# ── 동네 종합 페이지(/동네/시도/시군구/[동]/) + 순위 페이지(/순위/…) ── gen.py 안에서 exec로 실행
HUBK=['oil','pharm','ped','im','ent','kids','kinder','aca','swim','gym','pila','vet','care','study','elem']
def short(k): return cinfo(k)[1]
def first_price(P):
    ps=[v for x in P['it'] for v in won(x['p'])[:1]]; return min(ps) if ps else None
hubgu=collections.defaultdict(dict)
for (k,sd,gu),P in pages.items():
    if gu and P['kind']=='v': hubgu[(sd,gu)][k]=P
hubdg=collections.defaultdict(dict)
for (k,sd,gu,dg),D in dpages.items(): hubdg[(sd,gu,dg)][k]=D
def hurl(sd,gu,dg=''): return '/동네/'+'/'.join(slug(x) for x in [sd,gu,dg] if x)+'/'
def card(k,P,u,extra=''):
    names=', '.join(x['n'] for x in P['it'][:3])
    cn=f'<b>{P["cnt"]:,}곳</b>' if P.get('cntok',True) else '<b>보기 ›</b>'
    return f'<li><div><div class="nm"><a href="{E_(u)}">{E_(short(k))}</a></div><div class="ad">{E_(names)} 등</div>{extra}</div><div class="pr">{cn}</div></li>'
for (sd,gu),M in hubgu.items():
    if len(M)<3: continue
    pl=f'{sd} {gu}'; u=hurl(sd,gu); li=''; bits=[]
    for k in [x for x in HUBK if x in M]+[x for x in M if x not in HUBK]:
        P=M[k]; ex=''
        if k=='oil':
            p=first_price(P)
            if p: ex=f'<div class="ad">휘발유 최저 {p:,}원 · {E_(P["it"][0]["n"])}</div>'; bits.append(f'휘발유 최저 {p:,}원')
        if k=='swim':
            fs=[(v,x['n']) for x in P['it'] for v in won(x['p'])[:1]]
            if fs: v,n=min(fs); ex=f'<div class="ad">공공 수영장 강습 주3회 {v:,}원부터 · {E_(n)}</div>'
        li+=card(k,P,url(k,sd,gu),ex)
        if k in ('pharm','ped','kids','aca') and P.get('cntok'): bits.append(f'{short(k)} {P["cnt"]:,}곳')
    dl=sorted({dg for (s2,g2,dg) in hubdg if s2==sd and g2==gu})
    body=f'<h1>{E_(pl)} 생활비·동네 정보</h1><p class="lead">{E_(pl)}의 주유소 기름값, 약국·병원, 어린이집·유치원, 학원, 수영장·헬스장 정보를 한 장에 모았습니다. 정부·공공기관과 업체가 공개한 자료만 씁니다.</p><a class="cta" href="/">동네값에서 지도로 보기 →</a><ol class="li">{li}</ol>'
    if dl: body+=f'<h2>{E_(gu)} 동·읍·면별 종합</h2><div class="chips">'+''.join(f'<a href="{E_(hurl(sd,gu,d))}">{E_(d)}</a>' for d in dl)+'</div>'
    sib=sorted(g for (s2,g) in hubgu if s2==sd and g!=gu and len(hubgu[(s2,g)])>=3)
    if sib: body+=f'<h2>{E_(sd)} 다른 지역</h2><div class="chips">'+''.join(f'<a href="{E_(hurl(sd,g))}">{E_(g)}</a>' for g in sib)+'</div>'
    W(u,page(('hub',sd,gu),None,body,f'{pl} 생활비·동네 정보 (기름값·약국·병원·어린이집·학원) - 동네값',f'{pl} '+' · '.join(bits[:4])+' 등 생활비·동네 정보를 공개 자료로 모았습니다.',[('동네값','/'),('동네','/동네/'),(sd,'/동네/'+slug(sd)+'/'),(gu,u)]))
for (sd,gu,dg),M in hubdg.items():
    if len(M)<2: continue
    pl=f'{sd} {gu} {dg}'; u=hurl(sd,gu,dg); li=''; bits=[]
    for k in [x for x in HUBK if x in M]:
        D=M[k]; li+=card(k,{'it':D['it'],'cnt':D['cnt']},url(k,sd,gu)+slug(dg)+'/'); bits.append(f'{short(k)} {D["cnt"]}곳')
    G=hubgu.get((sd,gu),{})
    if 'oil' in G:
        p=first_price(G['oil'])
        if p: li+=f'<li><div><div class="nm"><a href="{E_(url("oil",sd,gu))}">{E_(gu)} 주유소 기름값</a></div><div class="ad">{E_(gu)} 전체 기준 휘발유 최저 {p:,}원 · {E_(G["oil"]["it"][0]["n"])}</div></div><div class="pr"><b>{p:,}원</b></div></li>'
    body=f'<h1>{E_(dg)} 생활비·동네 정보 <span style="font-size:15px;color:#6b7280">{E_(sd)} {E_(gu)}</span></h1><p class="lead">{E_(pl)}의 약국·병원·어린이집·학원·운동시설 정보를 한 장에 모았습니다. 정부·공공기관과 업체가 공개한 자료만 씁니다.</p><ol class="li">{li}</ol>'
    sib=sorted(d for (s2,g2,d) in hubdg if s2==sd and g2==gu and d!=dg and len(hubdg[(s2,g2,d)])>=2)
    if sib: body+=f'<h2>{E_(gu)} 다른 동네</h2><div class="chips">'+''.join(f'<a href="{E_(hurl(sd,gu,d))}">{E_(d)}</a>' for d in sib)+'</div>'
    body+=f'<h2>{E_(gu)} 전체</h2><div class="chips"><a href="{E_(hurl(sd,gu))}">{E_(sd)} {E_(gu)} 생활비·동네 정보</a></div>'
    W(u,page(('hub',sd,gu),None,body,f'{dg} 생활비·동네 정보 ({sd} {gu}) - 동네값',f'{pl} '+' · '.join(bits[:4])+' 등 동네 정보를 공개 자료로 모았습니다.',[('동네값','/'),('동네','/동네/'),(sd,'/동네/'+slug(sd)+'/'),(gu,hurl(sd,gu)),(dg,u)]))
sds=sorted({sd for (sd,gu) in hubgu if len(hubgu[(sd,gu)])>=3})
for sd in sds:
    gl=sorted(g for (s2,g) in hubgu if s2==sd and len(hubgu[(s2,g)])>=3)
    body=f'<h1>{E_(sd)} 동네별 생활비 정보</h1><div class="chips">'+''.join(f'<a href="{E_(hurl(sd,g))}">{E_(g)}</a>' for g in gl)+'</div>'
    W('/동네/'+slug(sd)+'/',page(('hub',sd,''),None,body,f'{sd} 동네별 생활비 정보 - 동네값',f'{sd} 시·군·구별 기름값·약국·병원·어린이집·학원 정보.',[('동네값','/'),('동네','/동네/'),(sd,'/동네/'+slug(sd)+'/')]))
W('/동네/',page(('hub','',''),None,'<h1>동네별 생활비 정보</h1><div class="chips">'+''.join(f'<a href="/동네/{E_(slug(sd))}/">{E_(sd)}</a>' for sd in sds)+'</div>','동네별 생활비 정보 - 동네값','전국 시·군·구, 동·읍·면별 생활비·동네 정보를 공개 자료로 모았습니다.',[('동네값','/'),('동네','/동네/')]))
# ── 순위 ──
RANKS=[]
def rank_page(slugname,title,desc,lead,rows,unit,lowbetter):
    # rows: [(sd,gu,value,link,note)]
    by=collections.defaultdict(list)
    for r in rows: by[r[0]].append(r)
    srt=lambda L:sorted(L,key=lambda r:(r[2] if lowbetter else -r[2]))
    top=srt(rows)[:30]
    tb=lambda L:'<table><tr><th>순위</th><th>지역</th><th>'+E_(unit)+'</th><th>참고</th></tr>'+''.join(f'<tr><td>{i+1}</td><td><a href="{E_(r[3])}">{E_(r[0]+" "+r[1])}</a></td><td><b>{r[2]:,}</b></td><td>{E_(r[4])}</td></tr>' for i,r in enumerate(L))+'</table>'
    body=f'<h1>{E_(title)}</h1><p class="lead">{E_(lead)}</p><h2>전국 상위 30</h2>{tb(top)}'
    for sd in sorted(by,key=lambda x:SIDO_ORD.index(x) if x in SIDO_ORD else 99):
        if len(by[sd])>=3: body+=f'<h2>{E_(sd)}</h2>{tb(srt(by[sd])[:10])}'
    u='/순위/'+slugname+'/'; W(u,page(('rank','',''),None,body,title+' - 동네값',desc,[('동네값','/'),('순위','/순위/'),(title,u)])); RANKS.append((title,u))
SIDO_ORD=['서울','경기','인천','부산','대구','광주','대전','울산','세종','강원','충북','충남','전북','전남','경북','경남','제주']
R=[]
for (sd,gu),M in hubgu.items():
    if 'oil' in M:
        p=first_price(M['oil'])
        if p: R.append((sd,gu,p,url('oil',sd,gu),M['oil']['it'][0]['n']))
if R: rank_page('기름값-싼-지역','휘발유 싼 동네 순위 (시·군·구별 최저가)','전국 시·군·구별로 가장 싼 주유소의 휘발유 가격을 비교한 순위입니다. 오피넷 공개 가격 기준.','시·군·구마다 가장 싼 주유소의 휘발유 1L 가격을 비교했습니다. 숫자가 낮을수록 싼 동네입니다. 가격은 매일 바뀌니 주유 전 확인하세요.',R,'휘발유 최저가(원)',True)
R=[]
for (sd,gu),M in hubgu.items():
    if 'swim' in M:
        for x in M['swim']['it']:
            if '주3회' in x['p']:
                v=won(x['p'])
                if v: R.append((sd,gu,v[0],url('swim',sd,gu),x['n']))
if len(R)>=5: rank_page('수영장-강습료-싼-곳','공공 수영장 강습료 싼 곳 순위 (성인 주3회)','구립·공공 수영장 성인 강습 월 수강료(주3회)를 싼 순서로 비교했습니다. 공공데이터포털 공개 자료 기준.','공공데이터포털에 요금이 공개된 공공 수영장의 성인 단체강습 월 수강료(주3회)를 비교했습니다. 기준월이 시설마다 다르니 신청 전 확인하세요.',R,'월 수강료(원)',True)
for k,nm in [('pharm','약국'),('ped','소아청소년과'),('aca','학원·교습소'),('kids','어린이집'),('kinder','유치원'),('gym','헬스장'),('pila','필라테스·요가'),('vet','동물병원'),('study','스터디카페'),('care','요양원'),('golf','골프연습장')]:
    R=[(sd,gu,M[k]['cnt'],url(k,sd,gu),', '.join(x['n'] for x in M[k]['it'][:2])) for (sd,gu),M in hubgu.items() if k in M and M[k].get('cntok')]
    if len(R)>=10: rank_page(slug(cinfo(k)[0])+'-많은-지역',f'{nm} 많은 동네 순위 (시·군·구별)',f'전국 시·군·구별 {nm} 수를 비교한 순위입니다. 정부 공개 자료 기준.',f'시·군·구마다 영업 중인 {nm} 수를 세어 비교했습니다. 인구가 많은 곳일수록 많아지는 점을 감안해 보세요.',R,f'{nm} 수(곳)',False)
W('/순위/',page(('rank','',''),None,'<h1>우리 동네는 몇 위?</h1><p class="lead">공개 자료로 계산한 지역별 순위입니다.</p><div class="chips">'+''.join(f'<a href="{E_(u)}">{E_(t)}</a>' for t,u in RANKS)+'</div>','우리 동네는 몇 위? 지역별 생활비 순위 - 동네값','기름값 싼 동네, 공공 수영장 강습료 싼 곳, 약국·소아과·학원 많은 동네 순위를 공개 자료로 계산했습니다.',[('동네값','/'),('순위','/순위/')]))
print('동네 종합(구)',sum(1 for k in hubgu if len(hubgu[k])>=3),'동네 종합(동)',sum(1 for k in hubdg if len(hubdg[k])>=2),'순위',len(RANKS))
