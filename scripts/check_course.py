"""Structural audit of the course; does not certify teaching quality or learner mastery."""
from pathlib import Path
from urllib.parse import unquote
import re, sys, json
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT/'docs/course_20h'
errors=[];notes=[]
units=sorted(COURSE.glob('unit_*'))
if len(units)!=10:errors.append(f'Expected 10 units, got {len(units)}')
lessons=[]
for unit in units:
 files=sorted(unit.glob('[0-9][0-9]_*.md'));lessons.extend(files)
 if len(files)!=8:errors.append(f'{unit.name}: expected 8 lessons, got {len(files)}')
 for f in files:
  s=f.read_text();name=str(f.relative_to(ROOT))
  if len(re.findall(r'[\u4e00-\u9fff]',s))<900:errors.append(f'{name}: unusually short; review content')
  if not re.search(r'English|英文',s):errors.append(f'{name}: missing English term explanations')
  if s.count('<details>')<2 or s.count('<details>')!=s.count('</details>'):errors.append(f'{name}: missing/unbalanced answer disclosure')
  if re.search(r'^#{1,6}\s*\d+\s*[～–—~-]\s*\d+\s*分钟',s,re.M):errors.append(f'{name}: mechanical timing heading')
  if re.search(r'\b(SC|CP|CFD)\b',s):notes.append(f'{name}: inspect ambiguous abbreviation')
for f in ROOT.rglob('*.md'):
 if '.git' in f.parts:continue
 s=f.read_text();name=str(f.relative_to(ROOT))
 if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',s):errors.append(f'{name}: control character')
 if s.count('$$')%2:errors.append(f'{name}: unbalanced display math delimiters')
 # Ignore fenced code so example links in a template are not treated as links.
 clean=re.sub(r'```.*?```','',s,flags=re.S)
 for match in re.finditer(r'!?\[[^\]\n]*\]\(([^\n)]*)\)',clean):
  target=match.group(1).strip().strip('<>')
  if not target or re.match(r'^(https?:|mailto:|app:|#)',target):continue
  target=unquote(target.split('#',1)[0].split('?',1)[0])
  if not target:continue
  resolved=(ROOT/target.lstrip('/') if target.startswith('/') else f.parent/target).resolve()
  if not resolved.exists():errors.append(f'{name}: missing link {target}')
 # A varying number of unescaped pipes signals a broken table (often |PED|).
 table=[]
 for line in clean.splitlines()+['']:
  if line.startswith('|'):
   count=len(re.findall(r'(?<!\\)\|',line));table.append((line,count))
  else:
   if len(table)>1 and all(re.match(r'^\|[ :|\-]+\|$',x[0]) is None for x in table[1:2]) is False:
    expected=table[0][1]
    for row,count in table[2:]:
     if count!=expected:errors.append(f'{name}: table column mismatch: {row[:100]}')
   table=[]
for f in COURSE.rglob('*.svg'):
 try:ET.parse(f)
 except ET.ParseError as e:errors.append(f'{f.relative_to(ROOT)}: invalid SVG: {e}')
report={'units':len(units),'lessons':len(lessons),'chinese_characters':sum(len(re.findall(r'[\u4e00-\u9fff]',f.read_text())) for f in lessons),'figures':len(list(COURSE.rglob('*.svg'))),'errors':errors,'notes':notes}
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
