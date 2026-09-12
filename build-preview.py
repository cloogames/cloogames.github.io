#!/usr/bin/env python3
"""Fold the boards folder into the page to make a single previewable file.

    python build-preview.py [out.html] [game-dir]

Both arguments are optional. The game folder defaults to guess-who/ next to
this script, so the script works from any working directory, and the output
defaults to guess-who-preview.html beside it.
"""
import json, pathlib, sys

here = pathlib.Path(__file__).resolve().parent
out  = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here/'guess-who-preview.html'
root = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else here/'guess-who'

if not (root/'index.html').is_file():
    sys.exit(f"no index.html in {root}")

html = (root/'index.html').read_text(encoding='utf-8')
index = json.loads((root/'boards'/'index.json').read_text(encoding='utf-8'))


def load(entry):
    """Roster plus, if the entry names one, the matching photo set folded in.

    The served page merges these at fetch time. Doing it here keeps the inline
    path showing the same board rather than a silently picture-less one.
    """
    roster = json.loads((root/'boards'/entry['file']).read_text(encoding='utf-8'))
    if entry.get('photos'):
        photos = json.loads((root/'photo-sets'/entry['photos']).read_text(encoding='utf-8'))
        by_name = {c['name']: c['img'] for c in photos if c.get('name') and c.get('img')}
        for card in roster:
            if card['name'] in by_name:
                card['img'] = by_name[card['name']]
    return roster


boards = [{"name": e.get("name", e["file"]), "roster": load(e)} for e in index]

block = ('<script type="application/json" id="starter-boards">\n'
         + json.dumps(boards, ensure_ascii=False) + '\n</script>\n')

marker = '<input type="file" id="filePicker" accept="image/*" hidden>'
if html.count(marker) != 1:
    sys.exit(f"expected exactly one filePicker input in {root/'index.html'}, found {html.count(marker)}")
html = html.replace(marker, marker + '\n' + block)

out.write_text(html, encoding='utf-8')
pics = sum(1 for b in boards for c in b['roster'] if c.get('img'))
print(f"built {out}: {len(boards)} boards, "
      f"{sum(len(b['roster']) for b in boards)} cards, {pics} with photos, {len(html)//1024}KB")
