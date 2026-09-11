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

boards = [{"name": e.get("name", e["file"]),
           "roster": json.loads((root/'boards'/e["file"]).read_text(encoding='utf-8'))}
          for e in index]

block = ('<script type="application/json" id="starter-boards">\n'
         + json.dumps(boards, ensure_ascii=False) + '\n</script>\n')

marker = '<input type="file" id="filePicker" accept="image/*" hidden>'
if html.count(marker) != 1:
    sys.exit(f"expected exactly one filePicker input in {root/'index.html'}, found {html.count(marker)}")
html = html.replace(marker, marker + '\n' + block)

out.write_text(html, encoding='utf-8')
print(f"built {out}: {len(boards)} boards, "
      f"{sum(len(b['roster']) for b in boards)} cards, {len(html)//1024}KB")
