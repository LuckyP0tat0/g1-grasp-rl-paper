"""Check references, measured counts and known training budgets without Isaac."""
from pathlib import Path
import csv
import re

root = Path(__file__).resolve().parents[1]
text = (root / 'article.tex').read_text(encoding='utf-8-sig')
keys = re.findall(r'\\bibitem\{([^}]+)\}', text)
assert len(keys) == len(set(keys)), 'Duplicate bibliography keys'
citations = {key.strip() for group in re.findall(r'\\cite\{([^}]+)\}', text) for key in group.split(',')}
assert citations == set(keys), 'Missing or unused bibliography entries'
labels = re.findall(r'\\label\{([^}]+)\}', text)
assert len(labels) == len(set(labels)), 'Duplicate labels'
assert set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', text)) <= set(labels), 'Undefined labels'
for include in re.findall(r'\\input\{([^}]+)\}', text):
    assert (root / include).is_file(), include
rows = list(csv.DictReader((root / 'results/evaluations.csv').open(encoding='utf-8')))
assert len(rows) == 10 and len({r['evaluation_id'] for r in rows}) == 10
for row in rows:
    assert 0 <= int(row['successes']) <= int(row['episodes'])
    assert int(row['episodes']) > 0
    assert re.fullmatch('[0-9a-f]{64}', row['source_sha256'])
    if row['strategy'].startswith('goal_curriculum'):
        assert int(row['stage_transitions']) == 2000 * 96 * int(row['stage_updates'])
by_id = {r['evaluation_id']: r for r in rows}
assert by_id['separate_grasp_175']['checkpoint'] == '175'
assert by_id['separate_grasp_175']['successes'] == '62'
assert by_id['separate_approach_249']['stage_transitions'] == str(128 * 32 * 250)
assert by_id['separate_lift_999']['episodes'] == str(19 * 3)
for forbidden in ('/home/', 'C:\\Users\\', 'PRIVATE KEY', 'ghp_', 'github_pat_'):
    assert forbidden not in text, 'Private environment detail in article'
print('PASS: six cited references, cross-references, ten evaluation records and transition budgets')
