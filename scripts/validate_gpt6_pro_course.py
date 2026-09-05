#!/usr/bin/env python3
"""Validate the new course only; historical material and learner progress are not rewritten."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import statistics
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'docs/course_gpt6_pro'


def numeric_checks() -> int:
    checks = []
    def eq(label, actual, expected):
        if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9):
            raise AssertionError(f'{label}: {actual} != {expected}')
        checks.append(label)
    eq('opportunity/refund', 2500-2000-800, -300)
    eq('comparative opportunity cost A', 3/6, .5)
    eq('comparative opportunity cost B', 2/2, 1)
    eq('base equilibrium price', (100+20)/4, 30)
    eq('base equilibrium quantity', 100-2*30, 40)
    eq('joint shift quantity', 120-2*30, 60)
    eq('cost shock price', (100+40)/4, 35)
    eq('cost shock quantity', 100-2*35, 30)
    eq('midpoint elastic', abs((-20/90)/(2/11)), 11/9)
    eq('unit arc elasticity', abs((-20/90)/(5/22.5)), 1)
    eq('revenue after increase', 12*80, 960)
    eq('contribution after increase', (12-6)*80, 480)
    eq('tax buyer price', 30+10/2, 35)
    eq('tax seller price', 30-10/2, 25)
    eq('tax quantity', 100-2*35, 30)
    eq('tax revenue', 10*30, 300)
    eq('tax CS', .5*(50-35)*30, 225)
    eq('tax PS', .5*(25-10)*30, 225)
    eq('tax DWL', 800-(225+225+300), 50)
    eq('tax 8 DWL', .5*8*8, 32)
    eq('tax 6 quantity', 100-2*33, 34)
    eq('tax 6 revenue', 6*34, 204)
    eq('subsidy quantity', 100-2*25, 50)
    eq('subsidy expenditure', 10*50, 500)
    eq('asymmetric tax share', 6/8, .75)
    eq('free trade CS', .5*(50-20)*60, 900)
    eq('free trade PS', .5*(20-10)*20, 100)
    eq('tariff CS', .5*(50-25)*50, 625)
    eq('tariff PS', .5*(25-10)*30, 225)
    eq('tariff revenue', 5*(50-30), 100)
    eq('tariff DWL', 1000-(625+225+100), 50)
    eq('foreign quota rent domestic welfare', 625+225, 850)
    eq('externality private Q', (100-20)/2, 40)
    eq('externality social Q', (100-20-20)/2, 30)
    eq('positive externality Q', (100+20-20)/2, 50)
    eq('abatement equal allocation', 2*10+2*40, 100)
    eq('abatement cost minimization', 4*10, 40)
    eq('NPV', -100+60/1.1+60/1.1**2, 500/121)
    eq('average tax rate', (10000*.1+10000*.2)/20000, .15)
    tc = lambda q: 100+10*q+q*q
    eq('TC q4', tc(4), 156)
    eq('discrete MC 4 to 5', tc(5)-tc(4), 19)
    eq('continuous MC at 5', 10+2*5, 20)
    eq('ATC minimum value', tc(10)/10, 30)
    eq('competitive profit P40', 40*15-tc(15), 125)
    eq('short run loss P18', 18*4-tc(4), -84)
    eq('short run advantage', -84-(-100), 16)
    eq('short run loss P22', 22*6-tc(6), -64)
    eq('discrete monopoly MR', 11*89-10*90, 79)
    eq('monopoly price', 100-40, 60)
    eq('monopoly profit', 60*40-(100+20*40), 1500)
    eq('monopoly DWL', .5*(80-40)*(60-20), 800)
    eq('Lerner index', (60-20)/60, 2/3)
    eq('alternative monopoly profit', 80*20-(80+40*20), 720)
    eq('repeat-game threshold', (10-8)/(10-4), 1/3)
    eq('VMPL', 20*8, 160)
    eq('MRPL', 15*8, 120)
    eq('monopsony quantity', 40/3, 13.333333333333334)
    eq('monopsony wage', 10+40/3, 70/3)
    eq('Gini population', 1-2*(.5*.25/2+.5*(.25+1)/2), .25)
    eq('EMTR', (100+500)/1000, .6)
    eq('consumer optimum x', 120/(2*10), 6)
    eq('consumer optimum y', 120/(2*20), 3)
    eq('consumer counterexample B', 6*3, 18)
    eq('consumer counterexample C', 10*1, 10)
    eq('Slutsky income', 5*6+20*3, 90)
    eq('Slutsky intermediate x', 90/(2*5), 9)
    eq('Slutsky intermediate y', 90/(2*20), 2.25)
    eq('Slutsky x SE', 9-6, 3)
    eq('Slutsky x IE', 12-9, 3)
    eq('Slutsky intermediate utility', 9*2.25, 20.25)
    eq('intertemporal future C', (100-60)*1.1, 44)
    eq('maintenance high effort', 10+.01*500, 15)
    eq('maintenance low effort', .05*500, 25)
    eq('maintenance deductible effort', 10+.01*100, 11)
    eq('lemons initial expected value', .5*200+.5*100, 150)
    eq('cost shock monopoly profit', 65*35-(100+30*35), 1125)
    return len(checks)


def validate() -> dict:
    expected = {COURSE/f'u{u:02d}'/f'{l:02d}.md' for u in range(1,11) for l in range(1,11)}
    actual = set(COURSE.glob('u[0-9][0-9]/[0-9][0-9].md'))
    if actual != expected:
        raise AssertionError(f'Lesson set mismatch. Missing: {sorted(expected-actual)}; extra: {sorted(actual-expected)}')
    required = ['README.md','GUIDE.md','GLOSSARY.md','WORKBOOK.md','SCOPE.md','SOURCES.md','CAPSTONE.md','AUDIT.md','course.json']
    for name in required:
        if not (COURSE/name).is_file():
            raise AssertionError('Missing required file: '+name)
    metadata = json.loads((COURSE/'course.json').read_text(encoding='utf-8'))
    assert metadata['lesson_count'] == 100
    assert metadata['unit_count'] == 10
    assert metadata['lessons_per_unit'] == 10
    assert metadata['reference_minutes_per_lesson'] * 100 == metadata['reference_total_minutes'] == 1200
    assert sorted(c for unit in metadata['units'] for c in unit['chapters']) == list(range(1,23))
    sizes = []
    for path in sorted(expected):
        text = path.read_text(encoding='utf-8')
        unit = int(path.parent.name[1:]); lesson = int(path.stem)
        if not re.search(r'^#\s+'+f'{unit:02d}\\.{lesson:02d}'+r'\b', text):
            # Use literal prefix to avoid regex differences across Unicode punctuation.
            if not text.startswith(f'# {unit:02d}.{lesson:02d}'):
                raise AssertionError('Lesson title ID mismatch: '+str(path))
        assert len(re.findall(r'^## ', text, flags=re.M)) >= 4, str(path)
        assert '<details>' in text and '</details>' in text and '<summary>' in text, str(path)
        assert f'../SOURCES.md#u{unit:02d}' in text, str(path)
        assert re.search(r'[A-Za-z]{3,}', text), str(path)
        count = len(re.findall(r'[\u4e00-\u9fff]', text))
        if count < 400:
            raise AssertionError(f'Unexpectedly short lesson: {path}: {count} Chinese characters')
        if re.search(r'(?i)\bTODO\b|\bTBD\b|待补充正文|此处占位', text):
            raise AssertionError('Placeholder found: '+str(path))
        if re.search(r'^#+\s*(?:第)?\s*\d+\s*[—–-]\s*\d+\s*分钟', text, re.M):
            raise AssertionError('Minute-sliced section found: '+str(path))
        sizes.append(count)
    for u in range(1,11):
        text = (COURSE/f'u{u:02d}'/'README.md').read_text(encoding='utf-8')
        assert '费曼' in text and '<details>' in text and '综合题' in text
        for l in range(1,11):
            assert f']({l:02d}.md)' in text, (u,l)
    sources = (COURSE/'SOURCES.md').read_text(encoding='utf-8')
    for u in range(1,11):
        assert f'id="u{u:02d}"' in sources
    assert '税率 20。' not in (COURSE/'u05/10.md').read_text(encoding='utf-8')
    assert 'C=(10,1)' in (COURSE/'u09/04.md').read_text(encoding='utf-8')
    checked_links = 0
    markdown = list(COURSE.rglob('*.md')) + [ROOT/p for p in ('README.md','START_HERE_20_HOURS.md','ROADMAP.md','docs/course_20h/README.md')]
    for path in markdown:
        raw = path.read_text(encoding='utf-8')
        raw = re.sub(r'```.*?```', '', raw, flags=re.S)
        for match in re.finditer(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', raw):
            destination = match.group(1).strip()
            if destination.startswith(('https://','http://','mailto:')):
                if re.search(r'\s', destination):
                    raise AssertionError(f'Malformed external URL in {path}: {destination}')
                continue
            target_part, _, fragment = destination.partition('#')
            if not target_part:
                target = path
            elif target_part.startswith('/'):
                target = ROOT / unquote(target_part.lstrip('/'))
            else:
                target = (path.parent/unquote(target_part)).resolve()
            if not target.exists():
                raise AssertionError(f'Broken local link in {path.relative_to(ROOT)}: {destination}')
            if fragment and target.name == 'SOURCES.md':
                target_text = target.read_text(encoding='utf-8')
                assert f'id="{fragment}"' in target_text, (path,destination)
            checked_links += 1
    return {'status':'passed', 'scope':'new course and current entry points; not a proof of all teaching claims',
            'lesson_count':100,'unit_count':10,'local_links_checked':checked_links,
            'numeric_regressions':numeric_checks(),'chinese_characters_in_lessons':sum(sizes),
            'minimum_lesson_chinese_characters':min(sizes),
            'median_lesson_chinese_characters':statistics.median(sizes),
            'maximum_lesson_chinese_characters':max(sizes),
            'estimated_first_pass_minutes':1200,
            'learner_mastery_not_inferred':True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--math-only', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = {'numeric_regressions':numeric_checks(),'status':'passed'} if args.math_only else validate()
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
