import json, os, glob, collections

base = r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING2\stage1'
files = glob.glob(os.path.join(base, '*.json'))

fails = []
for fp in files:
    with open(fp) as fh:
        data = json.load(fh)
    if data.get('verdict') == 'FAIL':
        fails.append({
            'filename': os.path.basename(fp),
            'symbol': data.get('symbol', ''),
            'direction': data.get('direction', ''),
            'sl_type': data.get('sl_type', ''),
            'note': data.get('note', '')
        })

# Group by note
by_note = collections.defaultdict(list)
for item in fails:
    by_note[item['note']].append(item)

print(f'Total FAIL files: {len(fails)}')
print()
print('=== Grouped by error type ===')
for note, items in sorted(by_note.items()):
    print(f'\n--- {note} ({len(items)} files) ---')
    for item in items:
        print(f'  {item["filename"]}')

# Separate OPT ERROR
opt_errors = [item for item in fails if 'OPT ERROR' in item['note']]
other_fails = [item for item in fails if 'OPT ERROR' not in item['note']]

print(f'\n\n=== COUNTS ===')
print(f'OPT ERROR: {len(opt_errors)}')
print(f'Other failures: {len(other_fails)}')

# Write OPT ERROR list to file — output next to this script
output_lines = []
for item in opt_errors:
    output_lines.append(f'{item["symbol"]} {item["direction"]} {item["sl_type"]}')

outpath = os.path.join(os.path.dirname(__file__), 'swing2_stage1_fails.txt')
with open(outpath, 'w') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f'\nWrote {len(output_lines)} OPT ERROR combos to {outpath}')
