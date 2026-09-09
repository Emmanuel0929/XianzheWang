#!/usr/bin/env python3
from pathlib import Path
import json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'blog-translated-all'; out=ROOT/'blog/en'; out.mkdir(parents=True,exist_ok=True)
urls=json.loads((ROOT/'blog/image-map.json').read_text())
ids=['cot-agent','sora-china','aigc-unicorns','zero-initialization','nlp-value','claude-3','simple-methods','vidu','ehang-air-taxi','thought-structures','superalignment','paper-without-code','humanoid-robots','algorithm-engineers']
for n, ident in enumerate(ids,1):
    f=next(src.glob(f'{n:02d}_*.md'))
    text=f.read_text()
    for url,path in urls.items(): text=text.replace(url,path)
    tmp=out/(ident+'.md'); tmp.write_text(text)
    subprocess.run(['pandoc',str(tmp),'-f','gfm','-s','--css=../blog.css','--include-before-body='+str(ROOT/'blog/en-header.html'),'--include-after-body='+str(ROOT/'blog/en-footer.html'),'-o',str(out/(ident+'.html'))],check=True)
    tmp.unlink()
