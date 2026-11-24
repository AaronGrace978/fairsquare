"""Optional: re-sync the manifest after editing agents.json. No build step is needed to run the site."""
import json, pathlib, re, shutil
root = pathlib.Path(__file__).parent
blob = json.dumps(json.loads((root / 'agents.json').read_text()), indent=2, ensure_ascii=False)
assert '</script' not in blob.lower()
html = (root / 'index.html').read_text()
html, n = re.subn(r'(<script type="application/json" id="fairsquare-manifest">).*?(</script>)',
                  lambda m: m.group(1) + blob + m.group(2), html, count=1, flags=re.S)
assert n == 1
(root / 'index.html').write_text(html)
(root / '.well-known').mkdir(exist_ok=True)
shutil.copy(root / 'agents.json', root / '.well-known' / 'agents.json')
(root / '.nojekyll').write_text('')
print('synced agents.json -> index.html, .well-known/agents.json')
