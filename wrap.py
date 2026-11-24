# 사이트 html(조각) → 완전한 문서(<!doctype html><html><head>…</head><body>…</body></html>)
import sys,re
s=open(sys.argv[1],encoding='utf-8').read()
if s.lstrip().lower().startswith('<!doctype'): sys.exit(0)
i=s.find('<header class="gnb"')
assert i>0
s='<!doctype html>\n<html lang="ko">\n<head>\n'+s[:i]+'</head>\n<body>\n'+s[i:]+'\n</body>\n</html>\n'
open(sys.argv[2] if len(sys.argv)>2 else sys.argv[1],'w',encoding='utf-8').write(s)
